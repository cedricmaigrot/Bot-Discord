import discord




async def order_not_available(message):
	await message.channel.send('Cette fonction n\'est pas encore disponible. Peut-être dans la prochaine version du bot. :thinking: ')
	await message.channel.send(file=discord.File('inputs/images/work.gif'))
	return
