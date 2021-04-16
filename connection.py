import os
import discord
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import pickle

import commands
import talk

messages_global = list()


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'ohana' in message.content.lower():
        for messages in talk.comportement_ohana(message):
            await messages
        return

    if message.content.startswith('!'):
        await commands.commands(message, client)

import discordToken
client.run(discordToken.DISCORD_TOKEN)

