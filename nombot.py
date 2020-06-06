import discord
import json, os, sys
import asyncpg, psycopg2

NOMS_FILE =  os.path.join(sys.path[0], 'noms.txt')

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

	if message.content.startswith('<nom '):
		user = message.mentions
		# TODO: allow nomming of multiple users
		nickname = str(user[0].nick).strip()
		msg_user_id = str(user[0].id).strip()

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

	if message.content.startswith('<unnom '):
		user = message.mentions
		nickname = str(user[0].nick).strip()
		msg_user_id = str(user[0].id).strip()

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

	if message.content.startswith('<noms'):
		listofnoms = ""

		cur = conn.cursor()
		cur.execute('SELECT * FROM public.noms')
		rows = cur.fetchall()
		cur.close()
		dic = dict(rows)
		for user_id, noms in dic.items():
			for user in message.guild.members:
				if str(user.id).strip() == str(user_id).strip():
					nickname = user.nick
					listofnoms = listofnoms + ("{}: {}".format(nickname, noms)) + "\n"
		await message.channel.send("List of <:nom:716879079894286376>s:\n" + listofnoms)

# TODO: random noms in #nom-spam

client.run(os.environ['RATS_NOM_TOKEN'])