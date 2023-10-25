import random

from discord.ext import commands
import discord
import datetime

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents=intents # Set up basic permissions
)

bot.author_id = 182718229272199168  # Change to your discord id
flod = [False]
users = []
limit = 5

def find(user):
    for i in range(len(users)):
        u, _ = users[i]
        if u == user:
            return i
    return -1

def check_time(messages):
    spam = True
    for i in range(len(messages)-1):
        spam = messages[i + 1].created_at.timestamp() - messages[i].created_at.timestamp() <= limit and spam

    return spam


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.event
async def on_message(ctx):
    if flod[0]:
        i = find(ctx.author)
        if i >= 0:
            _, m = users[i]
            m.append(ctx)
        else:
            users.append((ctx.author, [ctx]))
            i = -1

        user, messages = users[i]
        if len(messages) >= limit:
            if check_time(messages):
                await ctx.reply("You dare to spam here")
            messages.pop(0)

    if "Salut tout le monde" == ctx.clean_content:
        await ctx.reply("Salut tout seul " + ctx.author.mention)
    await bot.process_commands(ctx)


@bot.command()
async def pong(ctx):
    await ctx.send('pong')


@bot.command()
async def name(ctx):
    await ctx.send(ctx.message.author.name)


@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1, 6))


@bot.command()
async def admin(ctx, member:discord.Member):
    roles = await ctx.guild.fetch_roles()
    adin = None
    for i in roles:
        if i.name == "Admin":
            adin = i
            break
    if not adin:
        perm = discord.Permissions(0x8)
        adin = await ctx.guild.create_role(name="Admin", permissions=perm, colour=discord.colour.Colour.blurple())

    await member.add_roles(adin)


@bot.command()
async def ban(ctx, member:discord.Member, reason="You, stupid!"):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.guild.ban(member, reason=reason)


@bot.command()
async def flood(ctx):
    flod[0] = not flod[0]
    if flod[0]:
        await ctx.send("Anti Flood activated")
    else:
        await ctx.send("Anti Flood remove")


token = ""
bot.run(token)  # Starts the bot