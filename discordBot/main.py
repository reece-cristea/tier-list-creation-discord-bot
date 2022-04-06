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
    load_tier_lists()
    print(len(client.main_list))
    print(client.main_list[0].owner)
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
            entry = TierList(title, True, message.author.id)
            if len(message_contents) >= 3:
                category = message_contents[2]
                entry.change_category(category)
            if len(message_contents) >= 4:
                if message_contents[3] == "no":
                    entry.change_save(False)
            client.main_list.append(entry)
        await message.channel.send("Created Tier List")

    if message_contents[0] == "!showTierList":
        if len(message_contents) >= 2:
            tier_list = get_tier_list(message_contents[1], message.author)
            entry_list = tier_list.list_of_entries
            await message.channel.send(tier_list.title)
            await message.channel.send(f"No.                            Name                                    Rank")
            count = 0
            for entry in entry_list:
                count += 1
                await message.channel.send(f"{count}.                               {entry.to_string()}")

    if message_contents[0] == "!addEntryToTierList":
        await message.channel.send("here")
        if len(message_contents) == 4:
            tier_list = get_tier_list(message_contents[1], message.author)
            entry = TierListEntry(message_contents[2], message_contents[3])
            print(tier_list)
            tier_list.add_entry(entry.name, entry.rank)
            if tier_list.save:
                save_entry_to_list(entry, tier_list)
            await message.channel.send("created entry")


@client.event
async def on_member_join(member):
    for guild in client.guilds:
        if guild.name == GUILD:
            for channel in guild.channels:
                if channel.name == "general":
                    await channel.send(f"Hello {member.name}! Welcome to the server.")


def get_tier_list(title, owner):
    print(title)
    print(owner)
    for x in range(len(client.main_list)):
        print(client.main_list[x])
        print(client.main_list[x].title)
        print(client.main_list[x].owner)
        print(client.main_list[x].title == title)
        print(client.main_list[x].owner == owner.id)
        if client.main_list[x].title == title and client.main_list[x].owner == owner.id:
            return client.main_list[x]
    return None


def load_tier_lists():
    list_of_lists = open("save-tier-lists.txt")
    num_of_lists = list_of_lists.readline()
    for x in range(int(num_of_lists)):
        tier_list_line = list_of_lists.readline()
        properties = tier_list_line.split()
        tier_list = TierList(properties[0], True, str(properties[1]))
        for i in range(int(properties[2])):
            entry_line = list_of_lists.readline().split()
            entry = TierListEntry(entry_line[0], int(entry_line[1]))
            tier_list.add_entry(entry.name, entry.rank)
        client.main_list.append(tier_list)
    list_of_lists.close()


def save_entry_to_list(entry, tier_list):
    save_file = open("save-tier-lists.txt")
    num = int(save_file.readline())
    for x in range(num):
        title = save_file.readline().split()[0]
        if tier_list.title == title:
            entry_string = entry.to_string()
            save_file.write(entry_string)


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

    def change_save(self, save):
        self.save = save


class TierListEntry:
    name: None
    rank: None

    def __init__(self, name, rank):
        self.name = name
        self.rank = rank

    def to_string(self):
        entry = str(self.name + "                                    " + str(self.rank))
        return entry


client.run(TOKEN)
