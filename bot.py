import discord
from discord.ext import commands
from discord.ext import tasks
import praw
from dotenv import load_dotenv
import os
import contextlib
import requests
import time
import asyncio
import json
import secrets
load_dotenv()


client = commands.Bot(command_prefix = '!')

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
	global data
	with open('data.json', 'r') as file:
		data = json.load(file)

	global sear
	sear = {}
	global post_ids
	post_ids = {}
	test.start()
	print("READY")

@client.command()
async def new_search(ctx, subreddit: str = 'discordapp', *, items):
	new_search_id = abs(hash(str(subreddit) + str(items) + str(ctx.message.author.id)))
	if new_search_id in post_ids:
		await ctx.send('This search is already running.')
		return
	sear[new_search_id] = []
	sear[new_search_id].append({'ctx': ctx,'subreddit': str(subreddit), 'terms': str(items), 'user': str(ctx.message.author.id)})
	post_ids[new_search_id] = []
	print(sear)
	print(post_ids)

@client.command()
async def removesearch(ctx, subreddit: str = 'discordapp', *, items):
	try
		id = abs(hash(str(subreddit) + str(items) + str(ctx.message.author.id)))
		print(id)
		sear.pop(id)
		post_ids.pop(id)
		await ctx.send(f'Search has been removed.')
	except
		await ctx.send('No search found with those parameters.')

@client.command()
async def mysearch(ctx):
	temp = []
	for x in sear:
		if sear[x][0]['user'] == str(ctx.message.author.id):
			temp.append([sear[x][0]['subreddit'], sear[x][0]['terms']])
	await ctx.send(temp)		

async def all_searches():
	for search in sear:
		keywords = sear[search][0]['terms'].split(',')
		for submission in reddit.subreddit(sear[search][0]['subreddit']).new(limit=5):
			if submission.id not in post_ids[search]:

				post_ids[search].append(submission.id)
				# Searches each post for each of the keywords
				for word in keywords:
					if (word.lower() in submission.title.lower() 
							or word.lower() in submission.selftext.lower()):
						e = discord.Embed(
							title = (f'{submission.title[:256]}'),
							url = (f'{submission.url}')
							)
						if data[sear[search][0]['user']][0]['mention'] == 'true':
							await sear[search][0]['ctx'].send("{} Keyword: '".format(sear[search][0]['ctx'].author.mention) + word + "' was found", embed=e)
						else:
							await sear[search][0]['ctx'].send("Keyword: '" + word + "' was found", embed=e)

@tasks.loop(seconds=10)
async def test():
	await all_searches()


@client.command()
async def hello(ctx):
		if str(ctx.message.author.id) in data:
			await ctx.send('You have already registered!')
		else:
			await init_user(str(ctx.message.author.id))
			await ctx.send('Thank you for registering with Reddit Bot!')

async def init_user(user_id):
	data[user_id] = []
	data[user_id].append({'mention': 'false'})
	data[user_id].append({'orsearch': ''})
	print(data)
	await save_json()

@client.command()
async def mention(ctx, mention):
	print(mention)
	m = str(mention).lower()
	if (m != 'false' and m != 'true'):
		await ctx.send('Please only use !mention True or !mention False')
		return
	user_id = str(ctx.message.author.id)	
	if user_id not in data:
		await ctx.send('You are not registererd for Reddit Bot. Please use the !hello command!')
		return
	else:
		data[user_id][0]['mention'] = m
		save_json()
		print (data)
		temp = ' NOT' if m == 'false' else ''
		await ctx.send(f'Reddit Bot will{temp} @ mention you about found items.')


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

async def save_json():
		with open('data.json', 'w') as outfile:
			json.dump(data, outfile)	

client.run(os.getenv('DISCORD_API_KEY'))
