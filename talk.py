import os
import discord
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import pickle

import functions




async def comportement_ohana(message):
    if functions.is_an_order(message):
        await functions.apply_order(message)

    if 'anecdote' in message.content.lower():
        return

    if 'race' in message.content.lower():
        functions.race(message)
        return

    if message.content.lower().startswith('salut ohana'):
        await message.channel.send('Salut !')
        return

    if 'ohana' in message.content.lower():
        await message.channel.send('On parle de moi ?', file=discord.File('inputs/images/what.png'))
        return
