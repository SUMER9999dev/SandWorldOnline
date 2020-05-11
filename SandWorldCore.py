import json
import random
import discord
import requests
import asyncio
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
CoreVersion = "1.4.2"
DatabaseKey = os.environ.get("DatabaseKey")
def CreateArmor(ArmorPlus, ArmorName):
    return {"BlockPlus": ArmorPlus, "Name": ArmorName}
def CreateItem(SandFarmPlus, AttackPlus, Name):
    return {"AttackPlus": AttackPlus, "SandFarmPlus": SandFarmPlus, "Name": Name}
def BanUser(UserId):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/bans.txt").json()
    DataBase["BannedUsers"].append(UserId)
    requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=Bans&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
def UnBanUser(UserId):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/bans.txt").json()
    DataBase["BannedUsers"].remove(UserId)
    requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=Bans&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
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
                Block = random.randint(1, 4 + - DataBase[str(ctx.author.id)]["Armor"]["BlockPlus"])
                Heal = random.randint(1, 5)
                if EnemyAttackMax - Block > 0:
                    EnemyDamage = random.randint(EnemyAttackMin, EnemyAttackMax - Block)
                elif EnemyAttackMax - Block <= 0:
                    EnemyDamage = 0
                if PlayerHP - EnemyDamage < 0:
                    EnemyDamage = PlayerHP
                PlayerHP -= EnemyDamage
                if Heal + PlayerHP > 100:
                    pass
                else:
                    Heal + PlayerHP
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
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/admins.txt").json()
    if UserId in DataBase["AdminTable"]:
        return True
    else:
        return False
def GetBannedUsers():
    #with open("Data/Bans.json", "r") as f:
        #DataBase = json.load(f)
    return requests.get("https://sumer-database.000webhostapp.com/sandworldonline/bans.txt").json()
def AddAdmin(UserId):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/admins.txt").json()
    DataBase["AdminTable"].append(UserId)
    requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=Admins&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
def WritePlayerData(UserId):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    DataBase[str(UserId)] = {"Balance": 0, "shovel": False, "Armor": {"BlockPlus": 0, "Name": "None"}, "Item": {"AttackPlus": 0, "SandFarmPlus": 0, "Name": "None"}}
    requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=MainData&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
def IsProfileExist(UserId):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    if not str(UserId) in DataBase:
        return False
    else:
        return True
def BuyShovel(UserId):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    if IsProfileExist(UserId):
        if DataBase[str(UserId)]["shovel"] != True:
            if DataBase[str(UserId)]["Balance"] >= 30:
                DataBase[str(UserId)]["Balance"] -= 30
                DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"], "shovel": True, "Armor": DataBase[str(UserId)]["Armor"], "Item": DataBase[str(UserId)]["Item"]}
                requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=MainData&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
                return 1
            else:
                return 2
        else:
            return 3
    else:
        return 4
def BuyItem(UserId, Item, Price):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    if IsProfileExist(UserId):
        if DataBase[str(UserId)]["Item"] != Item:
                if DataBase[str(UserId)]["Balance"] >= Price:
                    DataBase[str(UserId)]["Balance"] -= Price
                    DataBase[str(UserId)]["Item"] = Item
                    requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=MainData&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
                    return 1
                else:
                    return 2
        else:
            return 3
    else:
        return 4
def BuyArmor(UserId, Armor, Price):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    if IsProfileExist(UserId):
        if DataBase[str(UserId)]["Armor"] != Armor:
                if DataBase[str(UserId)]["Balance"] >= Price:
                    DataBase[str(UserId)]["Balance"] -= Price
                    DataBase[str(UserId)]["Armor"] = Armor
                    requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=MainData&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
                    return 1
                else:
                    return 2
        else:
            return 3
    else:
        return 4
def Pay(UserId, TargerId, Value):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    if DataBase[str(UserId)]["Balance"] >= Value:
        DataBase[str(UserId)]["Balance"] -= Value
        DataBase[str(TargerId)]["Balance"] += Value
        requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=MainData&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
        return 1
    else:
        return 2
def GetBalance(UserId):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    return DataBase[str(UserId)]["Balance"]
def GetShovelExistEmoji(UserId):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    if DataBase[str(UserId)]["shovel"] == True:
        return ":white_check_mark:"
    else:
        return ":x:"
def RemoveAdmin(UserId):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/admins.txt").json()
    DataBase["AdminTable"].remove(UserId)
    requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=Admins&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
def AddSand(UserId, value):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"] + int(value), "shovel": DataBase[str(UserId)]["shovel"], "Armor": DataBase[str(UserId)]["Armor"], "Item": DataBase[str(UserId)]["Item"]}
    requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=MainData&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
def RemoveSand(UserId, value):
    DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
    DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"] -  int(value), "shovel": DataBase[str(UserId)]["shovel"], "Armor": DataBase[str(UserId)]["Armor"], "Item": DataBase[str(UserId)]["Item"]}
    requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=MainData&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
def DigSand(UserId):
    value = 0
    BannedIds = GetBannedUsers()
    if not UserId in BannedIds["BannedUsers"]:
        Event = random.randint(1, 10)
        if Event != 6:
            DataBase = requests.get("https://sumer-database.000webhostapp.com/sandworldonline/data.txt").json()
            if DataBase[str(UserId)]["shovel"] == True:
                value = random.randint(4, 10)
            else:
                value = random.randint(1, 4)
            DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"] + value, "shovel": DataBase[str(UserId)]["shovel"], "Armor": DataBase[str(UserId)]["Armor"], "Item": DataBase[str(UserId)]["Item"]}
            requests.get(f"https://sumer-database.000webhostapp.com/sandworldonline/writedata.php?DataType=MainData&key={DatabaseKey}&NewData={json.dumps(DataBase)}")
        else:
            value = 90000
    return value
