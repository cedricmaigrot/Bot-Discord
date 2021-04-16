import os
import discord
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import pickle

async def commands(message, client):
	if message.content.startswith('!utilisateurs'):
		await message.channel.send('Bien reçu ! Je vais inspecter les utilisateurs du Discord.')
		jeunes, encadrants, referents, autres = list(), list(), list(), list()
		for guild in client.guilds:
			if guild.name in "Clubs Jeunes SPA":
				for member in guild.members:
					r = list()
					for role in member.roles:
						r.append(role.name)
					has_a_role = False
					if "Référents" in r and not has_a_role:
						encadrants.append(member.name)
						has_a_role = True
					if "Encadrants" in r and not has_a_role:
						referents.append(member.name)
						has_a_role = True
					if "Jeunes" in r and not has_a_role:
						jeunes.append(member.name)
						has_a_role = True
					if not has_a_role:
						autres.append(member.name)
						has_a_role = True

				import matplotlib.pyplot as plt
				labels = 'Jeunes', 'Encadrants', 'Référents', 'Autres'
				sizes = [len(jeunes), len(encadrants), len(referents), len(autres)]
				explode = (0.1, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

				fig1, ax1 = plt.subplots()
				ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
						shadow=True, startangle=90)
				ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
				plt.savefig("outputs/images/chart.png")
				await message.channel.send(
					'Il y a : {} jeunes, {} encadrants, {} référents et {} autres personnes.'.format(len(jeunes),
																									 len(encadrants),
																									 len(referents),
																									 len(autres)),
					file=discord.File('outputs/images/chart.png'))

	if message.content.startswith('!messages'):
		import time
		start_time = time.time()

		await message.channel.send('Bien reçu ! Je vais compter les messages.')
		await message.channel.send('Je reviens dans quelques secondes ...')

		df = pd.read_csv("outputs/csv/messages.csv")

		import seaborn as sns
		top_five = df['channel'].value_counts().keys()[:5]
		df_temp = df[df['channel'].isin(top_five)]
		sns_plot = sns.catplot(y="channel", kind="count",
							   palette="pastel", edgecolor=".6",
							   data=df_temp)
		sns_plot.savefig("outputs/images/output.png")

		await message.channel.send('En tout, il y a {} messages.'.format(len(list(df['content']))))
		await message.channel.send('Répartition dans les salons :', file=discord.File('outputs/images/output.png'))
		await message.channel.send("J'ai trouvé ce résultat en %d secondes." % int(time.time() - start_time))
		return

	if message.content.startswith('!projets'):
		await message.channel.send('Tu veux faire ton propr veux connaître les prochaines fonctions qui arrivent ?')
		await message.channel.send('Jette un oeil ici  : https://github.com/cedricmaigrot/Discord_laSPA/projects/1',
							 file=discord.File('inputs/images/work.gif'))

	if message.content.startswith('!algo'):
		await message.channel.send('Tu veux savoir comment je pense ? :robot:')
		await message.channel.send('https://lucid.app/documents/view/a9109346-d490-4152-bafd-c8898eda02e2',
							 file=discord.File('inputs/images/robot.gif'))

	if message.content.startswith('!data'):
		import time
		start_time = time.time()
		await message.channel.send('Bien reçu ! Je vais mémoriser les données.')
		await message.channel.send('Je reviens dans quelques secondes ...')
		for guild in client.guilds:
			if guild.name in "Clubs Jeunes SPA":
				lst = list()
				for channel in guild.channels:
					print("Channel : " + channel.name)
					try:
						hist = await channel.history(limit=20000).flatten()
						for h in hist:
							lst.append([h.activity, h.application, h.attachments, h.author, h.call, h.channel,
										h.channel_mentions, h.clean_content, h.content, h.created_at, h.edited_at,
										h.embeds, h.flags, h.guild, h.id, h.jump_url, h.mention_everyone, h.mentions,
										h.nonce, h.pinned, h.raw_channel_mentions, h.raw_mentions, h.raw_role_mentions,
										h.reactions, h.reference, h.role_mentions, h.stickers, h.system_content, h.tts,
										h.type, h.webhook_id])
					except:
						pass
				df_messages = pd.DataFrame(lst, columns=["activity", "application", "attachments", "author", "call",
														 "channel", "channel_mentions", "clean_content", "content",
														 "created_at", "edited_at", "embeds", "flags", "guild", "id",
														 "jump_url", "mention_everyone", "mentions", "nonce", "pinned",
														 "raw_channel_mentions", "raw_mentions", "raw_role_mentions",
														 "reactions", "reference", "role_mentions", "stickers",
														 "system_content", "tts", "type", "webhook_id"])
				df_messages.to_csv("outputs/csv/messages.csv")
				df_messages.to_excel("outputs/xlsx/messages.xlsx")

				lst = list()
				for member in guild.members:
					print("Member : " + member.name)
					try:
						lst.append([member.activities,
									member.activity,
									member.avatar,
									member.avatar_url,
									member.bot,
									member.color,
									member.colour,
									member.created_at,
									member.default_avatar,
									member.default_avatar_url,
									member.desktop_status,
									member.discriminator,
									member.display_name,
									member.dm_channel,
									member.guild,
									member.guild_permissions,
									member.id,
									member.joined_at,
									member.mention,
									member.mobile_status,
									member.mutual_guilds,
									member.name,
									member.nick,
									member.pending,
									member.premium_since,
									member.public_flags,
									member.raw_status,
									member.relationship,
									member.roles,
									member.status,
									member.system,
									member.top_role,
									member.voice,
									member.web_status])
					except:
						pass
				df_members = pd.DataFrame(lst, columns=["activities",
														"activity",
														"avatar",
														"avatar_url",
														"bot",
														"color",
														"colour",
														"created_at",
														"default_avatar",
														"default_avatar_url",
														"desktop_status",
														"discriminator",
														"display_name",
														"dm_channel",
														"guild",
														"guild_permissions",
														"id",
														"joined_at",
														"mention",
														"mobile_status",
														"mutual_guilds",
														"name",
														"nick",
														"pending",
														"premium_since",
														"public_flags",
														"raw_status",
														"relationship",
														"roles",
														"status",
														"system",
														"top_role",
														"voice",
														"web_status"])
				df_members.to_csv("outputs/csv/members.csv")
				df_members.to_excel("outputs/xlsx/members.xlsx")

				lst = list()
				for role in guild.roles:
					print("Role : " + role.name)
					lst.append([role.color,
								role.colour,
								role.created_at,
								role.guild,
								role.hoist,
								role.id,
								role.managed,
								role.members,
								role.mention,
								role.mentionable,
								role.name,
								role.permissions,
								role.position,
								role.tags])
				df_roles = pd.DataFrame(lst,
										columns=["color", "colour", "created_at", "guild", "hoist", "id", "managed",
												 "members", "mention", "mentionable", "name", "permissions", "position",
												 "tags"])
				df_roles.to_csv("outputs/csv/roles.csv")
				df_roles.to_excel("outputs/xlsx/roles.xlsx")
				df_merge = df_messages.merge(df_members, left_on='author', right_on='name',
											 suffixes=('_messages', '_members'))

				df_merge = df_merge.merge(df_roles, left_on='top_role', right_on='name',
										  suffixes=('', '_roles'))
				df_merge.to_csv("outputs/csv/merge.csv")
				df_merge.to_excel("outputs/xlsx/merge.xlsx")
		await message.channel.send('C\'est fait !')
		await message.channel.send("J'ai fait cela en %d secondes." % int(time.time() - start_time))
		return