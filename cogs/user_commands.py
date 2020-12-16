import discord
from discord.ext import commands, tasks
import praw
from dotenv import load_dotenv
import os
import pickle
load_dotenv()

"""
This is a data container class for a search item
"""
class Search_item:
	def __init__(self, mention, subreddit, items, author_id, channel_id):
		self.mention = mention
		self.subreddit = subreddit
		self.items = items
		self.author_id = author_id
		self.channel_id = channel_id
		#the hash is used as a unique identifier for each search
		self.hash = self.my_hash(subreddit, items, author_id, channel_id)

	def my_hash(self, subreddit, items, author_id, channel_id):
		return abs(hash(str(subreddit) + str(items) + str(author_id) + str(channel_id)))


class User(commands.Cog):

	def __init__(self, client, reddit, data, post_ids):
		self.client = client
		self.reddit = reddit
		self.data = data
		self.post_ids = post_ids
		self.search_limit_int = 5
		


	@commands.Cog.listener()
	async def on_ready(self):
		
		# Waits for bot to cache all data
		await self.client.wait_until_ready()
		self.loop.start()  
		print('User commands loaded')

	"""
	Lets a user add a new search
	params: mention - weither the user wants to be @ mentioned. 'true', 't', and '1' will set to True, otherwise false
			subreddit - which subreddit is being searched
			items - all of the search terms seperated by commas
	"""
	@commands.command(aliases=['newsearch', 'ns'])
	async def new_search(self, ctx, mention='false', subreddit: str = 'discordapp', *, items=""):
		# Makes sure the user is registered
		if not await self.check_user(ctx):
			return

		# Formats the input	
		mention, subreddit, items = await self.parse(mention, subreddit, items)
		
		# Hash is used as a unique identifier for a search
		new_search_hash = await self.my_hash(subreddit, items, ctx.message.author.id, ctx.message.channel.id)
		
		# Prevents duplicate searches by a user
		if new_search_hash in self.post_ids:
			await ctx.send('This search is already running.')
			return

		
		user = str(ctx.message.author.id)
		# Creates new search item object
		new_search_obj = Search_item(mention, subreddit, items, ctx.message.author.id, ctx.message.channel.id)
		self.data[user]["searches"].append(new_search_obj) # Object is saved to the searches list for the user
		
		# Adds the hash post_ids list so it can track what posts it has looked at
		self.post_ids[new_search_hash] = []

		await ctx.send('Search has been added.')

		# Saves the current state of the data dictionary.
		# Data will presist through bot restarts
		await self.save_pickle()

	"""
	This command prints a list of searches the user has running
	"""	
	@commands.command(aliases=['mysearch', 'ms', 'list'])
	async def my_search(self, ctx):
		# Makes sure the user is registered
		if not await self.check_user(ctx):
			return

		user_id = str(ctx.message.author.id)
		ret = "```" # Format start of code string
		user_searches = self.data[user_id]["searches"]
		if not user_searches: # Checks for no searches
			await ctx.send(f'```0. No searches found```')
			return
		# Loop through all searches this user has	
		for i, search in enumerate(user_searches):
			ret += f'{i+1}. Subreddit: {search.subreddit}, Terms: {search.items}, Mention?: {search.mention}'
			ret += '\n'
		ret += "```" # Ends code block
		await ctx.send(ret)

	"""
	Lets a user remove one of their searches
	params: num (int) - the index number of the search the user wants to remove
	"""
	@commands.command(aliases=['removesearch', 'rs', 'remove'])
	async def remove_search(self, ctx, num=0):
		# Makes sure the user is registered
		if not await self.check_user(ctx):
			return

		# Converts string to int or returns
		try:
			num = int(num)
		except:
			await ctx.send('Please supply a valid number')
			return	

		user_id = str(ctx.message.author.id)	
		user_search_list = self.data[user_id]["searches"]
		if num > len(user_search_list) or num < 1: # Check validity of input index
			await ctx.send('No search found to remove')
			return
		else:
			# Pops search from the data dictionary and the post_id tracker
			removed_item = self.data[user_id]["searches"].pop(num-1)
			self.post_ids.pop(removed_item.hash)
			await ctx.send(f'Removed search:```{num}. Subreddit: {removed_item.subreddit}, Terms: {removed_item.items}, Mention?: {removed_item.mention}```')
			# Update the file with changes
			await self.save_pickle()

	"""
	This command adds a user to the data dictionary
	"""
	@commands.command()
	async def hello(self, ctx):
		if str(ctx.message.author.id) in self.data:
			await ctx.send('You have already registered!')
		else:
			await self.init_user(str(ctx.message.author.id))
			await ctx.send('Thank you for registering with Reddit Bot!')

	"""
	This command removes a user from data dict and all of their searches
	"""
	@commands.command()
	async def goodbye(self, ctx):
		if not await self.check_user(ctx):
			return
		user = str(ctx.message.author.id)
		for search in self.data[user]["searches"]:
			post_ids.pop(search.hash)
		self.data.pop(user)
		await self.save_pickle()
		await ctx.send('You have been deregistered from Reddit Bot.\nTo use user commands again, please run "!hello"')

	# Helper function to initalize user in dictionary	
	async def init_user(self, user_id):
		self.data[user_id] = {}
		self.data[user_id]["searches"] = []
		await self.save_pickle()

	"""
	Main function that loops. Loops through each search of each user and checks
	if there are new posts
	"""
	async def all_searches(self):
		for user in self.data:
			user_searches = self.data[user]["searches"]
			for search in user_searches:
				mention, subreddit, items = search.mention, search.subreddit, search.items # Params already formated
				for submission in self.reddit.subreddit(subreddit).new(limit=self.search_limit_int):
					if submission.id in self.post_ids[search.hash]: # If post has already been searched
						continue

					self.post_ids[search.hash].append(submission.id) # Add post_id to list
					# Keeps the post_ids list limited to 2*search_limit_int size
					if len(self.post_ids[search.hash]) > 2*self.search_limit_int:
						self.post_ids[searc.hash].pop(0) # Removes oldest

					# Format the title and body strings
					title = submission.title.lower()
					title = ''.join(title.split())
					body = submission.selftext.lower()
					body = ''.join(body.split())

					for keyword in items:
						if (keyword in title or keyword in body):
							# Create embed to be sent
							e = discord.Embed(
								title = (f'{submission.title[:256]}'),
								url = (f'{submission.url}')
								)
							channel = self.client.get_channel(search.channel_id)
				
							# @ mentions the user if they specified it, sends normally if not
							if mention:
								author = self.client.get_user(search.author_id)
								await channel.send("{} Keyword: '".format(author.mention) + keyword + "' was found", embed=e)
							else:
								await channel.send("Keyword: '" + keyword + "' was found", embed=e)
							break # Prevents re-searching of same post if a term is found


	async def my_hash(self, subreddit, items, author_id, channel_id):
		return abs(hash(str(subreddit) + str(items) + str(author_id) + str(channel_id)))

	"""
	Parses a search input and returns a formated and consistant version
	"""
	async def parse(self, mention, subreddit, items):
		# Removing all whitespace, lowercasing, and seperating
		items = items.lower()
		items = ''.join(items.split())
		items = items.split(",")
		subreddit = subreddit.lower()
		mention = mention.lower()

		# Morphs multiple string options to a bool
		if mention == 'true' or mention == 't' or mention == '1':
			mention = True
		else:
			mention = False
		return mention, subreddit, items

	# Helper function that checks if a user is already in the dictionary	
	async def check_user(self, ctx):
		if str(ctx.message.author.id) in self.data:
			return True
		else:	
			await ctx.send('You have not registered yet, please type "!hello"')
			return False
			
	# Main loop that calls all seaches function
	@tasks.loop(seconds=10)
	async def loop(self):
		await self.all_searches()

	# Helper function that saves the current data dictionary state to a pickle file
	async def save_pickle(self):
		with open('data.pkl', 'wb') as outfile:
			pickle.dump(self.data, outfile)


def setup(client):
	reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
				client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
				user_agent="my user agent")
	post_ids = {}
	# Read pickle file as dictionary
	with open('data.pkl', 'rb') as input:
		data = pickle.load(input)
	for user in data:
		for search in data[user]["searches"]:
			post_ids[search.hash] = []
	client.add_cog(User(client, reddit, data, post_ids))