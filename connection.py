import discord

import commands
import talk

messages_global = list()


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(name="Arrive sur le Discord", state="Arrive"))

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