import discord
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient
import random
import requests
from core import danime

class DanimeAPI:
	def __init__(self, api_url):
		self.api_url = api_url


	def get_image(self, tag):
		return requests.get(f"{self.api_url}{tag}").json()['url']

	def get_many_images(self, tag, amount):
		return requests.get(f"{self.api_url}{tag}/{amount}").json()['urls']

	def get_hentai(self, id):
		return requests.get(f"{self.api_url}{doujin}/{id}").json()['url']

	def tag_dict(self, tag:str):
		dict = {
			"sfwneko" : "sneko",
			"sfwoppai" : "soppai",
			"sfwswimsuit" : "sswimsuit",
			"hairy" : "bush"
		}
		return dict[tag]

	def available_paths(self, mongo_url):
		availablePaths = mongo_url['AbodeDB']['1avialablepaths'].find_one({"_id" : 1})['available_paths']
		return availablePaths

	async def is_nsfw(self, ctx):
		embed = discord.Embed()
		embed.title= f"Non-NSFW channel detected!"
		embed.add_field(name="Why should you care?", value=f"Discord forbids the use of NSFW content outside the NSFW-option enabled channels. [More here](https://discord.com/guidelines#:~:text=You%20must%20apply%20the%20NSFW,sexualize%20minors%20in%20any%20way.)", inline=False)
		embed.add_field(name="How can I enable the NSFW channel option?", value=f"** **", inline=False)
		embed.set_image(url=f"https://cdn.discordapp.com/attachments/802518639274229800/802936914054610954/nsfw.gif")
		embed.set_footer(text=f"Pro tip: dh set_nsfw can do the work for you.")
		return await ctx.send(embed=embed) 


class auto(commands.Cog, name="auto"):
	def __init__(self, Bot: danime.Danime):
		self.Bot = Bot
		self.danime_api = DanimeAPI(self.Bot.api_url)
	

	@commands.group(pass_context=True)
	@commands.has_permissions(manage_webhooks=True)
	@commands.bot_has_permissions(manage_webhooks=True)
	async def autonsfw(self,ctx):
		if ctx.invoked_subcommand is None:
			helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
			await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
			await ctx.send_help(helper)


	@autonsfw.command(pass_context=True, usage = "dh autonsfw enable yuri 5",
		description = "Cool feature that allows you to receive hentai automatically.")
	@commands.has_permissions(manage_webhooks=True)
	@commands.bot_has_permissions(manage_webhooks=True)
	async def enable(self, ctx, tag:str="nsfw", time:int=1):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.is_nsfw(ctx)	
		try:
			#Checks the time and backs off it's over than 30
			if time != None and time > 30:
				return await ctx.send("Sorry mate but 30 is the limit.")
			if time == 0:
				time = 1

			##It's checking the tag if it exists or not, if not backs away
			if tag != None:
				try:
					tag = self.danime_api.tag_dict(tag)

				except:
					tag = tag

				try:
					checkUrl = f"{self.Bot.api_url}{tag}"
					r = requests.get(f"{checkUrl}").json()['url']
				except TypeError:
					return await ctx.send("Please provide a valid tag, you can see the tags from the help command.")
			
			channel = ctx.channel
			webhook = await channel.create_webhook(name="Danime | Autonsfw")
			webhook_url = webhook.url
			db =  self.Bot.db1['AbodeDB']
			collection= db['autonsfw']

			#premium thing
			# active = collection.find({"guild_id" : ctx.guild.id}).count()
			# if active >= 10:
			# 	return await ctx.send("A server can't have more than 10 active autonsfw plugins. Please remove one.")

			if (collection.find_one({"channel_id": channel.id})== None):
				if isinstance(time, int):
					data =  {
					"_id": webhook_url,
					"guild_id" : channel.guild.id,
					"channel_id" : channel.id,
					"tag" : tag,
					"time" : time
					}
				collection.insert_one(data)
				await ctx.send(f'The channel has been set to accept the AutoNSFW feature with tag `{tag}` and procces time `{time}` minute.')	
			else:
				await webhook.delete()
				await ctx.send("This channel alreay has the auto nsfw feature enabled. If you just removed the webhook then this won't work, join the support server and ask the staff to manually remove it.")
		
		except discord.Forbidden:
			await ctx.send("I may not have enough permissions to complete the follow operation, make sure I have manage_webhooks and manage_channel permissions available.")
		
		except discord.HTTPException:
			await ctx.send("It seems there are already 10 webhooks in this channel, please delete them by going to `edit channel > integrations > webhooks` and deleting the one which isn't used.")

		except Exception:
			await ctx.send("Hey, it seems you called the command incorrectly, use this command like : `dh autonsfw enable stockings 5`")
	

	@autonsfw.command(usage = "dh autonsfw disable", description="Disables autonsfw for the channel the command was used on.")
	@commands.has_permissions(manage_webhooks=True)    
	@commands.bot_has_permissions(send_messages=True)
	async def disable(self,ctx):
			db =  self.Bot.db1['AbodeDB']
			collection= db['autonsfw']
			search = collection.find({"channel_id" : ctx.channel.id})
			
			if search is None:
				return await ctx.send("No active autonsfw plugin found in this channel.")

			else:
				collection.delete_one({"channel_id": ctx.channel.id})
				return await ctx.send("Successfully removed the feature.")

	# @tasks.loop(seconds=60)
	# async def auto_send(self):
	# 	await self.Bot.wait_until_ready()
	# 	try:
	# 		if self.Bot.DEFAULT_PREFIX == "&":
	# 			return 
	# 		self.Bot.counter += 1
	# 		db = self.Bot.db1['AbodeDB']
	# 		collection= db['autonsfw']
	# 		available_paths = self.danime_api.available_paths(self.Bot.db2)
	# 		for path in available_paths:
	# 			color = random.choice(self.Bot.color_list)
	# 			specificSearch = collection.find({"tag" : path})
	# 			if specificSearch.count() == 0:
	# 				continue
	# 			specificLength =  specificSearch.count()
	# 			image_list = self.danime_api.get_many_images(path, specificLength)
	# 			for key, item in enumerate(specificSearch):
	# 				webhook_url =item["_id"]
	# 				setTime = item["time"]
	# 				setTag = item["tag"]
	# 				image = image_list[key]
	# 				embed =  discord.Embed(color =  color)
	# 				embed.set_image(url=f"{image}")
	# 				embed.description = f"Images powered by [Danime Bot]({self.Bot.invite})"
	# 				if self.Bot.counter % setTime == 0:
	# 					try:
	# 						self.Bot.loop.create_task(self.sendwebhook(collection = collection, webhook_url = webhook_url, embed = embed))
	# 					except:
	# 						continue
	# 	except ValueError:	
	# 		self.Bot.counter += 1
	# 		print("Couldn't send it")
	# 		pass
	# 	except:
	# 		self.Bot.counter += 1
	# 		pass

			
	# async def sendwebhook(self, collection, webhook_url, embed:discord.Embed):
	# 	try:
	# 		bot_avatar = "https://cdn.discordapp.com/attachments/790246681563889694/804058149504942080/Vien.png"
	# 		hook = discord.Webhook.from_url(webhook_url,adapter=discord.RequestsWebhookAdapter())
	# 		hook.send(embed=embed, avatar_url= bot_avatar)
	# 	except discord.NotFound:
	# 		collection.delete_one({"_id" : webhook_url})
	# 		print("Deleted")
	# 	except discord.HTTPException:
	# 		await self.removeimage(setTag, image)
	# 		print(f"Removed , {setTag} tag, url : {image}")

	# async def removeimage(self, tag, url ):
	# 	db = self.Bot.db2['AbodeDB']
	# 	collection = db[tag]
	# 	try:
	# 		collection.delete_one({"_id" : url})
	# 	except:
	# 		pass

def setup (Bot: danime.Danime) -> None:
	Bot.add_cog(auto(Bot))
	Bot.logger.info("Auto nsfw is working.")