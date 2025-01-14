import discord
from discord.ext import commands
import random
from random import randint
import datetime
from core import danime

class logs(commands.Cog, name="logs"):
	def __init__(self, Bot):
		self.Bot = Bot


	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		if self.Bot.DEFAULT_PREFIX == "&":
			return
		channel = self.Bot.get_channel(856785981575659530)
		embed = discord.Embed()
		embed.description = f"Joined `{guild.name} | {guild.id}` with `{guild.member_count}` members."
		embed.set_thumbnail(url = guild.icon_url)
		await channel.send(content = "<@427436602403323905>",embed=embed)
		for channel in guild.text_channels:
			if channel.permissions_for(guild.me).embed_links:
				embed = discord.Embed(color = 0xff4042)
				embed.description= f"Thanks alot for inviting the bot to the server! The prefix is `dh `. Join [support server]({self.bot.support}) if needed. Also check out our affiliations."
				embed.add_field(name="Affiliations", value=f"[HanimeHaven](https://discord.gg/U7AJBVaFVg)\n"
				                                        f"[HentaiDelight](https://discord.gg/9VbqMyVvP3)\n"
				                                        f"[Gradient](discord.gg/EWfcVq7KvV)\n")
				await channel.send(embed=embed)
				break
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		if self.Bot.DEFAULT_PREFIX == "&":
			return
		channel = self.Bot.get_channel(856786043834335232)
		await channel.send("<@427436602403323905>")
		embed = discord.Embed()
		embed.description = f"Left `{guild.name} | {guild.id}` with `{guild.member_count}` members."
		embed.set_thumbnail(url = guild.icon_url)
		await channel.send(embed=embed)

	@commands.Cog.listener()
	async def on_command_completion(self, ctx):
		
		if self.Bot.DEFAULT_PREFIX == "&":
			return
		r = random.randint(0, 15)
		if r == 3:
			embed = discord.Embed()
			lists = [f"Like the bot? Why not [invite]({self.Bot.invite}) it to more servers?"]
			embed.description = random.choice(lists)
			embed.set_image(url = "https://media.discordapp.net/attachments/856616125857005658/861922663966441472/imonceagain.jpg")
			await ctx.send(embed = embed, delete_after=10)
			
		if ctx.author.id == self.Bot.vein_id:
			return
		channel = self.Bot.get_guild(self.Bot.guild_id).get_channel(856616128347111444)
		embed= discord.Embed()
		embed.description=f"Completed command, ``{ctx.invoked_with}``"
		embed.add_field(name=f"User", value=f"Name: {ctx.author.name}\n"
				 							f"ID: {ctx.author.id}")
		embed.add_field(name=f"Guild", value=f"Name: {ctx.guild.name}\n"
											f"Id : {ctx.guild.id}", inline=False)
		embed.set_thumbnail(url=f"{ctx.author.avatar_url}")

		embed.add_field(name=f"Args", value=f"``{ctx.message.clean_content[2:]}``")
		
		await channel.send(embed=embed)

def setup (Bot: danime.Danime):
	Bot.add_cog(logs(Bot))
	Bot.logger.info("Logs cog is working.") 