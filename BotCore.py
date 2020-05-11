import discord
import SandWorldCore
import random
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
import os
client = commands.Bot(command_prefix = "sw!")
client.remove_command("help")
BotCoreVer = "1.1.3"
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="sw!help"))
    print("bot ready")
#@client.event
#async def on_command_error(ctx, error):
    #if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        #await ctx.send(embed=discord.Embed(title="SandWorld Online Alpha", description=':warning: Command not found.\nType sw!help for get command list.', colour=0xffdd00))
    #if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        #await ctx.send(embed=discord.Embed(title="SandWorld Online Alpha", description=':warning: Argument Error.\nType sw!help for get Argument list.', colour=0xffdd00))
@client.command(name="Shop", description = "buy some item.")
async def shopcmd(ctx):
    em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"**🛒SHOP**\n⛏️ Shovel - 30 sand\n🗡️Rusty sword - 100 sand\n🦾Old armor - 120 sand", colour=0x337cc4)
    em.set_footer(text="for buy click reaction")
    msg = await ctx.send(embed=em)
    await msg.add_reaction("⛏️")
    await msg.add_reaction("🗡️")
    await msg.add_reaction("🦾")
    def check(reaction, user):
        return user.id == ctx.author.id and reaction.message.id == msg.id
    try:
        rea, use = await client.wait_for('reaction_add', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await msg.delete()
    if rea.emoji == "⛏️":
        shovel = SandWorldCore.BuyShovel(ctx.author.id)
        if shovel == 1:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":white_check_mark: Thanks for buy!", colour=0x31ab20)
            await msg.edit(embed=em)
        elif shovel == 2:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":x: Insufficient balance.", colour=0xd11f1f)
            await msg.edit(embed=em)
        elif shovel == 3:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You already have shovel.", colour=0xffdd00)
            await msg.edit(embed=em)
        elif shovel == 4:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
            await msg.edit(embed=em)
        await msg.clear_reactions()
    elif rea.emoji == "🗡️":
        TheSword = SandWorldCore.CreateItem(0, 7, "Rusty sword")
        Sword = SandWorldCore.BuyItem(ctx.author.id, TheSword, 100)
        if Sword == 1:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":white_check_mark: Thanks for buy!", colour=0x31ab20)
            await msg.edit(embed=em)
        elif Sword == 2:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":x: Insufficient balance.", colour=0xd11f1f)
            await msg.edit(embed=em)
        elif Sword == 3:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You already have rusty sword.", colour=0xffdd00)
            await msg.edit(embed=em)
        elif Sword == 4:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
            await msg.edit(embed=em)
        await msg.clear_reactions()
    elif rea.emoji == "🦾":
        TheArmor = SandWorldCore.CreateArmor(5, "Old armor")
        Armor = SandWorldCore.BuyArmor(ctx.author.id, TheArmor, 120)
        if Sword == 1:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":white_check_mark: Thanks for buy!", colour=0x31ab20)
            await msg.edit(embed=em)
        elif Sword == 2:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":x: Insufficient balance.", colour=0xd11f1f)
            await msg.edit(embed=em)
        elif Sword == 3:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You already have old armor.", colour=0xffdd00)
            await msg.edit(embed=em)
        elif Sword == 4:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
            await msg.edit(embed=em)
        await msg.clear_reactions()
    else:
        pass
@client.command(name="info", description = "info about game.")
async def InfoCmd(ctx):
    SandWorldCoreVer = SandWorldCore.CoreVersion
    em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":robot: Bot core version - {BotCoreVer}\n:cloud_tornado: SandWorld core version - {SandWorldCoreVer}", colour=0x8ceb07)
    await ctx.send(embed=em)
@client.command(name="Pay", description = "Pay some user Pay <User ping> <Value>.")
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
    name = "помощь",
    aliases = ["команды", "comms", "commands", "help"],
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
@client.command(name="RegProfile", description = "Profile creating.")
async def Reg(ctx):
    ProfileId = ctx.author.id
    if SandWorldCore.IsProfileExist(ProfileId):
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You already have account.", colour=0xffdd00)
        await ctx.send(embed=em)
    else:
        SandWorldCore.WritePlayerData(ProfileId)
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":white_check_mark: Account has been created!", colour=0x8ceb07)
        await ctx.send(embed=em)
@client.command(name="Profile", description = "You're profile info.")
async def Profile(ctx, member : discord.Member = None):
    if member == None:
        ProfileId = ctx.author.id
        if SandWorldCore.IsProfileExist(ProfileId):
            Balance = str(SandWorldCore.GetBalance(ProfileId))
            Shovel = SandWorldCore.GetShovelExistEmoji(ProfileId)
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":island: - {Balance}\n⛏️shovel - {Shovel}", colour=0x8ceb07)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: You need sw!RegProfile before do that!", colour=0xffdd00)
            await ctx.send(embed=em)
    else:
        ProfileId = member.id
        if SandWorldCore.IsProfileExist(ProfileId):
            Name = member.mention
            Balance = str(SandWorldCore.GetBalance(ProfileId))
            Shovel = SandWorldCore.GetShovelExistEmoji(ProfileId)
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{Name}'s profile\n:island: - {Balance}\n⛏️shovel - {Shovel}", colour=0x8ceb07)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: That member dont have profile!", colour=0xffdd00)
            await ctx.send(embed=em)
@client.command(hidden = True, name="GiveAdmin")
async def Hidden1(ctx, member : discord.Member):
    if ctx.author.id != 414039381398257704:
        pass
    else:
        SandWorldCore.AddAdmin(member.id)
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{member.mention} now admin!", colour=0x8ceb07)
        await ctx.send(embed=em)
@client.command(hidden = True, name="RemoveAdmin")
async def Hidden8(ctx, member : discord.Member):
    if ctx.author.id != 414039381398257704:
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
        SandWorldCore.AddSand(member.id, value)
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{member.mention} get {str(value)} sand!", colour=0x8ceb07)
        await ctx.send(embed=em)
    else:
        pass
@client.command(hidden=True, name="RemoveSand")
async def Hidden5(ctx, member : discord.Member, value):
    if SandWorldCore.IsAdmin(ctx.author.id):
        SandWorldCore.RemoveSand(member.id, value)
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f"{member.mention} lost {str(value)} sand.", colour=0x8ceb07)
        await ctx.send(embed=em)
    else:
        pass
@client.command(name="DigSand", description = "Get sand.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def Dig(ctx):
    ProfileId = ctx.author.id
    if SandWorldCore.IsProfileExist(ProfileId):
        Dig = SandWorldCore.DigSand(ProfileId)
        if Dig != 90000:
            em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=f":island: {ctx.author.mention} you get {str(Dig)} sand!", colour=0x8ceb07)
            await ctx.send(embed=em)
        else:
            TheFight = await SandWorldCore.FightStart(ctx, client, 70, 4, 14, "Sand Elemental")
            if TheFight == 1:
                Sand = random.randint(10, 20)
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
        em = discord.Embed(title="SandWorld Online Alpha", type="rich", description=":warning: This command can only be used once every 20 seconds!", colour=0xffdd00)
        await ctx.send(embed=em)
token = os.environ.get("BOT_TOKEN")
client.run(token)
