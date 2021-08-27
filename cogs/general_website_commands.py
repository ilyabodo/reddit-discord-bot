import discord
from discord.ext import commands, tasks
import hashlib
import bs4
from urllib.request import urlopen
import requests

class GeneralWebsiteUser(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		self.loop.start()
		print("READY")

	@commands.command()
	async def test(self, ctx):
		await ctx.send("hello")

	@tasks.loop(seconds=30)
	async def loop(self):
		try:
			for e in data:
				e = data[e]
				h = await get_hash(e['link'])
				if h == e['html_hash']:
					continue
				else:
					ctx = e['ctx']
					await ctx.send("{} ALERT! HTML HAS CHANGED: ".format(ctx.message.author.mention) + e['link'])
					e['html_hash'] = h

		except Exception as e:
			print(e)

	@commands.command()
	async def notif_add(self, ctx, link):
		user_id = ctx.message.author.id
		link_hash = hashlib.md5((link+str(user_id)).encode()).hexdigest()
		if link_hash in data:
			await ctx.send("Error - already added.")
			return
		h = await get_hash(link)
		if h == None:
			await ctx.send('Error - link needs to be in the form "https://example.com"')
			return
		data[link_hash] = {"ctx": ctx, "link": link, "html_hash": h}
		print(data[link_hash])
		print(data[link_hash]["html_hash"])
		await ctx.send("Website is now being monitored.")
		return

	async def get_hash(url):
		try:
			#source = urlopen(url).read().decode('utf-8')
			source = requests.get(url).content
			soup = bs4.BeautifulSoup(source, "html.parser")
			body = soup.find('body')
			h = hashlib.md5(body.encode()).hexdigest()
			return h
		except Exception as e:
			print(e)
			return None

	@commands.command()
	async def notif_remove_all(self, ctx):
		temp = "```Removed:\n"
		for e in list(data):
			g = e
			e = data[e]
			if e["ctx"].message.author.id == ctx.message.author.id:
				rem = data.pop(g)
				temp += e['link']
				temp += "\n"
		temp += "```"
		await ctx.send(temp)
		return

	@commands.command()
	async def notif_remove(ctx, link):
		user_id = ctx.message.author.id
		link_hash = hashlib.md5((link+str(user_id)).encode()).hexdigest()
		if link_hash in data:
			rem = data.pop(link_hash)
			await ctx.send("Removed " + link)
			return
		else:
			await ctx.send("Link doesn't exist in database")
			return
		return

	@commands.command()
	async def notif_list(self, ctx):
		temp = "```Monitored sites:\n"
		for e in data:
			e = data[e]
			if e["ctx"].message.author.id == ctx.message.author.id:
				temp += e['link']
				temp += "\n"
		temp += "```"
		await ctx.send(temp)
		return      

def setup(client):
	client.add_cog(GeneralWebsiteUser(client))