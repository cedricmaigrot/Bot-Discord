import urllib
from urllib.request import urlopen
from io import StringIO


import pandas as pd
df_members = pd.read_csv("outputs/members.csv")
def get_discriminator(author):
   return author.split("#")[-1]
df_quizz = pd.read_csv("outputs/charts/classement.csv")
df_quizz['discriminator'] = df_quizz.apply(lambda x: get_discriminator(x['Username']), axis=1)
df_members['discriminator'] = df_members['discriminator'].astype(int)
df_quizz['discriminator'] = df_quizz['discriminator'].astype(int)
df = df_quizz.merge(df_members, how="left", suffixes=('_quizz', '_data'))

pos = [[252,52], [92,92], [412,92]]
newsize = (100, 100)
urls = list()
for id, row in df.head(3).iterrows():
   urls.append(row['avatar_url'])


from PIL import Image, ImageDraw, ImageFilter

bg = Image.open('inputs/images/podium.png')

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}

import requests
for i in range(3):
   print(urls[i])
   with open('pic1.png', 'wb') as handle:
      response = requests.get(urls[i], stream=True)
      if not response.ok:
         print (response)
      for block in response.iter_content(1024):
         if not block:
            break
         handle.write(block)

   im = Image.open('pic1.png')
   im = im.resize(newsize)
   bg.paste(im, (pos[i][0],pos[i][1]))

bg.save('outputs/podium.png', quality=95)
