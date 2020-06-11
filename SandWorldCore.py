import json
import random
import discord
import requests
import asyncio
import uuid
import pyshorteners
import pymongo
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
CoreVersion = "1.5.1"
client = pymongo.MongoClient("MongoDBServerURL")
db = client.SandWorldDB
profiles = db.Profiles
other = db.Other
# Beta user table "414039381398257704": {"Balance": 3000000000580, "shovel": true, "Armor": {"BlockPlus": 300, "Name": "Test"}, "Item": {"AttackPlus": 300, "SandFarmPlus": 0, "Name": "Test"}}
def CreateArmor(ArmorPlus, ArmorName):
    return {"BlockPlus": ArmorPlus, "Name": ArmorName}
def CreateItem(SandFarmPlus, AttackPlus, Name):
    return {"AttackPlus": AttackPlus, "SandFarmPlus": SandFarmPlus, "Name": Name}
def GetPlayerItem(UserId):
    return profiles.find_one({'_id': str(UserId)})['Item']
def payment_history_last(my_login, api_access_token, rows_num, next_TxnId, next_TxnDate):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token  
    parameters = {'rows': rows_num, 'nextTxnId': next_TxnId, 'nextTxnDate': next_TxnDate}
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + my_login + '/payments', params = parameters)
    return h.json()
def create_payment_link(uuid):
    URL = f'https://qiwi.com/payment/form/99?extra[\'comment\']={uuid}&extra[\'account\']=Phone Number&amountInteger=50&amountFraction=0&blocked[0]=account&blocked[1]=comment'
    short = pyshorteners.Shortener()
    return short.tinyurl.short(URL)

def CheckPay(Uuid):
    for Payment in payment_history_last('Phone Number', 'Api key', 2, '', '')['data']:
        if Payment['type'] == 'IN' and Payment['total']['amount'] == 50 and Payment['comment'] == Uuid:
            return True
    return False

async def BuyPrime(ctx, client):
    uAuid = str(uuid.uuid4()).replace('-', '')
    def check(reaction, user):
        return user.id == ctx.author.id and reaction.message.id == msg.id
    em = discord.Embed(title="SandWorld Online Alpha", description=f"Pay at that url:\n{create_payment_link(uAuid)}", colour=0xf52c2c)
    em.set_footer(text='After finish click reaction.')
    msg = await ctx.author.send(embed=em)
    await msg.add_reaction("✔️")
    try:
        rea, use = await client.wait_for('reaction_add', check=check, timeout=120.0)
    except asyncio.TimeoutError:
        await msg.delete()
    if rea.emoji == '✔️':
        if CheckPay(uAuid) == True:
            other.update_one({'_id': 'PrimeTable'},  {'$push': {'PrimeArray': str(ctx.author.id)}})
            em = discord.Embed(title="SandWorld Online Alpha", description=f"✔️ thanks for buy!", colour=0x58eb2f)
            await msg.edit(embed=em)
        else:
            em = discord.Embed(title="SandWorld Online Alpha", description=f"❌ your transaction could not be found.", colour=0xf52c2c)
            await msg.edit(embed=em)
def IsPrime(UserId):
    DataBase = other.find_one({'_id': 'PrimeTable'})
    if str(UserId) in DataBase['PrimeArray']:
        return True
    else:
        return False
def GetPlayerArmor(UserId):
    return profiles.find_one({'_id': str(UserId)})['Armor']
def BanUser(UserId):
    other.update_one({'_id': 'BansTable'},  {'$push': {'BansArray': str(UserId)}})
def UnBanUser(UserId):
    other.update_one({'_id': 'BansTable'}, {'$pull': {'BansArray': str(UserId)}})
async def FightStart(ctx, client, EnemyHP, EnemyAttackMin, EnemyAttackMax, EnemyName):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    PlayerHP = 100
    StopBool = True
    em = discord.Embed(title="SandWorld Online Alpha", description=f"**{ctx.author.mention}** — **{EnemyName}**\n:heart: {str(PlayerHP)} vs :heart: {str(EnemyHP)}\nChoice by reaction.", colour=0xf52c2c)
    msg = await ctx.send(embed=em)
    await msg.add_reaction("⚔️")
    await msg.add_reaction("🛡️")
    def check(reaction, user):
        return user.id == ctx.author.id and reaction.message.id == msg.id
    while StopBool == True:
        if EnemyHP > 0 and PlayerHP > 0:
            try:
                rea, use = await client.wait_for('reaction_add', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                anv = discord.Embed(title="SandWorld Online Alpha", description=f":crossed_swords: {ctx.author.mention} Timeout.", colour=0xf52c2c)
                await msg.edit(embed=anv)
                await msg.clear_reactions()
                break
            if rea.emoji == '⚔️':
                DamageP = random.randint(4, 10 + DataBase[str(ctx.author.id)]["Item"]["AttackPlus"])
                if EnemyHP - DamageP < 0:
                    DamageP = EnemyHP 
                EnemyHP -= DamageP
                EnemyDamage = random.randint(EnemyAttackMin, EnemyAttackMax)
                if PlayerHP - EnemyDamage < 0:
                    EnemyDamage = PlayerHP
                PlayerHP -= EnemyDamage
                await msg.clear_reactions()
                await msg.add_reaction("⚔️")
                await msg.add_reaction("🛡️")
                anv = discord.Embed(title="SandWorld Online Alpha", description=f"**{ctx.author.mention}** — **{EnemyName}**\n:heart: {str(PlayerHP)} vs :heart: {str(EnemyHP)}\nChoice by reaction.", colour=0xf52c2c)
                await msg.edit(embed=anv)
            elif rea.emoji == '🛡️':
                PlayerBlock = random.randint(1, 4 + DataBase[str(ctx.author.id)]["Armor"]["BlockPlus"])
                EnemyAttack = random.randint(EnemyAttackMin, EnemyAttackMax)
                if EnemyAttack - PlayerBlock <= 0:
                    Heal = random.randint(1, 5)
                    if PlayerHP + Heal >= 100:
                        PlayerHP = 100
                    else:
                        PlayerHP += Heal
                else:
                    PlayerHP -= EnemyAttack 
                await msg.clear_reactions()
                await msg.add_reaction("⚔️")
                await msg.add_reaction("🛡️")
                anv = discord.Embed(title="SandWorld Online Alpha", description=f"**{ctx.author.mention}** — **{EnemyName}**\n:heart: {str(PlayerHP)} vs :heart: {str(EnemyHP)}\nChoice by reaction.", colour=0xf52c2c)
                await msg.edit(embed=anv)
            else:
                pass
        elif EnemyHP <= 0:
            anv = discord.Embed(title="SandWorld Online Alpha", description=f":crossed_swords: {ctx.author.mention} You win!", colour=0x58eb2f)
            await msg.edit(embed=anv)
            await msg.clear_reactions()
            return 1
        elif PlayerHP <= 0:
            anv = discord.Embed(title="SandWorld Online Alpha", description=f":crossed_swords: {ctx.author.mention} You lose.", colour=0xf52c2c)
            await msg.edit(embed=anv)
            await msg.clear_reactions()
            return 2
def IsAdmin(UserId):
    DataBase = other.find_one({'_id': 'AdminsTable'})
    if str(UserId) in DataBase["AdminsArray"]:
        return True
    else:
        return False
def GetBannedUsers():
    return other.find_one({'_id': 'BansTable'})
def AddAdmin(UserId):
    other.update_one({'_id': 'AdminsTable'},  {'$push': {'AdminsArray': str(UserId)}})
def IsProfileExist(UserId):
    Table = profiles.find_one({'_id': str(UserId)})
    if Table != None:
        return True
    else:
        return False
def WritePlayerData(UserId):
    if IsProfileExist(UserId):
        return False
    else:
        profiles.insert_one({"_id": str(UserId), "Balance": 0, "Armor": CreateArmor(0, "None"), "Item": CreateItem(0, 0, "None"), "Inventory": []})
        return True
def AddItemToShop(Name : str, Price : int, Item : dict, Emoji : str, Type : int):
    other.update_one({'_id': 'ShopTable'},  {'$push': {'ShopArray': {'Name': Name, 'Price': Price, 'Item': Item, 'reaction-emoji': Emoji, 'type': Type}}})
def Pay(UserId, TargerId, Value):
    User = profiles.find_one({"_id": str(UserId)})
    Target = profiles.find_one({"_id": str(TargerId)})
    if User["Balance"] >= Value:
        NewBalance = User["Balance"] - Value
        NewTargetBalance = Target["Balance"] + Value
        profiles.update_one({"_id": str(UserId)}, {'$set': {"Balance": NewBalance}})
        profiles.update_one({"_id": str(TargerId)}, {'$set': {"Balance": NewTargetBalance}})
        return 1
    else:
        return 2
def GetBalance(UserId):
    return profiles.find_one({"_id": str(UserId)})["Balance"]
def RemoveAdmin(UserId):
    other.update_one({'_id': 'AdminsTable'}, {'$pull': {'AdminsArray': str(UserId)}})
def AddSand(UserId, value):
    User = profiles.find_one({"_id": str(UserId)})
    NewBalance = User["Balance"] + int(value)
    profiles.update_one({"_id": str(UserId)}, {'$set': {"Balance": NewBalance}})
def RemoveSand(UserId, value):
    User = profiles.find_one({"_id": str(UserId)})
    NewBalance = User["Balance"] - value
    profiles.update_one({"_id": str(UserId)}, {'$set': {"Balance": NewBalance}})
def DigSand(UserId):
    value = 0
    BannedIds = GetBannedUsers()
    if not UserId in BannedIds["BansArray"]:
        Event = random.randint(1, 10)
        if Event != 6 and Event != 4:
            User = profiles.find_one({"_id": str(UserId)})
            value = random.randint(1 + User['Item']['SandFarmPlus'], 4 + User['Item']['SandFarmPlus'])
            NewBalance = User["Balance"] + value
            profiles.update_one({"_id": str(UserId)}, {'$set': {"Balance": NewBalance}})
        elif Event == 6:
            value = 90000
        elif Event == 4:
            value = 900001
    return value
