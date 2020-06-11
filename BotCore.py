import discord
import SandWorldCore
import random
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
import os
client = commands.Bot(command_prefix = "sw!")
client.remove_command("help")
BotCoreVer = "1.6.5"
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="sw!help"))
    print("bot ready")
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(embed=discord.Embed(title="SandWorld Online Alpha", description=':warning: Command not found.\nType sw!help for get command list.', colour=0xffdd00))
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(title="SandWorld Online Alpha", description=':warning: Argument Error.\nType sw!help for get Argument list.', colour=0xffdd00))
@client.command(name="shop", aliases=["Shop", "Market", "market"], description="Just shop.")
async def SHOPPPPP(ctx):
    if SandWorldCore.IsProfileExist(ctx.author.id):
        Text = "**🛒SHOP**\n"
        for index, ShopItem in enumerate(SandWorldCore.other.find_one({'_id': 'ShopTable'})['ShopArray']):
            Text += f"{ShopItem['reaction-emoji']}{str(ShopItem['Name'])} - {str(ShopItem['Price'])} sand\n"
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=Text, colour=0x337cc4)
        em.set_footer(text="for buy click reaction")
        msg = await ctx.send(embed=em)
        EmojieExist = []
        for index, ShopItem in enumerate(SandWorldCore.other.find_one({'_id': 'ShopTable'})['ShopArray']):
            await msg.add_reaction(ShopItem['reaction-emoji'])
            EmojieExist.append(ShopItem['reaction-emoji'])
        def check(reaction, user):
            return user.id == ctx.author.id and reaction.message.id == msg.id
        try:
            rea, use = await client.wait_for('reaction_add', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await msg.delete()
        if rea.emoji in EmojieExist:
            for index, ShopItem in enumerate(SandWorldCore.other.find_one({'_id': 'ShopTable'})['ShopArray']):
                if rea.emoji == ShopItem['reaction-emoji']:
                    User = SandWorldCore.profiles.find_one({"_id": str(ctx.author.id)})
                    if ShopItem['type'] == 1:
                        if User["Balance"] >= ShopItem['Price']:
                            if User["Item"]["Name"] != ShopItem['Item']['Name'] and not ShopItem['Item'] in User['Inventory']:
                                NewBalance = User["Balance"] - ShopItem['Price']
                                if User["Item"]["Name"] != "None":
                                    SandWorldCore.profiles.update_one({'_id': str(ctx.author.id)},  {'$push': {'Inventory': User["Item"]}})
                                SandWorldCore.profiles.update_one({"_id": str(ctx.author.id)}, {'$set': {"Balance": NewBalance, "Item": ShopItem['Item']}})
                                em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":white_check_mark: Thanks for buy!", colour=0x31ab20)
                                await msg.edit(embed=em)
                            else:
                                em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":warning: You already have {ShopItem['Item']['Name']}.", colour=0xffdd00)
                                await msg.edit(embed=em)
                        else:
                            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":x: Insufficient balance.", colour=0xd11f1f)
                            await msg.edit(embed=em)
                    else:
                        if User["Balance"] >= ShopItem['Price']:
                            if User["Armor"]["Name"] != ShopItem['Item']['Name'] and not ShopItem['Item'] in User['Inventory']:
                                NewBalance = User["Balance"] - ShopItem['Price']
                                if User["Armor"]["Name"] != "None":
                                    SandWorldCore.profiles.update_one({'_id': str(ctx.author.id)},  {'$push': {'Inventory': User["Armor"]}})
                                SandWorldCore.profiles.update_one({"_id": str(ctx.author.id)}, {'$set': {"Balance": NewBalance, "Armor": ShopItem['Item']}})
                                em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":white_check_mark: Thanks for buy!", colour=0x31ab20)
                                await msg.edit(embed=em)
                            else:
                                em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":warning: You already have {ShopItem['Item']['Name']}.", colour=0xffdd00)
                                await msg.edit(embed=em)
                        else:
                            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":x: Insufficient balance.", colour=0xd11f1f)
                            await msg.edit(embed=em)
                    await msg.clear_reactions()
                    break
        else:
            pass
    else:
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
        await msg.edit(embed=em)
@client.command(name="AlmietPyramid", description="Infinity fight.")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def FIGHTFIGHTFIGHT(ctx):
    if SandWorldCore.IsProfileExist(ctx.author.id):
        Wins = 0
        AlmietHP = 150
        AlmietMinDamage = 1
        AlmietMaxDamage =  8
        while Wins < 15:
            TheWar = await SandWorldCore.FightStart(ctx, client, AlmietHP, AlmietMinDamage, AlmietMaxDamage, "Almiet Guardian")
            if TheWar == 1:
                Wins += 1
                AlmietHP += 10
                AlmietMaxDamage += 1
                AlmietMinDamage += 1
            else:
                break
        SandGet = random.randint(10 * Wins, 20 * Wins)
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":island: You lost and get {str(SandGet)} sand!", colour=0x8ceb07)
        await ctx.send(embed=em)
        SandWorldCore.AddSand(ctx.author.id, SandGet)
    else:
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
        await ctx.send(embed=em)
@FIGHTFIGHTFIGHT.error
async def FIGHTFIGHTFIGHTERROR(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: This command can only be used once every 24 hours! Try again after {} seconds.".format(round(error.retry_after)), colour=0xffdd00)
        await ctx.send(embed=em)
@client.command(hidden=True, name="AddItem")
async def ADDITEM(ctx, Price : int, Emoji, Type : int, AttackPlus : int = None, SandFarmPlus : int = None, BlockPlus : int = None, *, Name):
    if ctx.author.id == 714881781408727189:
        if Type == 1:
            SandWorldCore.AddItemToShop(Name, Price, SandWorldCore.CreateItem(SandFarmPlus, AttackPlus, Name), Emoji, Type)
        else:
            SandWorldCore.AddItemToShop(Name, Price, SandWorldCore.CreateArmor(BlockPlus, Name), Emoji, Type)
    else:
        pass
@client.command(name="Equip", aliases=["equip"], description="You can equip item.")
async def EquipITEM(ctx):
    if SandWorldCore.IsProfileExist(ctx.author.id):
        User = SandWorldCore.profiles.find_one({"_id": str(ctx.author.id)})
        if User["Inventory"] != []:
            IndexTable = {}
            Message = "🎒Inventory:\n"
            Index = 0
            for InventoryMember in User["Inventory"]:
                Index += 1
                Message = Message + "``" + str(Index) + "``" + " — " + InventoryMember["Name"] + "\n"
                IndexTable[str(Index)] = InventoryMember
            TheEmbed = discord.Embed(title="SandWorld Online Alpha", type="rich", description=Message, colour=0x8ceb07)
            msg = await ctx.send(embed=TheEmbed)
            def check(message):
                return message.channel == msg.channel and message.author.id == ctx.author.id
            try:
                AuthorMessage = await client.wait_for('message', check=check)
            except asyncio.TimeoutError:
                await msg.delete()
            if AuthorMessage.content in IndexTable:
                if "AttackPlus" in IndexTable[AuthorMessage.content]:
                    if User["Item"]["Name"] == "None":
                        pass
                    else:
                        SandWorldCore.profiles.update_one({'_id': str(ctx.author.id)},  {'$push': {'Inventory': User["Item"]}})
                    SandWorldCore.profiles.update_one({"_id": str(ctx.author.id)}, {'$set': {"Item": IndexTable[AuthorMessage.content]}})
                else:
                    if User["Armor"]["Name"] == "None":
                        pass
                    else:
                        SandWorldCore.profiles.update_one({'_id': str(ctx.author.id)},  {'$push': {'Inventory': User["Armor"]}})
                    SandWorldCore.profiles.update_one({"_id": str(ctx.author.id)}, {'$set': {"Armor": IndexTable[AuthorMessage.content]}})
                SandWorldCore.profiles.update_one({'_id': str(ctx.author.id)}, {'$pull': {'Inventory': IndexTable[AuthorMessage.content]}})
                em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":white_check_mark: Successfully equipped!", colour=0x31ab20)
                await ctx.send(embed=em)
                IndexTable.clear()
            else:
                em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":warning: Invalid item index.", colour=0xffdd00)
                await ctx.send(embed=em)
                IndexTable.clear()
        else:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":warning: You're inventory is empty.", colour=0xffdd00)
            await ctx.send(embed=em)
    else:
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
        await ctx.send(embed=em)
@client.command(name="info", description = "info about game.")
async def InfoCmd(ctx):
    SandWorldCoreVer = SandWorldCore.CoreVersion
    em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":robot: Bot core version - {BotCoreVer}\n:cloud_tornado: SandWorld core version - {SandWorldCoreVer}", colour=0x8ceb07)
    await ctx.send(embed=em)
@client.command(name="Pay", aliases=["pay"], description = "Pay some user Pay <User ping> <Value>.")
async def PayCmd(ctx, member : discord.Member, Value : int):
    if Value >= 1:
        if SandWorldCore.IsProfileExist(ctx.author.id):
            if SandWorldCore.IsProfileExist(member.id):
                request = SandWorldCore.Pay(ctx.author.id, member.id, Value)
                if request == 1:
                    em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":white_check_mark: Successfully pay!", colour=0x31ab20)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":x: Insufficient balance.", colour=0xd11f1f)
                    await ctx.send(embed=em)
            else:
                em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":warning: {member.mention} need sw!RegProfile before do that!", colour=0xffdd00)
                await ctx.send(embed=em)
        else:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
            await ctx.send(embed=em)
    else:
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":warning: You can't send less than one sand!", colour=0xffdd00)
        await ctx.send(embed=em)
@client.command(
    name = "help",
    aliases = ["команды", "comms", "commands", "помощь"],
    description = "That message."
)
async def help(ctx):
    comm_list = []
    for command in client.commands:
        if not command.hidden:
            comm_list.append(f"`sw!{command}` — {command.description}\n")
    embed = discord.Embed(
        title = "SandWorld Online Alpha",
        description = "".join(comm_list),
        color = 0x8ceb07)
    embed.set_footer(text = f"author {ctx.author}", icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)
@client.command(hidden=True, name="AdminHelp")
async def Hidden6(ctx):
    if SandWorldCore.IsAdmin(ctx.author.id):
        embed = discord.Embed(title = "SandWorld Online Alpha", description = "sw!Ban <упоминания человека>\nsw!UnBan <упоминания человека>\nsw!AddSand <упоминания человека> <кол-во>\nsw!RemoveSand <упоминания человека> <кол-во>", color = 0x8ceb07)
        await ctx.send(embed=embed)
    else:
        pass
@client.command(name="RegProfile", aliases=["reg", "register", "regprofile", "Reg", "Register"], description = "Profile creating.")
async def Reg(ctx):
    ProfileId = ctx.author.id
    if SandWorldCore.IsProfileExist(ProfileId):
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You already have account.", colour=0xffdd00)
        await ctx.send(embed=em)
    else:
        SandWorldCore.WritePlayerData(ProfileId)
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":white_check_mark: Account has been created!", colour=0x8ceb07)
        await ctx.send(embed=em)
@client.command(name="Profile", aliases=["profile", "balance", "Balance"], description = "You're profile info.")
async def Profile(ctx, member : discord.Member = None):
    if member == None:
        ProfileId = ctx.author.id
        if SandWorldCore.IsProfileExist(ProfileId):
            Balance = str(SandWorldCore.GetBalance(ProfileId))
            ItemName = SandWorldCore.GetPlayerItem(ctx.author.id)["Name"]
            ArmorName = SandWorldCore.GetPlayerArmor(ctx.author.id)["Name"]
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":island: — {Balance}\nItem — {ItemName}\nArmor — {ArmorName}", colour=0x8ceb07)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
            await ctx.send(embed=em)
    else:
        ProfileId = member.id
        if SandWorldCore.IsProfileExist(ProfileId):
            Name = member.mention
            Balance = str(SandWorldCore.GetBalance(ProfileId))
            ItemName = SandWorldCore.GetPlayerItem(ProfileId)["Name"]
            ArmorName = SandWorldCore.GetPlayerArmor(ProfileId)["Name"]
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{Name}'s profile\n:island: - {Balance}\nItem — {ItemName}\nArmor — {ArmorName}", colour=0x8ceb07)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You need do sw!RegProfile before do that!", colour=0xffdd00)
            await ctx.send(embed=em)
@client.command(hidden = True, name="GiveAdmin")
async def Hidden1(ctx, member : discord.Member):
    if ctx.author.id != 714881781408727189:
        pass
    else:
        SandWorldCore.AddAdmin(member.id)
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{member.mention} now admin!", colour=0x8ceb07)
        await ctx.send(embed=em)
@client.command(hidden = True, name="IsAdmin")
async def Hidden8333(ctx, member : discord.Member):
    if ctx.author.id != 714881781408727189:
        pass
    else:
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{SandWorldCore.IsAdmin(ctx.author.id)}", colour=0x8ceb07)
        await ctx.send(embed=em)
@client.command(hidden = True, name="RemoveAdmin")
async def Hidden8(ctx, member : discord.Member):
    if ctx.author.id != 714881781408727189:
        pass
    else:
        if SandWorldCore.IsAdmin(member.id):
            SandWorldCore.RemoveAdmin(member.id)
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{member.mention} no longer admin.", colour=0x8ceb07)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{member.mention} not admin.", colour=0x8ceb07)
            await ctx.send(embed=em) 
@client.command(hidden=True, name="Ban")
async def Hidden2(ctx, member : discord.Member):
    if SandWorldCore.IsAdmin(ctx.author.id):
        SandWorldCore.BanUser(member.id)
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{member.mention} has been banned.", colour=0x8ceb07)
        await ctx.send(embed=em)
    else:
        pass
@client.command(hidden=True, name="UnBan")
async def Hidden3(ctx, member : discord.Member):
    if SandWorldCore.IsAdmin(ctx.author.id):
        SandWorldCore.UnBanUser(member.id)
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{member.mention} has been unbanned.", colour=0x8ceb07)
        await ctx.send(embed=em)
    else:
        pass
@client.command(hidden=True, name="AddSand")
async def Hidden4(ctx, member : discord.Member, value):
    if SandWorldCore.IsAdmin(ctx.author.id):
        if SandWorldCore.IsProfileExist(member.id):
            SandWorldCore.AddSand(member.id, value)
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{member.mention} get {str(value)} sand!", colour=0x8ceb07)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: That member dont have profile.", colour=0xffdd00)
            await ctx.send(embed=em)
    else:
        pass
@client.command(hidden=True, name="RemoveSand")
async def Hidden5(ctx, member : discord.Member, value):
    if SandWorldCore.IsAdmin(ctx.author.id):
        if SandWorldCore.IsProfileExist(member.id):
            SandWorldCore.RemoveSand(member.id, value)
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{member.mention} lost {str(value)} sand.", colour=0x8ceb07)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: That member dont have profile.", colour=0xffdd00)
            await ctx.send(embed=em)
    else:
        pass
@client.command(name="PrimeReward", aliases=["primereward"], description="Get daily send.")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def PrimeReward(ctx):
    if SandWorldCore.IsPrime(ctx.author.id):
        Dig = SandWorldCore.random.randint(40, 80)
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":island: {ctx.author.mention} you're reward {str(Dig)} sand!", colour=0x8ceb07)
        await ctx.send(embed=em)
        SandWorldCore.AddSand(ctx.author.id, Dig)
    else:
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You need buy prime before do that!", colour=0xffdd00)
        await ctx.send(embed=em)
@client.command(name="BuyPrime", aliases=["Prime", "prime", "buyprime"], description="Buy prime.")
async def BuyingShit(ctx):
    if SandWorldCore.IsProfileExist(ctx.author.id):
        if SandWorldCore.IsPrime(ctx.author.id):
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You already have prime.", colour=0xffdd00)
            await ctx.send(embed=em)
        else:
            await ctx.send("check you're DM's.")
            await SandWorldCore.BuyPrime(ctx, client)
    else:
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
        await ctx.send(embed=em)
@PrimeReward.error
async def PrimeRewardError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: This command can only be used once every 24 hours! Try again after {} seconds.".format(round(error.retry_after)), colour=0xffdd00)
        await ctx.send(embed=em)
@client.command(name="DigSand", aliases=["digsand", "GetSand", "getsand", "FarmSand", "farmsand"], description = "Get sand.")
@commands.cooldown(1, 20, commands.BucketType.user)
async def Dig(ctx):
    ProfileId = ctx.author.id
    if SandWorldCore.IsProfileExist(ProfileId):
        Dig = SandWorldCore.DigSand(ProfileId)
        if Dig != 90000 and Dig != 900001:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":island: {ctx.author.mention} you get {str(Dig)} sand!", colour=0x8ceb07)
            await ctx.send(embed=em)
        elif Dig == 90000:
            TheFight = await SandWorldCore.FightStart(ctx, client, 70, 4, 14, "Sand Elemental")
            if TheFight == 1:
                Sand = random.randint(10, 20)
                SandWorldCore.AddSand(ProfileId, Sand)
                em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":island: {ctx.author.mention} you get {str(Sand)} sand!", colour=0x8ceb07)
                await ctx.send(embed=em)
            else:
                pass
        elif Dig == 900001:
            TheFight = await SandWorldCore.FightStart(ctx, client, 250, 19, 40, "Lost almiet")
            if TheFight == 1:
                Sand = random.randint(20, 50)
                SandWorldCore.AddSand(ProfileId, Sand)
                em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":island: {ctx.author.mention} you get {str(Sand)} sand!", colour=0x8ceb07)
                await ctx.send(embed=em)
            else:
                pass  
    else:
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
        await ctx.send(embed=em)
@Dig.error
async def DigError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: This command can only be used once every 20 seconds! Try again after {} seconds.".format(round(error.retry_after)), colour=0xffdd00)
        await ctx.send(embed=em)
client.run('Token here')
