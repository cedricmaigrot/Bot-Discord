import os
import discord
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import pickle


df_images_races_urls = pd.read_csv('inputs/csv/images.csv', delimiter="\t")


file = open('inputs/txt/anecdotes.txt', "r")
anecdotes = list()
for line in file.readlines():
    if "#" not in line :
        anecdotes.append(line.strip())
file.close()

def comportement_ohana(message):
    responses = list()
    if random.randrange(100) < 10:
        if random.randrange(100) < 50:
            responses.append(message.channel.send('*Ohana t\'ignore*', file=discord.File('inputs/images/osef_2.jpg')))
        else:
            responses.append(message.channel.send('*Ohana préfère jouer que t\'écouter*', file=discord.File('inputs/images/osef.jpg')))
        return responses

    if 'belle' in message.content.lower():
        responses.append(message.channel.send('*Ohana fait la belle*', file=discord.File('inputs/images/belle.png')))
        return responses

    if 'assis' in message.content.lower():
        responses.append(message.channel.send('*Ohana s\'assoit*', file=discord.File('inputs/images/assis.jpg')))
        return responses

    if 'check' in message.content.lower() or 'high five' in message.content.lower():
        responses.append(message.channel.send('*Ohana s\'assoit*', file=discord.File('inputs/images/check.jpg')))
        return responses

    if 'patte' in message.content.lower():
        responses.append( message.channel.send('*Ohana donne la patte*', file=discord.File('inputs/images/patte.jpg')))
        return responses

    if 'couché' in message.content.lower():
        responses.append( message.channel.send('*Ohana se couche*', file=discord.File('inputs/images/couche.jpg')))
        return responses

    if 'anecdote' in message.content.lower():
        responses.append( message.channel.send('**Saviez-vous que :**'))
        responses.append( message.channel.send(random.choice(anecdotes)))
        return responses

    if 'race' in message.content.lower():
        df_temp = df_images_races_urls
        if 'chien' in message.content:
            df_temp = df_temp[df_temp['Espece'] == "chien"]
        if 'chat' in message.content:
            df_temp = df_temp[df_temp['Espece'] == "chat"]
        if 'cheval' in message.content:
            responses.append( message.channel.send('Je n\'ai pas d\'image de cheval. Pourtant ça doit faire 3 semaines que Cédric doit le faire ... '))
            return responses
        sample = df_temp.sample()
        message.channel.send('*Ohana montre une race au hasard :*')
        e = discord.Embed()
        e.set_image(url= list(sample['URL'])[0])
        responses.append(message.channel.send('**{}**'.format(list(sample['Name'])[0]), embed=e))
        return responses

    if message.content.lower().startswith('salut ohana'):
        responses.append( message.channel.send('Salut !'))
        return responses

    if 'ohana' in message.content.lower():
        responses.append( message.channel.send('On parle de moi ?', file=discord.File('inputs/images/what.png')))
        return responses
