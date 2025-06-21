import os
from random import randint
from typing import List
from discord.ext import commands
import discord
import math
styleArray = [
    discord.ButtonStyle.grey,
    discord.ButtonStyle.blurple,
    discord.ButtonStyle.green,
    discord.ButtonStyle.red,
    discord.ButtonStyle.premium,
]
labelArray = ["\u200b"]+list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
class MergeGameInstance:
    def __init__(self):
        self.board = [[0]*5 for i in range(5)]
        self.justChecked = set()
        self.cascadeLocs = []
    def addSquare(self,x,y,val):
        self.board[y][x] = val
        self.checkSquare(x,y)
        self.justChecked = set()
        updated = [(x,y)]
        while len(self.cascadeLocs) > 0:
            x,y, = self.cascadeLocs.pop()
            self.checkSquare(x,y)
            updated.append((x,y))
            self.justChecked = set()
        return updated
    def addSquareNoUpdate(self,x,y,val):
        self.board[y][x] = val
    def moveSquare(self,x1,y1,x2,y2,view):
        if self.board[y2][x2] != 0:return
        moving = self.board[y1][x1]
        if moving == 0:return
        self.board[y1][x1] = 0
        updated = self.addSquare(x2,y2,moving)
        for x,y in updated:
            view.findButton(x,y).changeStyle()
    def checkSquare(self,x,y):
        if (x,y) in self.justChecked:
            return
        self.justChecked.add((x,y))
        target = self.board[y][x]
        neighbors = self.getSameNeighbors(x,y)
        if len(neighbors) > 2:
            self.board[neighbors[2][1]][neighbors[2][0]] = 0
            self.board[neighbors[1][1]][neighbors[1][0]] = 0
            self.board[y][x] = 0
            self.addSquareNoUpdate(x,y,target+1)
            self.cascadeLocs.append((x,y))
        elif len(neighbors) == 2:
            self.checkSquare(*neighbors[1])
    def getSameNeighbors(self,x,y):
        target = self.board[y][x]
        if target == 0:return []
        t = [(x,y)]
        for i in range(y-1,y+2):
            for j in range(x-1,y+2):
                if i < 0 or j < 0 or i > 4 or j > 4 or j == x and i == y:continue # add or abs(i)==abs(j) for no diagonals
                if self.board[i][j] == target:
                    t.append((j,i))
        return t
    def addRandom(self):
        x,y = randint(0,4),randint(0,4)
        while self.board[y][x] != 0:
            x,y = randint(0,4),randint(0,4)
        self.board[y][x] = 1
    def displayBoard(self):
        os.system("clear")
        [print(*row) for row in self.board]
class MergeGameButton(discord.ui.Button['MergeGameView']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: MergeGameView = self.view
        val = view.instance.board[self.y][self.x]
        if view.selectedButton == None:
            if val == 0:
                return
            view.selectedButton = (self.x,self.y)
            self.style = discord.ButtonStyle.link
            return
        if val != 0:
            return
        view.instance.moveSquare(*view.selectedButton,self.x,self.y,view)
        view.selectedButton = None
        await interaction.response.edit_message(content="OK HERE'S SOME TEXT", view=view)
    def changeStyle(self):
        assert self.view is not None
        view: MergeGameView = self.view
        val = view.instance.board[self.y][self.x]
        self.style = styleArray[math.fmod(val-1)%4+1]
        self.label = labelArray[val//4]

class MergeGameView(discord.ui.View):
    children: List[MergeGameButton]

    def __init__(self):
        super().__init__()
        self.intance = MergeGameInstance()
        self.selectedButton = None
        for x in range(5):
            for y in range(5):
                self.add_item(MergeGameButton(x, y))
    def findButton(self,x,y):
        for i in self.children:
            if i.x == x and i.y == y:return i
        print("Didn't find it")
        return None
# test = MergeGameInstance()
# test.addSquare(1,0,1)
# test.addSquare(0,1,1)
# test.addSquareNoUpdate(2,1,1)
# test.addSquareNoUpdate(1,2,1)
# test.displayBoard()
# test.addSquare(1,1,1)
# test.displayBoard()
# exit()
# while True:
#     test.displayBoard()
#     a = input()
#     if a == "":
#         test.addRandom()
#     else:
#         x1,y1,x2,y2 = map(int,input().split())
#         test.move(x1,y1,x2,y2)