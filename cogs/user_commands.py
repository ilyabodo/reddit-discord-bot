import discord
from discord.ext import commands, tasks
import json
import praw
from dotenv import load_dotenv
import os
load_dotenv()

class User(commands.Cog):

	def __init__(self, client, reddit, data, sear, post_ids, user_searches):
		self.client = client
		self.reddit = reddit
		self.data = data
		self.sear = sear
		self.post_ids = post_ids
		self.user_searches = user_searches
		
	@commands.Cog.listener()
	async def on_ready(self):
		
		# starts the loop function that constantly searches for new posts
		self.test.start()  
		
		print('Ready')

	# Lets a user add a new search
	@commands.command(aliases=['newsearch', 'ns'])
	async def new_search(self, ctx, subreddit: str = 'discordapp', *, items):
		#creates a unique id number that can be reporduced later
		new_search_id = abs(hash(str(subreddit) + str(items) + str(ctx.message.author.id)))

		#Check if inputed search is already running
		if new_search_id in self.post_ids:
			await ctx.send('This search is already running.')
			return

		#Adds the search parameters to the list	
		self.sear[new_search_id] = []
		user_id = str(ctx.message.author.id)
		self.sear[new_search_id].append({'ctx': ctx,'subreddit': str(subreddit), 'terms': str(items), 'user': user_id})
		self.post_ids[new_search_id] = []
		
		self.user_searches[user_id].append(new_search_id)
		await ctx.send('Search has been added.')


	@commands.command(aliases=['removesearch', 'rs'])
	async def remove_search(self, ctx, subreddit: str = 'discordapp', *, items=' '):
		user_id = str(ctx.message.author.id)
		id = abs(hash(str(subreddit) + str(items) + user_id))
		if (user_id not in self.user_searches):
			await ctx.send('You have not registered, please use !hello')
			return
		if (id not in self.user_searches[user_id]):
			await ctx.send('No search found with those parameters.')
			return	
		self.user_searches[user_id].remove(id)
		self.sear.pop(id)
		self.post_ids.pop(id)
		await ctx.send('Search has been removed.')

	@commands.command(aliases=['mysearch', 'mysearches', 'my_searches', 'ms'])
	async def my_search(self, ctx):
		temp = []
		user_id = str(ctx.message.author.id)
		for x in self.user_searches[user_id]:
			temp.append([self.sear[x][0]['terms'], self.sear[x][0]['terms']])
		await ctx.send(temp)

	async def all_searches(self):
		global reddit
		for search in self.sear:
			keywords = self.sear[search][0]['terms'].split(',')
			for submission in self.reddit.subreddit(self.sear[search][0]['subreddit']).new(limit=5):
				if submission.id not in self.post_ids[search]:

					self.post_ids[search].append(submission.id)
					# Searches each post for each of the keywords
					for word in keywords:
						if (word.lower() in submission.title.lower() 
								or word.lower() in submission.selftext.lower()):
							e = discord.Embed(
								title = (f'{submission.title[:256]}'),
								url = (f'{submission.url}')
								)
							if self.data[self.sear[search][0]['user']][0]['mention'] == 'true':
								await self.sear[search][0]['ctx'].send("{} Keyword: '".format(self.sear[search][0]['ctx'].author.mention) + word + "' was found", embed=e)
							else:
								await self.sear[search][0]['ctx'].send("Keyword: '" + word + "' was found", embed=e)

	@tasks.loop(seconds=10)
	async def test(self):
		await self.all_searches()

	@commands.command()
	async def hello(self, ctx):
			if str(ctx.message.author.id) in self.data:
				await ctx.send('You have already registered!')
			else:
				await self.init_user(str(ctx.message.author.id))
				await ctx.send('Thank you for registering with Reddit Bot!')

	async def init_user(self, user_id):
		self.data[user_id] = []
		self.data[user_id].append({'mention': 'false'})
		await self.save_json(self.data, 'data.json')

	@commands.command()
	async def mention(self, ctx, mention):
		print(mention)
		m = str(mention).lower()
		if (m != 'false' and m != 'true'):
			await ctx.send('Please only use !mention True or !mention False')
			return
		user_id = str(ctx.message.author.id)	
		if user_id not in self.data:
			await ctx.send('You are not registererd for Reddit Bot. Please use the !hello command!')
			return
		else:
			self.data[user_id][0]['mention'] = m
			await self.save_json(self.data, 'data.json')
			temp = ' NOT' if m == 'false' else ''
			await ctx.send(f'Reddit Bot will{temp} @ mention you about found items.')

	async def save_json(self, data: {}, file: str):
			with open(file, 'w') as outfile:
				json.dump(data, outfile)

def setup(client):
	reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
				client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
				user_agent="my user agent")
	sear = {}
	post_ids = {}
	user_searches = {}
	with open('data.json', 'r') as file:
			data = json.load(file)
	for user in data:
		user_searches[user] = []		
	client.add_cog(User(client, reddit, data, sear, post_ids, user_searches))