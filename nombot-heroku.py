import discord
import json, os, sys
import asyncpg, psycopg2

NOMS_FILE =  os.path.join(sys.path[0], 'noms.txt')

# connect to postgresql db for storing noms
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as {0.user}!'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('<nom '):
		user = message.mentions
		# TODO: allow nomming of multiple users
		nickname = str(user[0].nick).strip()
		msg_user_id = str(user[0].id).strip()

		with open(NOMS_FILE,'r+') as file:
			dict = json.load(file)

			for file_user_id, noms in dict.items():
				if str(file_user_id).strip() == msg_user_id:
					dict[file_user_id] = dict[file_user_id] + 1

			if msg_user_id not in dict:
				dict[msg_user_id] = 1 # new user has been nommed once

		with open(NOMS_FILE,'w') as file:
			json.dump(dict, file)

		await message.channel.send('<:nom:716879079894286376> {} has been nommed.'.format(nickname))


	if message.content.startswith('<unnom '):
		user = message.mentions
		nickname = str(user[0].nick).strip()
		msg_user_id = str(user[0].id).strip()

		with open(NOMS_FILE,'r+') as file:
			dict = json.load(file)
			for file_user_id, noms in dict.items():
				if str(file_user_id).strip() == msg_user_id:
					dict[file_user_id] = dict[file_user_id] - 1
					# disallow negative noms
					if dict[file_user_id] < 0:
						dict[file_user_id] = 0

		with open(NOMS_FILE,'w') as file:
			json.dump(dict, file)

		await message.channel.send('<:nom:716879079894286376> {} has been unnommed.'.format(nickname))


	if message.content.startswith('<noms'):
		listofnoms = ""

		cur.execute('SELECT * FROM public.noms')
		dict = json.dumps(cur.fetchall())
		for user_id, noms in dict.items():
			for user in message.guild.members:
				if str(user.id).strip() == str(user_id).strip():
					nickname = user.nick
					listofnoms = listofnoms + ("{}: {}".format(nickname, noms)) + "\n"
		await message.channel.send("List of <:nom:716879079894286376>s:\n" + listofnoms)

# TODO: random noms in #nom-spam

client.run(os.environ['RATS_NOM_TOKEN'])