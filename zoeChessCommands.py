import discord
import zoeChess
from typing import Optional
class NoteGroup(discord.app_commands.Group):
    def __init__(self, parent):
        super().__init__(name="note", description="Commands for managing notes")
        self.parent = parent

    @discord.app_commands.command(name="read", description="Reads the notes on a piece")
    async def read(self, interaction: discord.Interaction, pos: str):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("note", "read", pos))

    @discord.app_commands.command(name="add", description="Adds a note to a piece")
    async def add(self, interaction: discord.Interaction, pos: str, note: str):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("note", "add", pos, note))
    
    @discord.app_commands.command(name="clear", description="Clears all notes from a piece")
    async def clear(self, interaction: discord.Interaction, pos: str):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("note", "clear", pos))
        
    @discord.app_commands.command(name="replace", description="Replaces all notes from a piece with a new note")
    async def replace(self, interaction: discord.Interaction, pos: str, note: str):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("note", "replace", pos, note))
class MarkerGroup(discord.app_commands.Group):
    def __init__(self, parent):
        super().__init__(name="marker", description="Commands for managing markers")
        self.parent = parent

    @discord.app_commands.command(name="read", description="Reads the markers on a piece")
    async def read(self, interaction: discord.Interaction, pos: str):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("marker", "read", pos))

    @discord.app_commands.command(name="getdescription", description="Reads a marker's description")
    async def get_description(self, interaction: discord.Interaction, name: str):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("marker", "getDescription", name))
    
    @discord.app_commands.command(name="new", description="Creates a new type of marker")
    async def new(self, interaction: discord.Interaction, name: str, color:str, description:str):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("marker", "new", name, color, description))
        
    @discord.app_commands.command(name="editcolor", description="Edits the color of a type of marker")
    async def edit_color(self, interaction: discord.Interaction, name: str, new_color:str):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("marker", "edit", "color", name, new_color))
        
    @discord.app_commands.command(name="editdescription", description="Edits the description of a type of marker")
    async def edit_description(self, interaction: discord.Interaction, name: str, new_description:str):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("marker", "edit", "description", name, new_description))

    @discord.app_commands.command(name="add", description="Adds a marker to a piece")
    async def add(self, interaction: discord.Interaction, name: str, pos:str, duration: Optional[int]=-1):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("marker", "add", name, pos, duration))
        
    @discord.app_commands.command(name="changeduration", description="Changes the duration of a marker on a piece")
    async def change_duration(self, interaction: discord.Interaction, name:str, pos: str, new_duration:int):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("marker", "changeDuration", name, pos, new_duration))
        
    @discord.app_commands.command(name="remove", description="Removes a marker from a piece")
    async def remove(self, interaction: discord.Interaction, name:str, pos: str):
        if not await self.parent.canInteractWithGame(interaction): return
        await interaction.response.send_message(await self.parent.games[self.parent.playerInGame[interaction.user.id]].handleCommand("marker", "remove", name, pos))
        
class ZoeChess(discord.app_commands.Group):
    def __init__(self):
        super().__init__(name="zoechess",description="Commands for playing ZoeChess")
        self.playerInGame = {}
        self.games = []
        self.add_command(NoteGroup(self))
        self.add_command(MarkerGroup(self))
    async def canInteractWithGame(self,interaction):
        user = interaction.user.id
        if user not in self.playerInGame:
            await interaction.response.send_message("You're not in a match",ephemeral=True)
            return False
        gameIndex = self.playerInGame[user]
        if self.games[gameIndex] == "Waiting":
            await interaction.response.send_message("No one's joined your match yet",ephemeral=True)
            return False
        c = self.games[gameIndex]
        if user != c.players[c.current_player]:
            await interaction.response.send_message("It's not your turn, you dip",ephemeral=True)
            return False
        return True
    group = discord.app_commands
    # Gameplay commands
    @group.command(name="move", description="Moves a piece")
    async def move(self, interaction: discord.Interaction, from_pos: str, to_pos:str):
        if not await self.canInteractWithGame(interaction):return
        await interaction.response.send_message(await self.games[self.playerInGame[interaction.user.id]].handleCommand("move",from_pos,to_pos))
    @group.command(name="addpiece", description="Adds a new piece to the board")
    async def addPiece(self, interaction: discord.Interaction, piece_owner: str, piece_type:str, pos:str):
        if not await self.canInteractWithGame(interaction):return
        await interaction.response.send_message(await self.games[self.playerInGame[interaction.user.id]].handleCommand("addPiece",piece_owner,piece_type,pos))
    @group.command(name="removepiece", description="Removes a piece from the board")
    async def removePiece(self, interaction: discord.Interaction, pos: str):
        if not await self.canInteractWithGame(interaction):return
        await interaction.response.send_message(await self.games[self.playerInGame[interaction.user.id]].handleCommand("removePiece", pos))
    @group.command(name="pass", description="Passes your turn")
    async def passTurn(self, interaction: discord.Interaction):
        if not await self.canInteractWithGame(interaction):return
        await interaction.response.send_message(await self.games[self.playerInGame[interaction.user.id]].handleCommand("pass"))
    @group.command(name="newgame", description="Creates a new ZoeChess instance and joins it, another player can join with /zoechess join")
    async def newGame(self, interaction: discord.Interaction):
        user = interaction.user.id
        if user in self.playerInGame:
            await interaction.response.send_message("You're already in a match",ephemeral=True)
            return
        usableIndex = 0
        while usableIndex < len(self.games):
            if self.games[usableIndex] is None:
                break
            usableIndex += 1
        if usableIndex == len(self.games):
            self.games.append("Waiting")
        else:
            self.games[usableIndex] = "Waiting"
        self.playerInGame[user] = usableIndex
        await interaction.response.send_message("New game created")
    @group.command(name="endgame", description="Ends the ZoeChess instance that you're in")
    async def endGame(self, interaction: discord.Interaction):
        user = interaction.user.id
        if user not in self.playerInGame:
            await interaction.response.send_message("You're not in a match",ephemeral=True)
            return
        c = self.games[self.playerInGame[user]]
        if c == "Waiting":
            self.games[self.playerInGame[user]] = None
            del self.playerInGame[user]
        elif c is None:
            await interaction.response.send_message("An error occured; give the bot creator the error code 16.",ephemeral=True)
        else:
            a,b = c.players
            self.games[self.playerInGame[a]] = None
            del self.playerInGame[a]
            del self.playerInGame[b]
        await interaction.response.send_message("Game ended")
    @group.command(name="join", description="Join's a player's ZoeChess instance")
    async def join(self, interaction: discord.Interaction, other_player:discord.Member):
        user = other_player.id
        user2 = interaction.user.id
        if user2 in self.playerInGame:
            await interaction.response.send_message("You're already in a match",ephemeral=True)
            return
        if user not in self.playerInGame:
            await interaction.response.send_message("That person's not queued for a match",ephemeral=True)
            return
        self.playerInGame[user2] = self.playerInGame[user]
        c = await interaction.channel.send("Loading")
        self.games[self.playerInGame[user]] = await zoeChess.ZoeChessInstance.init(user,user2,c)
        await interaction.response.send_message("Game started")
        # await interaction.response.send_message(str(str(self.playerInGame[user] if user in self.playerInGame else "DNE")+ " " + str(self.games[self.playerInGame[user]] if user in self.playerInGame else "DNE")),ephemeral=True)