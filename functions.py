import discord
import random
import pandas as pd

async def order_not_available(message):
	await message.channel.send('Cette fonction n\'est pas encore disponible. Peut-être dans la prochaine version du bot. :thinking: ')
	await message.channel.send(file=discord.File('inputs/images/work.gif'))
	return

def rank_to_emote(r, type="rank") :
    str = "";
    if type in "rank" :
        number = "{:02}".format(r)
        if r == 1:
            str += ":crown:"
        else:
            str += ":blue_square:"
    else :
        number = "{:05}".format(r)
    for i in number:
        if i in "0":
            str += ":zero:"
        if i in "1":
            str += ":one:"
        if i in "2":
            str += ":two:"
        if i in "3":
            str += ":three:"
        if i in "4":
            str += ":four:"
        if i in "5":
            str += ":five:"
        if i in "6":
            str += ":six:"
        if i in "7":
            str += ":seven:"
        if i in "8":
            str += ":eight:"
        if i in "9":
            str += ":nine:"
    if type in "rank" :
        if r == 1:
            str += ":crown:"
        else:
            str += ":blue_square:"
    return str

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
    order_executed = False
    if random.randrange(100) < 10:
        order_executed = True
        if random.randrange(100) < 50:
            await message.channel.send('*Ohana t\'ignore*', file=discord.File('inputs/images/osef_2.jpg'))
        else:
            await message.channel.send('*Ohana préfère jouer que t\'écouter*', file=discord.File('inputs/images/osef.jpg'))
        return
    if 'belle' in message.content.lower():
        order_executed = True
        await message.channel.send('*Ohana fait la belle*', file=discord.File('inputs/images/belle.png'))
        return
    if 'assis' in message.content.lower():
        order_executed = True
        await message.channel.send('*Ohana s\'assoit*', file=discord.File('inputs/images/assis.jpg'))
        return
    if 'check' in message.content.lower() or 'high five' in message.content.lower():
        order_executed = True
        await message.channel.send('*Ohana s\'assoit*', file=discord.File('inputs/images/check.jpg'))
        return
    if 'patte' in message.content.lower():
        order_executed = True
        await message.channel.send('*Ohana donne la patte*', file=discord.File('inputs/images/patte.jpg'))
        return
    if 'couché' in message.content.lower():
        order_executed = True
        await message.channel.send('*Ohana se couche*', file=discord.File('inputs/images/couche.jpg'))
        return
    await message.channel.send('*Ohana te regarde et ne comprend pas*', file=discord.File('inputs/images/couche.jpg'))

async def anecdote(message):
    df = pd.read_excel('inputs/xlsx/anecdotes.xlsx')
    s = df.sample()
    categorie = list(s['Espèce'])[0]
    titre = list(s['Titre'])[0]
    texte = list(s['Texte'])[0]
    await message.channel.send('**Catégorie : {}**'.format(categorie))
    await message.channel.send("{}".format(titre))
    if not pd.isna(texte) :
        await message.channel.send("*{}*".format(texte))


async def race(message):
    df_images_races_urls = pd.read_csv('inputs/csv/images.csv', delimiter=",")
    df_temp = df_images_races_urls
    if 'chien' in message.content:
        df_temp = df_temp[df_temp['Espece'] == "chien"]
    if 'chat' in message.content:
        df_temp = df_temp[df_temp['Espece'] == "chat"]
    if 'cheval' in message.content:
        df_temp = df_temp[df_temp['Espece'] == "cheval"]
    sample = df_temp.sample()
    await message.channel.send('*Ohana montre une race au hasard :*')
    e = discord.Embed()
    e.set_image(url= list(sample['URL'])[0])
    if 'cheval' in list(sample['Espece'])[0]:
        await message.channel.send('**{}** | *{}*'.format(list(sample['Race'])[0], list(sample['Categorie'])[0]), embed=e)
    else :
        await message.channel.send('**{}**'.format(list(sample['Race'])[0]), embed=e)