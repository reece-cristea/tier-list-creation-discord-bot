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
            if entry.save:
                entry.add_list_to_save_file()

        await message.channel.send("Created Tier List")

    if message_contents[0] == "!showTierList":
        if len(message_contents) >= 2:
            tier_list = get_tier_list(message_contents[1], message.author)
            entry_list = tier_list.list_of_entries
            await message.channel.send(tier_list.title)
            await message.channel.send(f"No. Name Rank")
            count = 0
            for entry in entry_list:
                count += 1
                await message.channel.send(f"{count}. {entry.to_string()}")

    if message_contents[0] == "!addEntryToTierList":
        await message.channel.send("here")
        if len(message_contents) == 4:
            tier_list = get_tier_list(message_contents[1], message.author)
            entry = TierListEntry(message_contents[2], message_contents[3])
            tier_list.add_entry(entry.name, entry.rank)
            if tier_list.save:
                print("here")
                save_entry_to_list(entry, tier_list)
            await message.channel.send("created entry")

    if message_contents[0] == "!help":
        if len(message_contents) == 1:
            await message.channel.send("Hi there, below is the manual for the Tier List Maker Discord Bot.\n\n"
                                       "Here is a list of available commands:\n"
                                       "!createTierList\n"
                                       "!showTierList\n"
                                       "!addEntryToTierList\n"
                                       "!help\n\n"
                                       "To see more help on a command type '!help (command)'.\n")
        if len(message_contents) > 1:
            if message_contents[1] == "createTierList":
                await message.channel.send(
                    "Correct syntax to use !createTierList ({} means required, [] means optional)\n\n"
                    "!createTierList {title of tier list} [category of tier list] [save tier list]\n\n"
                    "!createTierList creates a tier list object with a title. "
                    "You can add a category if you would like and you can also choose "
                    "to not save the list because a list is saved by default.\n")
            elif message_contents[1] == "showTierList":
                await message.channel.send(
                    "Correct syntax to use !showTierList ({} means required, [] means optional):\n"
                    "!showTierList {title of tier list} [owner]\n\n"
                    "!showTierList displays the tier list object with the matching title. "
                    "By default, it will display tier lists you own, but if you would like "
                    "to display another person's tier list, you can add a owner specifier.\n")
            elif message_contents[1] == "addEntryToTierList":
                await message.channel.send(
                    "Correct syntax to use !createTierList ({} means required, [] means optional)\n\n"
                    "!addEntryToTierList {title of tier list} [name of entry] [rank of entry]\n\n"
                    "!addEntryToTierList creates a tier list entry object and adds it to a "
                    "tier list. You can only add an entry to a tier list you own.\n")
            else:
                await message.channel.send("Sorry, I didn't recognize the command you were looking for. "
                                           "Use !help to get a list of commands you can use.")


@client.event
async def on_member_join(member):
    for guild in client.guilds:
        if guild.name == GUILD:
            for channel in guild.channels:
                if channel.name == "general":
                    await channel.send(f"Hello {member.name}! Welcome to the server.")


def get_tier_list(title, owner):
    for x in range(len(client.main_list)):
        print("here list")
        print(client.main_list[x].title)
        print(title)
        print(client.main_list[x].owner)
        print(str(owner.id))
        if client.main_list[x].title == title and client.main_list[x].owner == str(owner.id):
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
    save_file = open("save-tier-lists.txt", "r")
    lines = save_file.readlines()
    for x in range(len(lines)):
        title = lines[x].split()[0]
        if tier_list.title == title:
            tier_list_info = lines[x].split()
            tier_list_info[2] = str(len(tier_list.list_of_entries))
            new_tier_list_info = " ".join(tier_list_info) + "\n"
            lines[x] = new_tier_list_info
            entry_string = entry.to_string()
            lines.insert(x + 1, entry_string + "\n")
            break
    save_file.close()
    save_file = open("save-tier-lists.txt", "w")
    save_file.write("".join(lines))
    save_file.close()


class TierList:
    name: None
    category: None
    list_of_entries: []
    save: None
    owner: None

    def __init__(self, title, save, owner):
        self.title = title
        self.save = save
        self.owner = str(owner)
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

    def add_list_to_save_file(self):
        save_file = open("save-tier-lists.txt", "a")
        save_file.write(f"{self.title} {str(self.owner)} {str(len(self.list_of_entries))}\n")
        save_file.close()
        save_file = open("save-tier-lists.txt")
        lines = save_file.readlines()
        lines[0] = f"{str(len(client.main_list))}\n"
        save_file.close()
        save_file = open("save-tier-lists.txt", "w")
        save_file.writelines(lines)
        save_file.close()


class TierListEntry:
    name: None
    rank: None

    def __init__(self, name, rank):
        self.name = name
        self.rank = rank

    def to_string(self):
        entry = str(self.name + " " + str(self.rank))
        return entry


client.run(TOKEN)
