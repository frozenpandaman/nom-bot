import discord, json

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

		with open('noms.txt','r+') as file:
			dict = json.load(file)

			for file_user_id, noms in dict.items():
				if str(file_user_id).strip() == msg_user_id:
					dict[file_user_id] = dict[file_user_id] + 1

			if msg_user_id not in dict:
				dict[msg_user_id] = 1 # new user has been nommed once

		with open('noms.txt','w') as file:
			json.dump(dict, file)

		await message.channel.send('<:nom:716879079894286376> {} has been nommed.'.format(nickname))


	if message.content.startswith('<unnom '):
		user = message.mentions
		nickname = str(user[0].nick).strip()
		msg_user_id = str(user[0].id).strip()

		with open('noms.txt','r+') as file:
			dict = json.load(file)
			for file_user_id, noms in dict.items():
				if str(file_user_id).strip() == msg_user_id:
					dict[file_user_id] = dict[file_user_id] - 1
					# disallow negative noms
					if dict[file_user_id] < 0:
						dict[file_user_id] = 0

		with open('noms.txt','w') as file:
			json.dump(dict, file)

		await message.channel.send('<:nom:716879079894286376> {} has been unnommed.'.format(nickname))


	if message.content.startswith('<noms'):
		listofnoms = ""
		with open('noms.txt','r') as file:
			dict = json.load(file)
			for user_id, noms in dict.items():
				for user in message.guild.members:
					if str(user.id).strip() == str(user_id).strip():
						nickname = user.nick
						listofnoms = listofnoms + ("{}: {}".format(nickname, noms)) + "\n"
		await message.channel.send("List of <:nom:716879079894286376>s:\n" + listofnoms)

# TODO: random noms in #nom-spam

with open('token.txt','r') as f:
	line = f.readlines()
	token = line[0].strip()
client.run(token)