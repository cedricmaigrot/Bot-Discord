import pandas as pd
df = pd.read_csv("/Users/cedricmaigrot/Google Drive/Chiens/Projets informatiques/data/csv/fci.csv", delimiter="\t")

l = list()

txt = list()
for key, row in df.sample().iterrows():
    r = row
while r['id'] in l:
    for key, row in df.sample().iterrows():
        r = row
l.append(r['id'])
id_b = r['id']
name_b = r['name_fr']
country_b = r['country']

txt.append("De quel pays provient la race : " + name_b.title())
txt.append(country_b.title())

rows_same_country = df[df['country'] == country_b]
rows_diff_country = df.merge(rows_same_country, how='outer', indicator=True).loc[
    lambda x: x['_merge'] == 'left_only']
other_responses = rows_diff_country.sample(3)
for key, row in other_responses.iterrows():
    txt.append(row['country'].title())


#     print(country_b, len(rows_same_country), len(rows_diff_country))

