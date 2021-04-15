import pandas as pd
import time
import datetime

cpt = dict()


def preproc(x):
	return x.replace("'", "").split(" ")[0]

df_messages = pd.read_csv("messages.csv")
df_messages['created_at_day'] = df_messages['created_at'].apply(preproc)

def full_pseudo(x):
	return "{0}#{1:04d}".format(x['name'], (int)(x['discriminator']))
df_members = pd.read_csv("members.csv")
df_members['full-pseudo'] = df_members.apply (lambda row: full_pseudo(row), axis=1)

df_roles = pd.read_csv("roles.csv")


df_merge = df_messages.merge(df_members, how='left',
							 left_on='author', right_on='full-pseudo',
							 suffixes=('_messages', '_members'))

df_merge = df_merge.merge(df_roles, how='left',
						  left_on='top_role', right_on='name',
						  suffixes=('', '_roles'))

df_merge.to_excel("merge.xlsx")
