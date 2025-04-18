pieceCharMapping = {
    "rook":"♖♜",
    "king":"♔♚",
    "queen":"♕♛",
    "bishop":"♗♝",
    "knight":"♘♞",
    "pawn":"♙♟"
}
import os
RESET = '\033[0m'
def colorText(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'
class ZoeChessPiece:
    def __init__(self,piece,player,x,y):
        self.piece = piece
        self.player = player
        self.x = x
        self.y = y
        self.displayChar = pieceCharMapping[piece][player]
        self.notes = []
        self.markers = []
    def getNote(self):
        return "\n".join(self.notes)
    def getMarkers(self):
        return "\n".join([f"{i[0]} for {i[1]} turns" for i in self.markers])
    def getDisplay(self, instance):
        if len(self.markers) != 1:
            return f" {self.displayChar} "
        markerIndex = instance.markerNames.index(self.markers[0][0])
        r1,r2,g1,g2,b1,b2 = list(instance.markerColors[markerIndex][1:])
        return f" {colorText(int(r1+r2,16),int(g1+g2,16),int(b1+b2,16))}{self.displayChar}{RESET} "
import random
class ZoeChessRules:
    @staticmethod
    def notationToXY(notation):
        return "abcdefgh".index(notation[0]),int(notation[1])-1
    @staticmethod
    def isValidNotation(notation):
        return notation[0] in "abcdefgh" and notation[1] in "12345678"
    @staticmethod
    def xYToNotation(x, y):
        return "abcdefgh"[x]+str(y+1)
class ZoeChessInstance:
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    WHITE = 0
    BLACK = 1

    def __init__(self, player1, player2):
        self.current_player = random.randint(0,1)
        self.markerNames = []
        self.markerDescriptions = []
        self.markerColors = []
        self.players = [player1,player2]
        self.board = [
            [ZoeChessPiece("rook",1,0,0), ZoeChessPiece("knight",1,1,0), ZoeChessPiece("bishop",1,2,0), ZoeChessPiece("queen",1,3,0), ZoeChessPiece("king",1,4,0), ZoeChessPiece("bishop",1,5,0), ZoeChessPiece("knight",1,6,0), ZoeChessPiece("rook",1,7,0)],
            [ZoeChessPiece("pawn",1,0,1), ZoeChessPiece("pawn",1,1,1), ZoeChessPiece("pawn",1,2,1), ZoeChessPiece("pawn",1,3,1), ZoeChessPiece("pawn",1,4,1), ZoeChessPiece("pawn",1,5,1), ZoeChessPiece("pawn",1,6,1), ZoeChessPiece("pawn",1,7,1)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [ZoeChessPiece("pawn",0,0,6), ZoeChessPiece("pawn",0,1,6), ZoeChessPiece("pawn",0,2,6), ZoeChessPiece("pawn",0,3,6), ZoeChessPiece("pawn",0,4,6), ZoeChessPiece("pawn",0,5,6), ZoeChessPiece("pawn",0,6,6), ZoeChessPiece("pawn",0,7,6)],
            [ZoeChessPiece("rook",0,0,7), ZoeChessPiece("knight",0,1,7), ZoeChessPiece("bishop",0,2,7), ZoeChessPiece("queen",0,3,7), ZoeChessPiece("king",0,4,7), ZoeChessPiece("bishop",0,5,7), ZoeChessPiece("knight",0,6,7), ZoeChessPiece("rook",0,7,7)],
        ]
    def move(self,fromNotation,toNotation):
        fromNotation = fromNotation[:2]
        toNotation = toNotation[:2]
        if not ZoeChessRules.isValidNotation(fromNotation) or not ZoeChessRules.isValidNotation(toNotation):
            return "Fix your notation, you bum"
        x1,y1 = ZoeChessRules.notationToXY(fromNotation)
        x2,y2 = ZoeChessRules.notationToXY(toNotation)
        if self.board[y1][x1] == None:
            return "There's no piece there, stupidface"
        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = None
        return "You moved it all right"
    def moveToRiver(self,fromNotation):
        fromNotation = fromNotation[:2]
        if not ZoeChessRules.isValidNotation(fromNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(fromNotation)
        if self.board[y][x] == None:
            return "There's no piece there, stupidface"
        if random.random() < 0.5:
            newX = random.randint(0,7)
            newY = random.randint(0,1)*7
        else:
            newY = random.randint(0,7)
            newX = random.randint(0,1)*7
        self.board[newY][newX] = self.board[y][x]
        self.board[y][x] = None
        return f"Went for a swim and landed on {ZoeChessRules.xYToNotation(newX,newY)}"
    def removePiece(self,posNotation):
        posNotation = posNotation[:2]
        if not ZoeChessRules.isValidNotation(posNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(posNotation)
        if self.board[y][x] == None:
            return "There wasn't a piece there anyway, but go off I guess"
        self.board[y][x] = None
        return f"You removed that piece all right"
    def readNote(self,posNotation):
        posNotation = posNotation[:2]
        if not ZoeChessRules.isValidNotation(posNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(posNotation)
        if self.board[y][x] == None:
            return "There's no piece there, stupidface"
        return self.board[y][x].getNote()
    def clearNote(self,posNotation):
        posNotation = posNotation[:2]
        if not ZoeChessRules.isValidNotation(posNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(posNotation)
        if self.board[y][x] == None:
            return "There's no piece there, stupidface"
        self.board[y][x].notes = []
        return "Cleared the notes all right"
    def addNote(self,posNotation, newNote):
        posNotation = posNotation[:2]
        if not ZoeChessRules.isValidNotation(posNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(posNotation)
        if self.board[y][x] == None:
            return "There's no piece there, stupidface"
        self.board[y][x].notes.append(newNote)
        return "Added that note all right"
    def replaceNote(self,posNotation, newNote):
        posNotation = posNotation[:2]
        if not ZoeChessRules.isValidNotation(posNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(posNotation)
        if self.board[y][x] == None:
            return "There's no piece there, stupidface"
        self.board[y][x].notes = [newNote]
        return "Replaced the notes with what you gave all right"
    def deleteMarker(self,markerName):
        if markerName not in self.markerNames:return "That isn't a marker, bozo"
        markerIndex = self.markerNames.index(markerName)
        self.markerNames.remove(markerIndex)
        self.markerColors.remove(markerIndex)
        return "Deleted that marker all right"
    def describeMarker(self,markerName):
        if markerName not in self.markerNames:return "That isn't a marker, bozo"
        markerIndex = self.markerNames.index(markerName)
        return self.markerDescriptions[markerIndex]
    def editMarkerColor(self,markerName,newColor):
        if markerName not in self.markerNames:return "That isn't a marker, bozo"
        markerIndex = self.markerNames.index(markerName)
        self.markerColors[markerIndex] = newColor
        return "Changed the marker color all right"
    def newMarker(self,markerName,markerColor,markerDescription):
        if markerName in self.markerNames:return "There's already a marker named that, goober"
        self.markerNames.append(markerName)
        self.markerColors.append(markerColor)
        self.markerDescriptions.append(markerDescription)
        return "Added the new marker all right"
    def editMarkerDescription(self,markerName,newDescription):
        if markerName not in self.markerNames:return "That isn't a marker, bozo"
        markerIndex = self.markerNames.index(markerName)
        self.markerDescriptions[markerIndex] = newDescription
        return "Changed the marker description all right"
    def addMarker(self,markerName,posNotation,duration=-1):
        if markerName not in self.markerNames:return "That isn't a marker, bozo"
        markerIndex = self.markerNames.index(markerName)
        posNotation = posNotation[:2]
        if not ZoeChessRules.isValidNotation(posNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(posNotation)
        if self.board[y][x] == None:
            return "There's no piece there, stupidface"
        try:
            int(duration)
        except:
            return "That duration isn't a whole number of turns"
        self.board[y][x].markers.append([markerName,duration])
        return "Added that marker all right"
    def removeMarker(self,markerName,posNotation):
        if markerName not in self.markerNames:return "That isn't a marker, bozo"
        markerIndex = self.markerNames.index(markerName)
        posNotation = posNotation[:2]
        if not ZoeChessRules.isValidNotation(posNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(posNotation)
        if self.board[y][x] == None:
            return "There's no piece there, stupidface"
        try:
            pieceMarkerIndex = [i[0] for i in self.board[y][x].markers].index(markerName)
        except:
            return "The piece didn't have that marker anyway, but go off I guess"
        self.board[y][x].markers.pop(pieceMarkerIndex)
        return "Removed that marker all right"
    def changeMarkerDuration(self,markerName,posNotation,newDuration):
        if markerName not in self.markerNames:return "That isn't a marker, bozo"
        markerIndex = self.markerNames.index(markerName)
        posNotation = posNotation[:2]
        if not ZoeChessRules.isValidNotation(posNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(posNotation)
        if self.board[y][x] == None:
            return "There's no piece there, stupidface"
        try:
            int(newDuration)
        except:
            return "That duration isn't a whole number of turns"
        try:
            pieceMarkerIndex = [i[0] for i in self.board[y][x].markers].index(markerName)
        except:
            return "The piece doesn't have that marker"
        self.board[y][x].markers[pieceMarkerIndex][1] = int(newDuration)
        return "Changed that marker's duration all right"
    def readMarker(self,posNotation):
        posNotation = posNotation[:2]
        if not ZoeChessRules.isValidNotation(posNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(posNotation)
        if self.board[y][x] == None:
            return "There's no piece there, stupidface"
        return self.board[y][x].getMarkers()
    def addPiece(self,pieceType,pieceOwner,posNotation):
        posNotation = posNotation[:2]
        if not ZoeChessRules.isValidNotation(posNotation): return "Fix your notation, you bum"
        x,y = ZoeChessRules.notationToXY(posNotation)
        if self.board[y][x] != None:
            return "There's already a piece there, stupidface"
        if pieceType.lower() not in pieceCharMapping:
            return "That's not even a piece, moron"
        if pieceOwner.lower() not in ["white","black"]:
            return "That's not a valid piece owner, moron"
        self.board[y][x] = ZoeChessPiece(pieceType.lower(),self.WHITE if pieceOwner.lower() == "white" else self.BLACK,x,y)
        return "Added the piece all right"
    def endTurn(self):
        self.current_player = 1-self.current_player
        for j in self.board:
            for i in j:
                if i.player == self.players[self.current_player]:
                    continue
                for k in range(len(i.markers)-1,-1,-1):
                    i.markers[k][1] -= 1
                    if i.markers[k][1] == 0:
                        i.markers.pop(k)
    def printBoard(self):
        print("   ".join(list(" abcdefgh")))
        print("  +"+"---+"*8)
        for j in range(8):
            print("|".join([str(j+1) + " ",*[i.getDisplay(self) if i else "   " for i in self.board[j]],""]))
            print("  +"+"---+"*8)
    def handleCommand(self,command):
        if command[0] == "move":
            if len(command) < 3: return "Malformed move command"
            if command[2] == "river": return self.moveToRiver(command[1])
            return self.move(command[1],command[2])
        if command[0] == "removePiece":
            if len(command) != 2: return "Malformed remove piece command"
            return self.removePiece(command[1])
        if command[0] == "note":
            if len(command) < 3: return "Malformed note command"
            if command[1] == "read":
                return self.readNote(command[2])
            if command[1] == "clear":
                return self.clearNote(command[2])
            if len(command) < 4: return "Malformed note command"
            if command[1] == "add":
                return self.addNote(command[2],command[3])
            if command[1] == "replace":
                return self.replaceNote(command[2],command[3])
            return "Malformed note command, that's not an option"
        if command[0] == "marker":
            if len(command) < 3: return "Malformed marker command"
            if command[1] == "delete":
                return self.deleteMarker(command[2].lower())
            if command[1] == "read":
                return self.readMarker(command[2])
            if command[1] == "getDescription":
                return self.describeMarker(command[2].lower())
            if len(command) < 4: return "Malformed marker command"
            if command[1] == "add":
                return self.addMarker(command[2].lower(),command[3],command[4] if len(command) > 4 else -1)
            if command[1] == "remove":
                return self.removeMarker(command[2].lower(),command[3])
            if len(command) < 5: return "Malformed marker command"
            if command[1] == "edit":
                if command[2] == "color":
                    return self.editMarkerColor(command[3].lower(),command[4])
                if command[2] == "description":
                    return self.editMarkerDescription(command[3].lower(),command[4])
                return "Malformed marker command, that's not an edit option"
            if command[1] == "new":
                return self.newMarker(command[2].lower(),command[3],command[4])
            if command[1] == "changeDuration":
                return self.changeMarkerDuration(command[2].lower(),command[3],command[4])
            return "Malformed marker command, that's not an option"
        if command[0] == "addPiece":
            if len(command) < 4: return "Malformed addPiece command"
            return self.addPiece(command[2],command[1],command[3])
        if command[0] == "pass":
            self.endTurn()
            return "Passed the turn"
        return "That's not a command, you imbicile"
game = ZoeChessInstance("a","b")
game.printBoard()
while True:
    command = input().split(" ")
    os.system("clear")
    res = game.handleCommand(command)
    game.printBoard()
    print(res)

# /zoechess move [fromPos] [toPos] ✓✓
# /zoechess move [fromPos on border] river ✓✓ - might not be able to take pieces, especially king

# /zoechess marker new [name] [color] [description] ✓✓
# /zoechess marker getDescription [name] ✓✓
# /zoechess marker read [pos] ✓✓ don't let it say turns if it's -1
# /zoechess marker edit color [name] [newColor] ✓✓
# /zoechess marker edit description [name] [newDescription] ✓✓
# /zoechess marker add [name] [pos] [?duration] ✓✓
# /zoechess marker changeDuration [name] [pos] [newDuration] ✓✓
# /zoechess marker remove [name] [pos] ✓✓

# /zoechess addPiece [pieceOwner] [pieceType] [pos] ✓✓

# /zoechess removePiece [pos] ✓✓

# /zoechess note read [pos] ✓✓
# /zoechess note add [pos] [newNote] ✓✓
# /zoechess note replace [pos] [newNote] ✓✓
# /zoechess note clear [pos] ✓✓

# /zoechess pass ✓✓

"""
Rules:

Start with normal chess rules
Take the other player's king to win
    A player may never have more than one king
You can do mostly anything on your turn
    Limit it to one "thing"
    Make sure nothing is too gamebreaking
    Option 1: use the other player for approval
    Option 2: have a referee

Common added rules; up for discussion at the beginning of a game

The River
    Pieces on the edge of the board can move into "the river."
    Those who do so end up on a random square on the border of the board
    Pieces leaving the river take pieces they land on, regardless of whose side they're on

Professions
    Use a turn to give a piece, mostly pawns, a profession
    If the profession gives allies new abilities, it may give them those abilities immediately
    If it gives itself new abilities instead of its allies, wait a turn to use it

Riding knights
    A orthogonally adjacent piece can hop on a knight before the knight moves
    They land in the same relative position
    One or none of the pieces can capture, but not both
    If both pieces would capture, you cannot make that move

Game Engine
Due to limitations, not everything is possible in this engine.
However, many things are.

You can move pieces, including into the river
You can add and remove pieces
Notes
    You can add, remove, and read notes on pieces
    Use this for gameplay such as Professions
Markers
    You can create a new type of marker and give it a color and a description
    You can edit the colors and descriptions of existing markers
    You can give pieces markers, with an optional duration
    You can also edit the duration or remove markers from pieces
And, of course, you can pass your turn

Ideas:
Here are some commonly used physical aspects of ZoeChess and how to replicate them
Combined pieces:
    For example, a piece fortifying themselves within a castle (rook)
    Remove the piece from the board
    Store all relevant information about it in a note on the rook
    When it leaves, remove that note from the rook
    Re-add the piece and restore its attributes manually
Games of skill:
    For example, throwing a small ball of paper and taking whatever piece it touches
    This cannot easily be recreated in the game engine
    Try only posing games of skill that can be completed digitally, such as guessing where a piece is
    I guess you could pull out real objects, but most people aren't that serious about online ZoeChess
Alternate pieces:
    For example, spending the first turn of the game swapping out your queen for a unicorn
    Use the original piece's icon and just store what its actual abilities are in a note
Afflicted pieces:
    For example, a freezing pawn that immobalizes pieces for two turns
    Simply create a frozen condition and give it a description that says something like "immobalizes"
    Add it to affected pieces, setting a duration of two turns
    When adding a condition to your own pieces, the current turn is counted as part of the duration



"""


"""
@fruits.autocomplete('fruit')
async def fruits_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]

"""