import discord
from discord.ext import commands
import praw
from dotenv import load_dotenv
import os
load_dotenv()


client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	
	global reddit
	reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                     client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                     user_agent="my user agent")
	print("READY")

@client.command()
async def test(ctx):
	await ctx.send('testing compelte')

@client.command()
async def hot(ctx, subreddit, l='5'):
	try:
		submissions = reddit.subreddit(subreddit).hot(limit=int(l))
		e = discord.Embed(
			title = subreddit,
			url = 'https://reddit.com/r/' + subreddit
			)
		for x in submissions:
			e.add_field(name=x.title, value = x.url, inline = False)
		await ctx.send(embed=e)	
	except:
		await ctx.send("Either that subreddit doesn't exist, the number of posts is too high, or you formated the command wrong!")

@client.command()
async def new(ctx, subreddit, l='5'):
	try:
		submissions = reddit.subreddit(subreddit).new(limit=int(l))
		e = discord.Embed(
			title = subreddit,
			url = 'https://reddit.com/r/' + subreddit
			)
		for x in submissions:
			e.add_field(name=x.title, value = x.url, inline = False)
		await ctx.send(embed=e)	
	except:
		await ctx.send("Either that subreddit doesn't exist, the number of posts is too high, or you formated the command wrong!")		

client.run(os.getenv('DISCORD_API_KEY'))