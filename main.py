# 1134699422427200
# add russian roulette, automatic if Sophia says SEVENTEEN
import discord
from discord.ext import commands
import asyncio
import os
import time
import random
import spotifyAPI
used_servers = [discord.Object(id=1361848960955977840),discord.Object(id=1361810429441212536)]
userRizzcoins = {}
userWagers = {}
idToDisplayName = {}
proposedWagers = []
excludedPeople = {"Simply a Bot Tester","Green-bot","Rizz Scribe"}
roulettedUsers = set()
HOUR_MS = 1000*60*6
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self.lastTime = 0
        super().__init__(command_prefix=commands.when_mentioned_or('/'), intents=intents)
    async def on_ready(self):
        global userRizzcoins
        global userWagers
        global idToDisplayName
        for test_server in used_servers:
            self.tree.copy_global_to(guild=test_server)
            await self.tree.sync(guild=test_server)
        with open("rizzcoins.json","r") as fl:
            c = json.load(fl)
        userRizzcoins = {int(k):v for k,v in c.items() if k != "lastDeposit"}
        userRizzcoins["lastDeposit"] = c["lastDeposit"]
        with open("wagers.json","r") as fl:
            userWagers = {int(k):v for k,v in json.load(fl).items()}
        self.lastTime = userRizzcoins["lastDeposit"]
        for guild in client.guilds:
            for member in guild.members:
                if member.id not in userRizzcoins:
                    userRizzcoins[member.id] = 0
                if member.id not in userWagers:
                    userWagers[member.id] = []
                if member.id not in idToDisplayName:
                    idToDisplayName[member.id] = member.display_name
        self.bg_task = self.loop.create_task(self.checkAddRizzcoins())
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
    async def checkAddRizzcoins(self):
        await self.wait_until_ready()
        while not self.is_closed():
            cTime = time.time()*1000
            if cTime-self.lastTime >= HOUR_MS:
                toAdd = 0
                while cTime-self.lastTime >= HOUR_MS:
                    toAdd += 1
                    self.lastTime += HOUR_MS
                    cTime = time.time()*1000
                for i in userRizzcoins:
                    if i == "lastDeposit":continue
                    userRizzcoins[i] += toAdd
                userRizzcoins["lastDeposit"] = self.lastTime

                with open("rizzcoinsTemp.json","w") as fl:
                    json.dump(userRizzcoins,fl)
                os.replace("rizzcoinsTemp.json","rizzcoins.json")
            await asyncio.sleep(10)

client = Bot()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "scoreboard" in message.content.lower():
        final = []
        counter = 0
        for i,j in sorted(userRizzcoins.items(),key=lambda x:x[1],reverse=True):
            if i == "lastDeposit" or idToDisplayName[i] in excludedPeople:continue
            counter += 1
            final.append(f"{counter}. {idToDisplayName[i]}: {j}")
        # await interaction.response.send_message("\n".join(final),ephemeral=True)
        embed = discord.Embed(title=f"RizzCoin Leaderboard", colour=discord.Colour.yellow())
        embed.add_field(name="Leaderboard", value=f"\n".join(final))
        await message.channel.send(embed=embed)
    if message.author.id in roulettedUsers:
        if random.random() < 0.3333:
            await message.delete()
    if "SEVENTEEN" in message.content and message.author.id == 735282479476506674:
        roulettedUsers.add(message.author.id)
@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return
    print(message.content)
from zoeChessCommands import ZoeChess
client.tree.add_command(ZoeChess())
import json
class Gambling(discord.app_commands.Group): # wagers stored as [id1,id2,amount,name,description]
    def __init__(self):
        super().__init__(name="gambling",description="Commands to gamble your RizzCoin")
    @discord.app_commands.command(name="balance", description="Check how much RizzCoin you have")
    async def balance(self, interaction: discord.Interaction, other_user: discord.Member = None):
        await interaction.response.send_message(f"{'You have' if other_user == None else 'They have'} {userRizzcoins[interaction.user.id if other_user == None else other_user.id]} RizzCoin",ephemeral=True)
    @discord.app_commands.command(name="wager", description="Propose a new RizzCoin bet with a user")
    async def wager(self, interaction: discord.Interaction, other_gambler:discord.Member, amount:int, wager_name:str, description:str):
        effectiveRizzcoins = userRizzcoins[interaction.user.id] - sum(i[2] for i in userWagers[interaction.user.id]) - sum(i[2] for i in proposedWagers if i[0] == interaction.user.id)
        effectiveRizzcoins2 = userRizzcoins[other_gambler.id] - sum(i[2] for i in userWagers[other_gambler.id]) - sum(i[2] for i in proposedWagers if i[0] == other_gambler.id)
        if effectiveRizzcoins < amount:
            await interaction.response.send_message("You don't have enough money for that wager",ephemeral=True)
            return
        if effectiveRizzcoins2 < amount:
            await interaction.response.send_message("They don't have enough money for that wager",ephemeral=True)
            return
        if len([i for i in proposedWagers if i[3] == wager_name] + [i for i in userWagers[other_gambler.id] if i[3] == wager_name] + [i for i in userWagers[interaction.user.id] if i[3] == wager_name]) > 0:
            await interaction.response.send_message("That wager name already exists",ephemeral=True)
            return
        proposedWagers.append([interaction.user.id,other_gambler.id,amount,wager_name,description])
        await interaction.response.send_message(f"{interaction.user.display_name} proposes a wager \"{wager_name}\" with {other_gambler.display_name} for {amount} RizzCoin. The description is as follows: \"{description}\"")
    @discord.app_commands.command(name="accept", description="Accept a proposed RizzCoin wager")
    async def accept(self, interaction: discord.Interaction, wager_name:str):
        found = [i for i in proposedWagers if i[3] == wager_name]
        if len(found) == 0:
            await interaction.response.send_message("That wager name doesn't exist",ephemeral=True)
            return
        found = [i for i in found if i[1] == interaction.user.id]
        if len(found) == 0:
            await interaction.response.send_message("That wager wasn't for you",ephemeral=True)
            return
        found = found[0]
        effectiveRizzcoins = userRizzcoins[found[0]] - sum(i[2] for i in userWagers[found[0]]) - sum(i[2] for i in proposedWagers if i[0] == found[0] and i[3] != found[3])
        effectiveRizzcoins2 = userRizzcoins[found[1]] - sum(i[2] for i in userWagers[found[1]]) - sum(i[2] for i in proposedWagers if i[0] == found[1] and i[3] != found[3])
        if effectiveRizzcoins < found[2]:
            await interaction.response.send_message("They don't have enough money for that wager",ephemeral=True)
            return
        if effectiveRizzcoins2 < found[2]:
            await interaction.response.send_message("You don't have enough money for that wager",ephemeral=True)
            return
        userWagers[found[1]].append(found)
        userWagers[found[0]].append(found)
        with open("wagersTemp.json","w") as fl:
            json.dump(userWagers,fl)
        os.replace("wagersTemp.json","wagers.json")
        await interaction.response.send_message(f"{interaction.user.display_name} accepted the wager \"{wager_name}\"")
    @discord.app_commands.command(name="listwagers", description="List all of the current RizzCoin wagers you're part of")
    async def listwagers(self, interaction: discord.Interaction):
        final = []
        if len(userWagers[interaction.user.id]) == 0:
            await interaction.response.send_message("You're not currently in any wagers",ephemeral=True)
            return
        for you,other,amount,name,description in userWagers[interaction.user.id]:
            other = other if you==interaction.user.id else you
            final.append(f"\"{name}\": {amount} RizzCoin with {idToDisplayName[other]}, description \"{description}\"")
        await interaction.response.send_message("\n".join(final),ephemeral=True)
    @discord.app_commands.command(name="leaderboard", description="View the leaderboard of who is the richest in RizzCoin")
    async def leaderboard(self, interaction: discord.Interaction):
        final = []
        counter = 0
        for i,j in sorted(userRizzcoins.items(),key=lambda x:x[1],reverse=True):
            if i == "lastDeposit" or idToDisplayName[i] in excludedPeople:continue
            counter += 1
            final.append(f"{counter}. {idToDisplayName[i]}: {j}")
        # await interaction.response.send_message("\n".join(final),ephemeral=True)
        embed = discord.Embed(title=f"RizzCoin Leaderboard", colour=discord.Colour.yellow())
        embed.add_field(name="Leaderboard", value=f"\n".join(final))
        await interaction.response.send_message(embed=embed,ephemeral=True)
    @discord.app_commands.command(name="win", description="Win a current RizzCoin wager")
    async def win(self, interaction: discord.Interaction, wager_name:str):
        currentUser = interaction.user.id
        found = [(i,j) for (j,i) in enumerate(userWagers[currentUser]) if i[3] == wager_name]
        if len(found) == 0:
            await interaction.response.send_message("You aren't in a wager with that name",ephemeral=True)
            return
        found,ind = found[0]
        otherUser = found[1] if found[0] == currentUser else found[0]
        userWagers[currentUser].pop(ind)
        userWagers[otherUser].pop([j for (j,i) in enumerate(userWagers[otherUser]) if i[3] == wager_name][0])
        userRizzcoins[currentUser] += found[2]
        userRizzcoins[otherUser] -= found[2]
        with open("rizzcoinsTemp.json","w") as fl:
            json.dump(userRizzcoins,fl)
        os.replace("rizzcoinsTemp.json","rizzcoins.json")
        with open("wagersTemp.json","w") as fl:
            json.dump(userWagers,fl)
        os.replace("wagersTemp.json","wagers.json")
        await interaction.response.send_message(f"{interaction.user.display_name} won the wager \"{wager_name}\" against {idToDisplayName[otherUser]}")
# client.tree.add_command(Gambling())
editedMessages = {}
@client.event
async def on_message_edit(before, after):
    if before.content != after.content:
        if before.content in editedMessages:
            editedMessages[after.content] = editedMessages[before.content]
        else:
            editedMessages[after.content] = before.content
@discord.app_commands.command(name="secret",description="Secret commands for just Eli to use because I'm funny and I don't trust most people with this power")
async def secret(interaction:discord.Interaction,*,args:str):
    args = args.split("|")
    if len(args) < 4:return
    if args[0] not in ["grammar"]:return
    channel = interaction.channel #get channel where command was used
    if args[0] == "grammar":
        await channel.send(f"Ummm ahcktually it should be \"{args[2]}\" instead of \"{args[1]}.\"",reference=await channel.fetch_message(args[3].strip()))
        await interaction.response.send_message("worked",ephemeral=True)
@discord.app_commands.command(name="reference",description="Reference a song by its title and artist")
async def reference(interaction:discord.Interaction,title:str,artist:str):
    channel = interaction.channel
    result = await spotifyAPI.getSong(title,artist)
    if "tracks" not in result:
        await interaction.response.send_message("sorry it failed, mb",ephemeral=True)
        return
    result = result["tracks"]["items"][0]
    embed = discord.Embed(
        title=result["name"],
        description=" | ".join([i["name"] for i in result["artists"]]),
        color=discord.Color.light_gray()
	)
    embed.set_thumbnail(url=result["album"]["images"][0]["url"])
    await channel.send(embed=embed)
    await interaction.response.send_message("worked",ephemeral=True)
@discord.app_commands.context_menu(name="Put On Blast")
async def putOnBlast(interaction,message:discord.Message):
    a = message.content
    if a in editedMessages:
        originalMessage = editedMessages[a]
    else:
        await interaction.response.send_message("Either that's not an edited message or the bot has restarted since it was sent.",ephemeral=True)
        return
    await interaction.response.send_message("Success",ephemeral=True)
    await message.reply("The original message was:\n>>> "+originalMessage)
import datetime
def get_formatted_date():
    now = datetime.datetime.now()-datetime.timedelta(hours=4)
    day = now.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    formatted_date = now.strftime(f"%B {day}{suffix}, %Y")
    return formatted_date
@discord.app_commands.context_menu(name='Quote them on That')
async def quoteThemOnThat(interaction, message:discord.Message):
    final = f">>> *\"{message.content}\"* - {message.author.display_name} ({get_formatted_date()})"
    await interaction.response.send_message(final)

client.tree.add_command(putOnBlast)
client.tree.add_command(quoteThemOnThat)
client.tree.add_command(secret)
client.tree.add_command(reference)
client.run('.'.join(['MTM2MTgyMzIxOTM4ODEyNTMxNA','G4ayHA','Ou219vOevrd-L9UG5vgexY5wgIP6GL4LK9p3mU']))


# 1745139600000