# bot.py
import discord
TOKEN = 'OTQ4OTc1MDIxMjk1MDM4NTE2.YiDn3A.a8OyeOmtCioEdx9YYk3sntEWjlY'
GUILD = 'DiscordBot'
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            print(f"{client.user} is connected to the following guild: {guild.name}({guild.id})")
            print(f"members in guild:")
            for member in guild.members:
                print(f"{member.name} ")
            print("Channels:")
            for channel in guild.channels:
                print(f"{channel.name}")


@client.event
async def on_message(message):
    if message.content == "/hello":
        await message.channel.send("Hello there")


@client.event
async def on_member_join(member):
    for guild in client.guilds:
        if guild.name == GUILD:
            for channel in guild.channels:
                if channel.name == "general":
                    await channel.send(f"Hello {member.name}, welcome to the server!")


client.run(TOKEN)
