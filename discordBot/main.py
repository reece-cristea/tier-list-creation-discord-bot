# bot.py
import discord
TOKEN = 'OTQ4OTc1MDIxMjk1MDM4NTE2.YiDn3A.a8OyeOmtCioEdx9YYk3sntEWjlY'
GUILD = 'DiscordBot'
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
client.main_list = []


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
    message_contents = message.content.split()
    if message_contents[0] == "!createTierList":
        if len(message_contents) >= 2:
            title = message_contents[1]
            entry = TierList(title, True, message.author)
            if len(message_contents) >= 3:
                category = message_contents[2]
                entry.change_category(category)
            client.main_list.append(entry)
        await message.channel.send("Created Tier List")

    if message_contents[0] == "!showTierList":
        await message.channel.send("here")
        if len(message_contents) >= 2:
            tier_list = get_tier_list(message_contents[1], message.author)
            entry_list = tier_list.get_entry_list()
            count = 0
            for entry in entry_list:
                count += 1
                await message.channel.send(f"{count}. {entry.to_string()}")

    if message_contents[0] == "!addEntryToTierList":
        await message.channel.send("here")
        if len(message_contents) == 4:
            tier_list = get_tier_list(message_contents[1], message.author)
            tier_list.add_entry(message_contents[2], message_contents[3])
            await message.channel.send("created entry")


@client.event
async def on_member_join(member):
    for guild in client.guilds:
        if guild.name == GUILD:
            for channel in guild.channels:
                if channel.name == "general":
                    await channel.send(f"{member.name} is a bing bong.")


def get_tier_list(title, owner):
    for tier_list in client.main_list:
        if tier_list.get_title() == title and tier_list.get_owner() == owner:
            return tier_list
    return None


class TierList:
    name: None
    category: None
    list_of_entries: []
    save: None
    owner: None

    def __init__(self, title, save, owner):
        self.title = title
        self.save = save
        self.owner = owner
        self.category = None
        self.list_of_entries = []

    def add_entry(self, name, rank):
        entry = TierListEntry(name, rank)
        self.list_of_entries.append(entry)

    def get_title(self):
        return self.title

    def get_owner(self):
        return self.owner

    def get_entry_list(self):
        return self.list_of_entries

    def change_category(self, category):
        self.category = category


class TierListEntry:
    name: None
    rank: None

    def __init__(self, name, rank):
        self.name = name
        self.rank = rank

    def to_string(self):
        entry = str(self.name + " " + self.rank)
        return entry


client.run(TOKEN)
