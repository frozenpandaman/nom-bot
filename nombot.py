import discord
import json, os, sys
import asyncpg, psycopg2
import requests, random

# connect to postgresql db for storing noms
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

client = discord.Client()

def update_noms(dic, cur):
		newrows = []
		for key, value in dic.items():
			row = {"id": key, "noms": value}
			newrows.append(row)
		namedict = tuple(newrows)
		cur.executemany('INSERT INTO public.noms(id,noms) VALUES (%(id)s, %(noms)s)', namedict)

@client.event
async def on_ready():
	print('Logged in as {0.user}!'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	# NOM COMMAND
	if message.content.startswith('<nom '):
		users = message.mentions
		for user in users:
			try: # if role, etc. is mentioned - aka no nickname
				nickname = str(user.display_name).strip()
				msg_user_id = str(user.id).strip()

				cur = conn.cursor()
				cur.execute('SELECT * FROM public.noms')
				rows = cur.fetchall()
				dic = dict(rows)

				for file_user_id, noms in dic.items():
					if str(file_user_id).strip() == msg_user_id:
						dic[file_user_id] = dic[file_user_id] + 1

				if msg_user_id not in dic:
					dic[msg_user_id] = 1 # new user has been nommed once

				update_noms(dic, cur)
				cur.close()
				await message.channel.send('<:nom:716879079894286376> {} has been nommed.'.format(nickname))
			except:
				pass

	# UNNOM COMMAND
	elif message.content.startswith('<unnom '):
		users = message.mentions
		for user in users:
			try:
				nickname = str(user.display_name).strip()
				msg_user_id = str(user.id).strip()

				cur = conn.cursor()
				cur.execute('SELECT * FROM public.noms')
				rows = cur.fetchall()
				dic = dict(rows)

				for file_user_id, noms in dic.items():
					if str(file_user_id).strip() == msg_user_id:
						dic[file_user_id] = dic[file_user_id] - 1
						# disallow negative noms
						if dic[file_user_id] < 0:
							dic[file_user_id] = 0

				update_noms(dic, cur)
				cur.close()
				await message.channel.send('<:nom:716879079894286376> {} has been unnommed.'.format(nickname))
			except:
				pass

	# NOMS COMMAND
	elif message.content.lower() == "<noms":
		listofnoms = []

		cur = conn.cursor()
		cur.execute('SELECT * FROM public.noms')
		rows = cur.fetchall()
		cur.close()
		dic = dict(rows)
		for user_id, noms in dic.items():
			for user in message.guild.members:
				if str(user.id).strip() == str(user_id).strip():
					nickname = user.display_name # nickname if available
					listofnoms.append("{}: {}".format(nickname, noms))

		listofnoms = sorted(listofnoms, key=str.lower)
		await message.channel.send("List of <:nom:716879079894286376>s:\n" + "\n".join(listofnoms))

	# MESSAGE HAS NOM IN IT
	elif "nom" in message.content.lower():
		await message.channel.send('Nom.')

	# BUN COMMAND
	elif message.content.lower() == "<bun":
		buns = "https://www.reddit.com/r/rabbits/new.json?sort=new"
		r = requests.get(buns, headers={'User-Agent': 'nom bot/0.1'})
		data = r.json()
		bun_choices = []
		for post in data["data"]["children"]:
			if "i.redd.it" in post["data"]["url"]:
				bun_choices.append(post["data"]["url"])
		bun = random.choice(bun_choices)
		await message.channel.send(bun)

	# RESPOND TO BUN DM
	elif "bun" in message.content.lower():
		if message.channel.type == discord.ChannelType.private:
			buns = "https://www.reddit.com/r/rabbits/new.json?sort=new"
			r = requests.get(buns, headers={'User-Agent': 'nom bot/0.1'})
			data = r.json()
			bun_choices = []
			for post in data["data"]["children"]:
				if "i.redd.it" in post["data"]["url"]:
					bun_choices.append(post["data"]["url"])
			bun = random.choice(bun_choices)
			await message.author.send(bun)

	# trigger fishy command, for miso bot
	elif message.content.lower() == "fishy":
		await message.channel.send('>fishy')

	# voice channel party
	elif message.content.lower() == "<tok":
		author = message.author
		channel = author.voice_channel
		await bot.join_voice_channel(channel)


client.run(os.environ['RATS_NOM_TOKEN'])