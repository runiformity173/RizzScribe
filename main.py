import discord
from discord.ext import commands





#


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('/'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


client = Bot()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
# This example requires the 'message_content' privileged intent to function.

# @client.command()
# async def tic(ctx: commands.Context):
#     """Starts a tic-tac-toe game with yourself."""
#     await ctx.send('Tic Tac Toe: X goes first', view=Bot())


client.run('.'.join(['MTM2MTgyMzIxOTM4ODEyNTMxNA','G4ayHA','Ou219vOevrd-L9UG5vgexY5wgIP6GL4LK9p3mU']))