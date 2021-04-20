import pandas as pd
import seaborn as sns
import matplotlib as plt

#df = pd.read_excel("outputs/xlsx/members.xlsx")
#g = sns.catplot(y="top_role", kind="count", palette="ch:.25", data=df)
#g.set_xticklabels(rotation=15)

df = pd.read_csv("outputs/charts/classement.csv")
txt = ""
for key, row in df.iterrows():
	txt += "{:6d} pts\t<@{}>\n".format(row['Points'], row['Id'])

print(txt)