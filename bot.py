import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
	print("READY")

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv('DISCORD_API_KEY'))