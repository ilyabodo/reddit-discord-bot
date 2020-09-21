import discord
from discord.ext import commands, tasks
import praw
from dotenv import load_dotenv
import os
load_dotenv()

class Basic(commands.Cog):

	def __init__(self, client, reddit):
		self.client = client
		self.reddit = reddit

	@commands.command()
	async def hot(self, ctx, subreddit='discordapp', l='5'):
		try:
			submissions = self.reddit.subreddit(subreddit).hot(limit=int(l))
			e = discord.Embed(
				title = subreddit,
				url = 'https://reddit.com/r/' + subreddit
				)
			for x in submissions:
				e.add_field(name=x.title, value = x.url, inline = False)
			await ctx.send(embed=e)	
		except:
			await ctx.send("Either that subreddit doesn't exist, the number of posts is too high, or you formated the command wrong!")


	@commands.command()
	async def new(self, ctx, subreddit='discordapp', l='5'):
		try:
			submissions = self.reddit.subreddit(subreddit).new(limit=int(l))
			e = discord.Embed(
				title = subreddit,
				url = 'https://reddit.com/r/' + subreddit
				)
			for x in submissions:
				e.add_field(name=x.title, value = x.url, inline = False)
			await ctx.send(embed=e)	
		except:
			await ctx.send("Either that subreddit doesn't exist, the number of posts is too high, or you formated the command wrong!")

	@commands.command(aliases=['all', 'top_all'])
	async def topall(self, ctx, subreddit='discordapp'):
		try:
			submissions = self.reddit.subreddit(subreddit).top("all")
			e = discord.Embed(
				title = 'Top posts of all time on r/' + subreddit,
				url = 'https://reddit.com/r/' + subreddit + '/top/?t=all'
				)
			for x in submissions:
				e.add_field(name=x.title, value = x.url, inline = False)
			await ctx.send(embed=e)	
		except:
			await ctx.send("Either that subreddit doesn't exist, the number of posts is too high, or you formated the command wrong!")

	@commands.command(aliases=['year', 'top_year'])
	async def topyear(self, ctx, subreddit='discordapp'):
		try:
			submissions = self.reddit.subreddit(subreddit).top("year")
			e = discord.Embed(
				title = 'Top posts of the year on r/' + subreddit,
				url = 'https://reddit.com/r/' + subreddit + '/top/?t=year'
				)
			for x in submissions:
				e.add_field(name=x.title, value = x.url, inline = False)
			await ctx.send(embed=e)	
		except:
			await ctx.send("Either that subreddit doesn't exist, the number of posts is too high, or you formated the command wrong!")

	@commands.command(aliases=['month', 'top_month'])		
	async def topmonth(self, ctx, subreddit='discordapp'):
		try:
			submissions = self.reddit.subreddit(subreddit).top("month")
			e = discord.Embed(
				title = 'Top posts of the month on r/' + subreddit,
				url = 'https://reddit.com/r/' + subreddit + '/top/?t=month'
				)
			for x in submissions:
				e.add_field(name=x.title, value = x.url, inline = False)
			await ctx.send(embed=e)	
		except:
			await ctx.send("Either that subreddit doesn't exist, the number of posts is too high, or you formated the command wrong!")			

	@commands.command(aliases=['week', 'top_week'])
	async def topweek(self, ctx, subreddit='discordapp'):
		try:
			submissions = self.reddit.subreddit(subreddit).top("week")
			e = discord.Embed(
				title = 'Top posts of the week on r/' + subreddit,
				url = 'https://reddit.com/r/' + subreddit + '/top/?t=week'
				)
			for x in submissions:
				e.add_field(name=x.title, value = x.url, inline = False)
			await ctx.send(embed=e)	
		except:
			await ctx.send("Either that subreddit doesn't exist, the number of posts is too high, or you formated the command wrong!")	

	@commands.command(aliases=['day', 'top_day', 'top', 'today'])
	async def topday(self, ctx, subreddit='discordapp'):
		try:
			submissions = self.reddit.subreddit(subreddit).top("day")
			e = discord.Embed(
				title = 'Top posts of the day on r/' + subreddit,
				url = 'https://reddit.com/r/' + subreddit + '/top/?t=day'
				)
			for x in submissions:
				e.add_field(name=x.title, value = x.url, inline = False)
			await ctx.send(embed=e)	
		except:
			await ctx.send("Either that subreddit doesn't exist, the number of posts is too high, or you formated the command wrong!")	

	@commands.command(aliases=['hour', 'top_hour', 'now'])
	async def tophour(self, ctx, subreddit='discordapp'):
		try:
			submissions = self.reddit.subreddit(subreddit).top("hour")
			e = discord.Embed(
				title = 'Top posts of the hour on r/' + subreddit,
				url = 'https://reddit.com/r/' + subreddit + '/top/?t=hour'
				)
			for x in submissions:
				e.add_field(name=x.title, value = x.url, inline = False)
			await ctx.send(embed=e)
		except:
			await ctx.send("Either that subreddit doesn't exist, the number of posts is too high, or you formated the command wrong!")	

def setup(client):
	reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
					client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
					user_agent="my user agent")
	client.add_cog(Basic(client, reddit))