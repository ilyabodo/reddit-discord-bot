import discord
from discord.ext import commands
import praw
from dotenv import load_dotenv
import os
import requests
import time
import asyncio
load_dotenv()


client = commands.Bot(command_prefix = '.')

class Item:
	def __init__(self, title='', body='', ids=''):
		self.title = title
		self.body = body
		self.id = ids

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

@client.command()
async def lookfor(ctx, length: int = 3, mention: bool = False, subreddit: str = 'discordapp', *, items):

	keywords = items.split(',')
	items_list = list() # List to hold all the Items
	id_list = list()
	for x in range (10):
		for submission in reddit.subreddit(subreddit).new(limit=5):
			# More attributes/properties of each post can be gathered here
			entree = Item(submission.title, submission.selftext, submission.id)
			# Adds and prints any posts that havent already been recorded
			if submission.id not in id_list:
				items_list.append(entree)
				id_list.append(submission.id)
				# Searches each post for each of the keywords
				for word in keywords:
					if (word.lower() in entree.title.lower() 
							or word.lower() in entree.body.lower()):
						e = discord.Embed(
							title = (f'{submission.title}'),
							url = (f'{submission.url}')
							)
						if mention == True:
							await ctx.send("{} Keyword: '".format(ctx.author.mention) + word + "' was found", embed=e)
						else:
							await ctx.send("Keyword: '" + word + "' was found", embed=e)
		await asyncio.sleep(5)
	await ctx.send(f'Search for {items} in {subreddit} has ended.')	

client.run(os.getenv('DISCORD_API_KEY'))
