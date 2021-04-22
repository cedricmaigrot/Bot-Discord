import discord

import commands
import talk
import quiz

messages_global = list()


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(name="Arrive sur le Discord", state="Arrive"))

@client.event
async def on_message(message):
    if not message.content.startswith('>') and message.author == client.user:
        return

    if 'ohana' in message.content.lower():
        await talk.comportement_ohana(message)

    if message.content.startswith('>'):
        await commands.commands(message, client)

import discordToken
client.run(discordToken.DISCORD_TOKEN)