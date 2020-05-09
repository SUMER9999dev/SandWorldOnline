import json
import random
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
CoreVersion = "1.2.1"
def BanUser(UserId):
    with open("Data/Bans.json", "r") as f:
        DataBase = json.load(f)
    DataBase["BannedUsers"].append(UserId)
    with open("Data/Bans.json", "w") as r:
        json.dump(DataBase, r)
def UnBanUser(UserId):
    with open("Data/Bans.json", "r") as f:
        DataBase = json.load(f)
    DataBase["BannedUsers"].remove(UserId)
    with open("Data/Bans.json", "w") as r:
        json.dump(DataBase, r)
async def FightStart(ctx, client, EnemyHP, EnemyAttackMin, EnemyAttackMax, EnemyName):
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
                DamageP = random.randint(4, 10)
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
                Block = random.randint(1, 4)
                Heal = random.randint(1, 5)
                EnemyDamage = random.randint(EnemyAttackMin, EnemyAttackMax - Block)
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
    with open("Data/Admins.json", "r") as f:
        DataBase = json.load(f)
    if UserId in DataBase["AdminTable"]:
        return True
    else:
        return False
def GetBannedUsers():
    with open("Data/Bans.json", "r") as f:
        DataBase = json.load(f)
    return DataBase["BannedUsers"]
def AddAdmin(UserId):
    with open("Data/Admins.json", "r") as f:
        DataBase = json.load(f)
    DataBase["AdminTable"].append(UserId)
    with open("Data/Admins.json", "w") as r:
        json.dump(DataBase, r)
def WritePlayerData(UserId):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    DataBase[str(UserId)] = {"Balance": 0, "shovel": False}
    with open("Data/DataBase.json", "w") as r:
        json.dump(DataBase, r)
def IsProfileExist(UserId):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    if not str(UserId) in DataBase:
        return False
    else:
        return True
def BuyShovel(UserId):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    if IsProfileExist(UserId):
        if DataBase[str(UserId)]["shovel"] != True:
            if DataBase[str(UserId)]["Balance"] >= 30:
                DataBase[str(UserId)]["Balance"] -= 30
                DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"], "shovel": True}
                with open("Data/DataBase.json", "w") as r:
                    json.dump(DataBase, r)
                return 1
            else:
                return 2
        else:
            return 3
    else:
        return 4
def Pay(UserId, TargerId, Value):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    if DataBase[str(UserId)]["Balance"] >= Value:
        DataBase[str(UserId)]["Balance"] -= Value
        DataBase[str(TargerId)]["Balance"] += Value
        with open("Data/DataBase.json", "w") as r:
            json.dump(DataBase, r)
        return 1
    else:
        return 2
def GetBalance(UserId):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    return DataBase[str(UserId)]["Balance"]
def GetShovelExistEmoji(UserId):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    if DataBase[str(UserId)]["shovel"] == True:
        return ":white_check_mark:"
    else:
        return ":x:"
def RemoveAdmin(UserId):
    with open("Data/Admins.json", "r") as f:
        DataBase = json.load(f)
    DataBase["AdminTable"].remove(UserId)
    with open("Data/Admins.json", "w") as r:
        json.dump(DataBase, r)
def AddSand(UserId, value):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"] + int(value), "shovel": DataBase[str(UserId)]["shovel"]}
    with open("Data/DataBase.json", "w") as r:
        json.dump(DataBase, r)
def RemoveSand(UserId, value):
    with open("Data/DataBase.json", "r") as f:
        DataBase = json.load(f)
    DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"] -  int(value), "shovel": DataBase[str(UserId)]["shovel"]}
    with open("Data/DataBase.json", "w") as r:
        json.dump(DataBase, r)
def DigSand(UserId):
    value = 0
    BannedIds = GetBannedUsers()
    if not UserId in BannedIds:
        Event = random.randint(1, 10)
        if Event != 6:
            with open("Data/DataBase.json", "r") as f:
                DataBase = json.load(f)
            if DataBase[str(UserId)]["shovel"] == True:
                value = random.randint(4, 10)
            else:
                value = random.randint(1, 4)
            DataBase[str(UserId)] = {"Balance": DataBase[str(UserId)]["Balance"] + value, "shovel": DataBase[str(UserId)]["shovel"]}
            with open("Data/DataBase.json", "w") as r:
                json.dump(DataBase, r)
        else:
            value = 90000
    return value
