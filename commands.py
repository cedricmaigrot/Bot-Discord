import asyncio

import discord
import pandas as pd
import random

from discord import Color

import functions
import quiz


async def commands(message, client):
    if message.content.startswith('>help'):
        txt = ""
        txt += "**FONCTIONS D\'ANIMATION DU DISCORD**\n"
        txt += "-----------------------------------\n"
        txt += ':dog2: | **>ordre** : Donne un ordre à Ohana.\n'
        txt += '> Paramètres :\n'
        txt += '> *assis*, *couché* ou *patte* | Liste non exhaustive.A toi de trouver les autres :upside_down:.\n'
        txt += '> Exemple : **>ordre patte chien**\n'
        txt += ':frame_photo: | **>race** : affiche une race d\`une espèce aléatoire.\n'
        txt += '> Paramètres :\n'
        txt += '> *chien* :dog:, *chat* :cat: ou *cheval* :horse: | Permet de préciser l\'espèce dont la race tirée au sort est associée.\n'
        txt += '> Exemple : **>race chien**\n'
        txt += ':teacher: | **>anecdote** : affiche une anecdote sur les animaux.\n'
        txt += "\n"
        txt += "**FONCTIONS POUR LES QUIZ**\n"
        txt += "-----------------------------------\n"
        txt += ':question: | **>quiz** : commande globale pour toutes les commandes liées aux quiz.\n'
        txt += '> Paramètres :\n'
        txt += '> *planning* :calendar: | Affiche la liste des quiz avec leur date.\n'
        txt += '> *classement* :crown: | Affiche le classement en cours (mois courant).\n'
        txt += '> *rappel* :notepad_spiral: | Gestion de la liste des joueurs de quiz qui veulent un rappel 10 minutes avant les quiz.\n'
        txt += "\n"
        txt += "**FONCTIONS DE GESTION DU DISCORD**\n"
        txt += "-----------------------------------\n"
        # txt += ':bar_chart: **>utilisateurs** : affiche des statistiques sur les utilisateurs du Discord.\n'
        # txt += ':bar_chart: **>messages** : affiche des statistiques sur les messages postés sur le Discord.\n'
        # txt += ':calendar: **>algo** : affiche le lien vers le flowchart du bot.\n'
        txt += ':calendar: **>code** : affiche le lien vers la roadmap du bot.\n'
        txt += ':computer: **>data** : regénère les fichiers de données pour mettre à jour les statistiques.\n'
        await message.channel.send(txt)

    if message.content.startswith('>test'):
        commands = ['>help',
                    '>race',
                    '>race chat',
                    '>race chien',
                    '>race cheval',
                    '>anecdote',
                    '>ordre assis',
                    '>ordre couché',
                    '>ordre patte',
                    '>ordre high five',
                    '>ordre belle',
                    '>utilisateur',
                    '>messages',
                    '>code',
                    '>data']
        for command in commands:
            await message.channel.send(command)
            await asyncio.sleep(1)

    # INTERACTIONS COMMANDS
    if message.content.startswith('>ordre'):
        await functions.apply_order(message)

    if message.content.startswith('>anecdote'):
        await functions.anecdote(message)

    if message.content.startswith('>race'):
        await functions.race(message)

    # QUIZ COMMANDS
    if message.content.startswith('>quiz planning'):
        import pandas as pd
        df = pd.read_excel("inputs/xlsx/planning.xlsx")

        def category(cat):
            if "Chien" in cat:
                return ":dog2:"
            if "Chat" in cat:
                return ":cat2:"
            if "Cheval" in cat:
                return ":racehorse:"
            if "Oiseau" in cat:
                return ":bird:"
            if "NAC" in cat:
                return ":rabbit2:"
            if "?" in cat:
                return ":interrobang:"
            return ":feet:"

        txt = "**QUIZ PASSÉS**\n"
        separator_added = False
        for id, row in df.iterrows():
            # Date	Titre	Catégorie
            ts = pd.to_datetime(str(row['Date']))
            date = ts.strftime('%d/%m/%Y')
            d, m, y = date.split("/")
            d = functions.rank_to_emote(d, type="date")
            m = functions.rank_to_emote(m, type="date")
            y = functions.rank_to_emote(y, type="date")

            import datetime
            if (ts > datetime.datetime.now() and not separator_added):
                txt += "**QUIZ FUTURS**\n"
                separator_added = True
            # txt += "{}/{}/{} : {} {}\n".format(d,m,y, row['Titre'], category(row['Catégorie']))
            txt += ":arrow_forward: {} {} : {}\n".format(category(row['Catégorie']), date, row['Titre'])
            if len(txt) > 1000:
                am = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)
                await message.channel.send(txt, allowed_mentions=am)
                txt = ""
        am = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)
        await message.channel.send(txt, allowed_mentions=am)

    if message.content.startswith('>question'):
        import pandas as pd
        df = pd.read_csv("inputs/csv/fci.csv",
                         delimiter="\t")
        l = list()
        for key, row in df.sample().iterrows():
            r = row
        while r['id'] in l:
            for key, row in df.sample().iterrows():
                r = row
        l.append(r['id'])
        id_b = r['id']
        name_b = r['name_fr']
        country_b = r['country']

        propositions = list()
        propositions.append(country_b)

        await message.channel.send("De quel pays provient la race : " + name_b.title())

        rows_same_country = df[df['country'] == country_b]
        rows_diff_country = df.merge(rows_same_country, how='outer', indicator=True).loc[
            lambda x: x['_merge'] == 'left_only']
        other_responses = rows_diff_country.sample(3)
        for key, row in other_responses.iterrows():
            propositions.append(row['country'].title())
        for p in propositions:
            await message.channel.send("- {}".format(p.title()))
        await message.channel.send(":star: Réponse : ||"+country_b.title()+"||")

    if message.content.startswith('>quiz classement'):
        quiz.prepare_csv()
        functions.create_podium()
        df_members = pd.read_csv("outputs/members.csv")

        def get_discriminator(author):
            return author.split("#")[-1]

        df_quizz = pd.read_csv("outputs/charts/classement.csv")
        df_quizz['discriminator'] = df_quizz.apply(lambda x: get_discriminator(x['Username']), axis=1)
        df_members['discriminator'] = df_members['discriminator'].astype(int)
        df_quizz['discriminator'] = df_quizz['discriminator'].astype(int)
        df = df_quizz.merge(df_members, how="left", suffixes=('_quizz', '_data'))
        await message.channel.send(file=discord.File('outputs/podium.png'))
        txt = "Classement du mois :\n"
        for key, row in df.head(10).iterrows():
            print(row['id'
                      ''])
            txt += "{}\n{} [<@{}>]\n:homes: {} |:1234: {}pts\n".format(functions.rank_to_emote(key + 1), row['display_name'].split("-")[0].strip(), row['id'],
                                                    row['refuge'], row['Points'])
            if len(txt) > 1000:
                am = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)
                await message.channel.send(txt, allowed_mentions=am)
                txt = ""
        am = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)
        await message.channel.send(txt, allowed_mentions=am)

        # await functions.order_not_available(message);

    if message.content.startswith('>bug'):
        from discord.utils import get
        user = get(message.guild.members, name="Cédric")
        if user:
            await user.send(content=message.author.name)
            await user.send(content=message.content)
        else:
            print("NON")

    if message.content.startswith('>quiz rappel'):
        await functions.order_not_available(message);

    # ADMIN COMMANDS
    if message.content.startswith('>algo'):
        await functions.order_not_available(message);

    if message.content.startswith('>utilisateurs'):
        # await functions.order_not_available(message);
        # return
        df = pd.read_csv("outputs/members.csv")
        cjs = df['refuge'].unique()
        cjs = sorted(cjs)
        roles = ['Administrateurs', 'Modérateurs', 'Responsables de refuge', 'Agents animaliers', 'Référents',
                 'Encadrants', 'Jeunes']
        colors = dict()
        colors['Administrateurs'] = Color.red()
        colors['Modérateurs'] = Color.orange()
        colors['Responsables de refuge'] = Color.green()
        colors['Agents animaliers'] = Color.teal()
        colors['Référents'] = Color.purple()
        colors['Encadrants'] = Color.blue()
        colors['Jeunes'] = Color.gold()
        colors['Non présentés'] = Color.dark_red()
        for cj in cjs:
            await message.channel.send(":map: **{}** :map:".format(cj))
            df_temp = df[df['refuge'] == cj]
            for role in roles:
                l = list()
                for key, row in df_temp[df_temp['top_role'] == role].iterrows():
                    l.append(row['display_name'])
                if len(l) > 0 :
                    l = sorted(l)
                    emeb = discord.Embed(title=role, description="\n".join(l), color=colors[role])
                    await message.channel.send(embed=emeb)

    if message.content.startswith('>messages'):
        import time
        start_time = time.time()

        await message.channel.send('Bien reçu ! Je vais compter les messages.')
        await message.channel.send('Je reviens dans quelques secondes ...')

        df = pd.read_csv("outputs/csv/messages.csv")

        import seaborn as sns
        top_five = df['channel'].value_counts().keys()[:5]
        df_temp = df[df['channel'].isin(top_five)]
        sns_plot = sns.catplot(y="channel", kind="count",
                               palette="pastel", edgecolor=".6",
                               data=df_temp)
        sns_plot.savefig("outputs/images/output.png")

        await message.channel.send('En tout, il y a {} messages.'.format(len(list(df['content']))))
        await message.channel.send('Répartition dans les salons :', file=discord.File('outputs/images/output.png'))
        await message.channel.send("J'ai trouvé ce résultat en %d secondes." % int(time.time() - start_time))
        return

    if message.content.startswith('>code'):
        await message.channel.send('Tu veux connaître les prochaines améliorations du bot ? Ca se passe ici !')
        await message.channel.send('https://github.com/cedricmaigrot/Discord_laSPA/projects/1')
        await message.channel.send(
            'Tu veux faire ton propre bot comme <@818564026237452350> ? Le code est en open source !')
        await message.channel.send(file=discord.File('inputs/images/work.gif'))

    if message.content.startswith('>data'):
        import time
        start_time = time.time()
        await message.channel.send('Bien reçu ! Je vais mémoriser les données.')
        await message.channel.send('Je reviens dans quelques secondes ...')
        for guild in client.guilds:
            if guild.name in "Clubs Jeunes SPA":
                # lst = list()
                # for channel in guild.channels:
                #     print("Channel : " + channel.name)
                #     try:
                #         hist = await channel.history(limit=20000).flatten()
                #         for h in hist:
                #             lst.append([h.activity, h.application, h.attachments, h.author, h.call, h.channel,
                #                         h.channel_mentions, h.clean_content, h.content, h.created_at, h.edited_at,
                #                         h.embeds, h.flags, h.guild, h.id, h.jump_url, h.mention_everyone, h.mentions,
                #                         h.nonce, h.pinned, h.raw_channel_mentions, h.raw_mentions, h.raw_role_mentions,
                #                         h.reactions, h.reference, h.role_mentions, h.stickers, h.system_content, h.tts,
                #                         h.type, h.webhook_id])
                #     except:
                #         pass
                # df_messages = pd.DataFrame(lst, columns=["activity", "application", "attachments", "author", "call",
                #                                          "channel", "channel_mentions", "clean_content", "content",
                #                                          "created_at", "edited_at", "embeds", "flags", "guild", "id",
                #                                          "jump_url", "mention_everyone", "mentions", "nonce", "pinned",
                #                                          "raw_channel_mentions", "raw_mentions", "raw_role_mentions",
                #                                          "reactions", "reference", "role_mentions", "stickers",
                #                                          "system_content", "tts", "type", "webhook_id"])
                # df_messages.to_csv("outputs/messages.csv")
                # df_messages.to_excel("outputs/messages.xlsx")
                # df_messages.to_html("outputs/messages.html")

                df_messages = pd.read_excel("outputs/messages.xlsx")

                lst = list()
                for member in guild.members:
                    print("Member : " + member.name)
                    lst.append([member.activities,
                                member.activity,
                                member.avatar,
                                member.avatar_url,
                                member.bot,
                                member.color,
                                member.colour,
                                member.created_at,
                                member.default_avatar,
                                member.default_avatar_url,
                                member.desktop_status,
                                member.discriminator,
                                member.display_name,
                                member.guild,
                                member.guild_permissions,
                                member.id,
                                member.joined_at,
                                member.mention,
                                member.mobile_status,
                                member.name,
                                member.nick,
                                member.pending,
                                member.premium_since,
                                member.public_flags,
                                member.raw_status,
                                member.roles,
                                member.status,
                                member.system,
                                member.top_role,
                                member.voice,
                                member.web_status])
                df_members = pd.DataFrame(lst, columns=["activities",
                                                        "activity",
                                                        "avatar",
                                                        "avatar_url",
                                                        "bot",
                                                        "color",
                                                        "colour",
                                                        "created_at",
                                                        "default_avatar",
                                                        "default_avatar_url",
                                                        "desktop_status",
                                                        "discriminator",
                                                        "display_name",
                                                        "guild",
                                                        "guild_permissions",
                                                        "id",
                                                        "joined_at",
                                                        "mention",
                                                        "mobile_status",
                                                        "name",
                                                        "nick",
                                                        "pending",
                                                        "premium_since",
                                                        "public_flags",
                                                        "raw_status",
                                                        "roles",
                                                        "status",
                                                        "system",
                                                        "top_role",
                                                        "voice",
                                                        "web_status"])

                def get_shelter(roles):
                    shelter = "Inconnu"
                    for role in roles:
                        r = discord.utils.get(guild.roles, id=role.id)
                        if "Club Jeunes" in r.name:
                            shelter = r.name
                            print(r.name)
                    return shelter

                df_members['refuge'] = df_members.apply(lambda x: get_shelter(x['roles']), axis=1)

                df_members.to_csv("outputs/members.csv")
                df_members.to_excel("outputs/members.xlsx")
                df_members.to_html("outputs/members.html")

                lst = list()
                for role in guild.roles:
                    print("Role : " + role.name)
                    lst.append([role.color,
                                role.colour,
                                role.created_at,
                                role.guild,
                                role.hoist,
                                role.id,
                                role.managed,
                                role.members,
                                role.mention,
                                role.mentionable,
                                role.name,
                                role.permissions,
                                role.position,
                                role.tags])
                df_roles = pd.DataFrame(lst,
                                        columns=["color", "colour", "created_at", "guild", "hoist", "id", "managed",
                                                 "members", "mention", "mentionable", "name", "permissions", "position",
                                                 "tags"])
                df_roles.to_csv("outputs/roles.csv")
                df_roles.to_excel("outputs/roles.xlsx")
                df_roles.to_html("outputs/roles.html")

                df_members['discriminator'] = df_members['discriminator'].astype(str)

                def get_discriminator(author):
                    name = "{}".format(author)
                    return name.split("#")[-1]

                df_messages['author_discriminator'] = df_messages.apply(lambda x: get_discriminator(x['author']),
                                                                        axis=1)
                df_messages['author_discriminator'] = df_messages['author_discriminator'].astype(str)

                df_merge = df_messages.merge(df_members,
                                             left_on='author_discriminator',
                                             right_on='discriminator',
                                             suffixes=('_messages', '_members'))
                df_merge = df_merge.merge(df_roles, left_on='top_role', right_on='name',
                                          suffixes=('', '_role'))

                # df_messages[(~df_messages['id'].isin(df_merge['id_messages']))]['author']
                df_merge.to_html("outputs/merge.html")
                df_merge.to_csv("outputs/merge.csv")
                df_merge.to_excel("outputs/merge.xlsx")

        await message.channel.send('C\'est fait !')
        await message.channel.send("J'ai fait cela en %d secondes." % int(time.time() - start_time))
        return
