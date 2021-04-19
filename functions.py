import discord
import random
import pandas as pd

async def order_not_available(message):
	await message.channel.send('Cette fonction n\'est pas encore disponible. Peut-être dans la prochaine version du bot. :thinking: ')
	await message.channel.send(file=discord.File('inputs/images/work.gif'))
	return

def is_an_order(message):
    if 'belle' in message.content.lower():
        return True
    if 'assis' in message.content.lower():
        return True
    if 'check' in message.content.lower() or 'high five' in message.content.lower():
        return True
    if 'patte' in message.content.lower():
        return True
    if 'couché' in message.content.lower():
        return True
    return False

async def apply_order(message):
    if random.randrange(100) < 10:
        if random.randrange(100) < 50:
            await message.channel.send('*Ohana t\'ignore*', file=discord.File('inputs/images/osef_2.jpg'))
        else:
            await message.channel.send('*Ohana préfère jouer que t\'écouter*', file=discord.File('inputs/images/osef.jpg'))
        return
    if 'belle' in message.content.lower():
        await message.channel.send('*Ohana fait la belle*', file=discord.File('inputs/images/belle.png'))
        return
    if 'assis' in message.content.lower():
        await message.channel.send('*Ohana s\'assoit*', file=discord.File('inputs/images/assis.jpg'))
        return
    if 'check' in message.content.lower() or 'high five' in message.content.lower():
        await message.channel.send('*Ohana s\'assoit*', file=discord.File('inputs/images/check.jpg'))
        return
    if 'patte' in message.content.lower():
        await message.channel.send('*Ohana donne la patte*', file=discord.File('inputs/images/patte.jpg'))
        return
    if 'couché' in message.content.lower():
        await message.channel.send('*Ohana se couche*', file=discord.File('inputs/images/couche.jpg'))
        return

async def anecdote(message):
    file = open('inputs/txt/anecdotes.txt', "r")
    anecdotes = list()
    for line in file.readlines():
        if "#" not in line:
            anecdotes.append(line.strip())
    file.close()

    await message.channel.send('**Saviez-vous que :**')
    await message.channel.send(random.choice(anecdotes))


async def race(message):
    df_images_races_urls = pd.read_csv('inputs/csv/images.csv', delimiter="\t")
    df_temp = df_images_races_urls
    if 'chien' in message.content:
        df_temp = df_temp[df_temp['Espece'] == "chien"]
    if 'chat' in message.content:
        df_temp = df_temp[df_temp['Espece'] == "chat"]
    if 'cheval' in message.content:
        await message.channel.send('Je n\'ai pas d\'image de cheval. Pourtant ça doit faire 3 semaines que Cédric doit le faire ... ')
        return
    sample = df_temp.sample()
    message.channel.send('*Ohana montre une race au hasard :*')
    e = discord.Embed()
    e.set_image(url= list(sample['URL'])[0])
    await message.channel.send('**{}**'.format(list(sample['Name'])[0]), embed=e)