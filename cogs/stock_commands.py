import discord
from discord.ext import commands
import yfinance as yf

class StockBasic(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def price(self, ctx, *, ticker):
		try:
			info = yf.Ticker(str(ticker).upper()).info
			sym = info['symbol']
			ask = info['ask']
			bid = info['bid']
			tradeable = info['tradeable']
			prevClose = info['previousClose']
			if tradeable:
				await ctx.send(f'{sym} - Ask: {ask} / Bid: {bid}')
			else:
				if bid == 0:
					await ctx.send(f'The market is currently closed. The previous closing price for {sym} is: {prevClose}')
				else:
					await ctx.send(f'The market is currently closed. {sym} - Ask: {ask} / Bid: {bid}')	
		except:
			await ctx.send(f'Unknown ticker {ticker}')

	@commands.command()
	async def name(self, ctx, *, ticker):	
		try:
			info = yf.Ticker(str(ticker).upper()).info
			name = info['longName']
			sym = info['symbol']
			await ctx.send(f'{sym} is {name}')
		except:
			await ctx.send(f'"{ticker}" is not a valid ticker')

	@commands.command()
	async def exloc(self, ctx, *, ticker):	
		try:
			info = yf.Ticker(str(ticker).upper()).info
			sym = info['symbol']
			exloc = info['exchangeTimezoneName']
			await ctx.send(f'{sym} is exchanged in {exloc}')
		except:
			await ctx.send(f'"{ticker}" is not a valid ticker')	

	@commands.command(aliases=['52high'])
	async def _52high(self, ctx, *, ticker):	
		try:
			info = yf.Ticker(str(ticker).upper()).info
			sym = info['symbol']
			high = info['fiftyTwoWeekHigh']
			await ctx.send(f'The 52 week high for {sym} is: {high}')
		except:
			await ctx.send(f'"{ticker}" is not a valid ticker')	
	
	@commands.command(aliases=['52low'])
	async def _52low(self, ctx, *, ticker):	
		try:
			info = yf.Ticker(str(ticker).upper()).info
			sym = info['symbol']
			low = info['fiftyTwoWeekLow']
			await ctx.send(f'The 52 week low for {sym} is: {low}')
		except:
			await ctx.send(f'"{ticker}" is not a valid ticker')

	@commands.command()
	async def summary(self, ctx, *, ticker):	
		try:
			info = yf.Ticker(str(ticker).upper()).info
			sym = info['symbol']
			summary = info['longBusinessSummary']
			await ctx.send(f'{summary}')
		except:
			await ctx.send(f'"{ticker}" is not a valid ticker')

	@commands.command()
	async def divrate(self, ctx, *, ticker):	
		try:
			info = yf.Ticker(str(ticker).upper()).info
			sym = info['symbol']
			div = info['dividendRate']
			div = 0 if div == None else div
			await ctx.send(f'{sym} dividend rate is: {div}%')
		except:
			await ctx.send(f'"{ticker}" is not a valid ticker')

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
	
	
	@commands.Cog.listener()
	async def on_ready(self):
		global data
		with open('data.json', 'r') as file:
			data = json.load(file)
		

	@commands.command()
	async def hello(self, ctx):
		if str(ctx.message.author.id) in data:
			await ctx.send('You have already registered!')
		else:
			data[str(ctx.message.author.id)] = []
			await ctx.send('Thank you for registering with Stonk Bot!')

	@commands.command()
	async def add(self, ctx, *, ticker):
		user_id = str(ctx.message.author.id)
		if user_id in data:
			if ticker.upper() in data[user_id]:
				await ctx.send(f'You already have {ticker.upper()} in your tracker.')
			else:
				try:
					info = yf.Ticker(str(ticker).upper()).info
					sym = info['symbol']
					data[str(ctx.message.author.id)].append(sym)
					print(data)
					await self.save_json()
					await ctx.send(f'Added {sym} to your tracker')
				except Exception as e:
					print(e)
					await ctx.send(f'"{ticker}" is not a valid ticker')
		else:
			await ctx.send('You are not registererd for Stonk Bot. Please use the .hello command!')

	@commands.command()
	async def mystocks(self, ctx):	
		for stock in data[str(ctx.message.author.id)]:
			await ctx.send(f'{stock}')

	async def save_json(self):
		with open('data.json', 'w') as outfile:
			json.dump(data, outfile)		

def setup(client):
	client.add_cog(StockBasic(client))