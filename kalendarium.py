import discord
from datetime import date
from discord.ext import tasks, commands
import requests
from urllib.parse import quote
import random

# import os

botVersion = "1.0"
botAuthorName = "𝓪𝓵𝓪𝓷𝓮𝔃𝔂#8315"
botAuthorID = "305309443921412116"
botAuthorIDnum = 305309443921412116
token = "TOKEN"
client = commands.Bot(command_prefix=">>")
client.remove_command('help')
jsonLink = "https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/" + date.today().strftime(
    "%#m") + "/" + date.today().strftime("%#d") + ".json"
req = requests.get(url=jsonLink)
odp = (
    "tak", "nie", "wydaje mi się, że tak", "wydaje mi się, że nie", "zwykle nie", "zwykle tak",
    "świetny pomysł!", "oczywiście, że nie", "oczywiście, że tak", "może", "nie wiem")


@client.event
async def on_ready():
    print("Bot jest gotowy!")
    loop.start()
    await client.change_presence(activity=discord.Game(name="essa byku! (>>help)"))


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Dziękuję za dodanie do serwera, nazywam się Kalendarium :)')
            helpmsg = discord.Embed(
                title="Pomoc",
                colour=discord.Colour.red()
            )
            helpmsg.add_field(name=">>dzisiaj", value="Pokazuje dzisiejsze nietypowe święta", inline=False)
            helpmsg.add_field(name=">>autor", value="Pokazuje autora bota")
            await channel.send(embed=helpmsg)
        break


@tasks.loop(minutes=5.0)
async def loop():
    global req, jsonLink
    jsonLink = "https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/" + date.today().strftime(
        "%#m") + "/" + date.today().strftime("%#d") + ".json"
    req = requests.get(url=jsonLink)
    # print(req.json())


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        helpmsg = discord.Embed(
            title="Pomoc",
            colour=discord.Colour.red()
        )
        helpmsg.add_field(name=">>dzisiaj", value="Pokazuje dzisiejsze nietypowe święta", inline=False)
        helpmsg.add_field(name=">>autor", value="Pokazuje autora bota", inline=False)
        helpmsg.add_field(name=">>8ball <pytanie>", value="Losuje odpowiedź w stylu TAK/NIE", inline=False)
        helpmsg.add_field(name=">>ile <pytanie>", value="Losuje liczbę 0-20", inline=False)
        helpmsg.add_field(name=">>howgay <osoba>", value="Test na bycie gejem (0-100%)", inline=False)
        await ctx.send(embed=helpmsg)
    else:
        await ctx.send("Wystąpił błąd podczas działania bota, zgłoś to do autora: <@" + botAuthorID + ">")
        print(error)


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, args):
    # pyt1 = (' '.join(args))
    odp1 = random.choice(odp)
    pyt1 = args
    embed = discord.Embed(
        title="8ball",
        colour=discord.Colour.green()
    )
    embed.set_footer(text="Kalendarium " + botVersion + " by " + botAuthorName)
    embed.add_field(name="Pytanie od " + str(ctx.message.author), value=pyt1, inline=False)
    embed.add_field(name="Odpowiedź:", value=odp1, inline=False)
    # await client.delete_message(ctx.message)
    await ctx.message.delete()
    await ctx.send(embed=embed)


@client.command()
async def ile(ctx, *args):
    pyt1 = (' '.join(args))
    odp1 = random.randint(0, 20)
    embed = discord.Embed(
        title="Ile?",
        colour=discord.Colour.green()
    )
    embed.set_footer(text="Kalendarium " + botVersion + " by " + botAuthorName)
    embed.add_field(name="Pytanie od " + str(ctx.message.author), value="Ile " + pyt1, inline=False)
    embed.add_field(name="Odpowiedź:", value=str(odp1), inline=False)
    await ctx.message.delete()
    await ctx.send(embed=embed)


@client.command()
async def howgay(ctx, *args):
    pyt1 = ' '.join(args)
    odp1 = random.randint(0, 100)
    embed = discord.Embed(
        title="Jak bardzo jest gejem?",
        colour=discord.Colour.red()
    )
    embed.set_footer(text="Kalendarium " + botVersion + " by " + botAuthorName)
    embed.add_field(name="Kto:", value=pyt1, inline=False)
    embed.add_field(name="Odpowiedź:", value=str(odp1) + "%", inline=False)
    await ctx.message.delete()
    await ctx.send(embed=embed)


@client.command()
async def dzisiaj(ctx):
    embed = discord.Embed(
        title="Kalendarz Świąt Nietypowych",
        colour=discord.Colour.orange()
    )
    embed.set_footer(text="Kalendarium " + botVersion + " by " + botAuthorName)
    embed.set_author(name="Data: " + str(date.today().strftime("%d/%m/%Y")), icon_url='https://i.imgur.com/vclVfjH.png')
    for key in req.json():
        embed.add_field(name=key['name'],
                        value="[Więcej informacji](https://google.com/search?q=" + quote(key['name']) + ")",
                        inline=False)

    await ctx.send(embed=embed)


@client.command()
async def autor(ctx):
    await ctx.send("Autorem Kalendarium " + botVersion + " jest: <@" + botAuthorID + ">")


@client.event
async def on_message(message):
    if message.content.lower().startswith("-p"):
        await message.delete()
        return
    if message.content.lower().startswith(">>"):
        await client.process_commands(message)
        return
    else:
        user = await client.fetch_user(botAuthorIDnum)
        user2 = await client.fetch_user(414737694808342529)
        if message.author == user or message.author == user2:
            emojis = ['🇪', '🇸', '💲', '🇦']
            for emoji in emojis:
                await message.add_reaction(emoji)
    await client.process_commands(message)


# client.run(os.environ['token'])
client.run(token)
