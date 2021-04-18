import os

import pandas as pd

def read_report(path, df_users):
	with open(path) as fp:
		lines = fp.readlines()
	quizz_id = lines[9].split("ID ")[-1].split(")")[0].strip()
	quizz_date = lines[5].split("time:")[-1].strip().split(" ")[0].split("-")
	if not os.path.exists(os.path.join("charts", quizz_id)):
		os.makedirs(os.path.join("charts", quizz_id))
	nombre_questions = lines[17].split("/")[-1].strip()
	numero_question = 1
	Quizz, Username,Answer,Time,Points = list(), list(), list(), list(), list()
	list_of_df_questions = list()
	for line in lines:
		if "### Question" in line:
			if len(Username)> 0:
				dict = {'Quizz': Quizz, 'Question': Question, 'Username': Username, 'Answer': Answer, 'Time': Time, 'Points': Points}
				df_question = pd.DataFrame(dict)
				df_question = df_users.merge(df_question, left_on='Id', right_on='Username')
				chart_classement(df_question, path=os.path.join("outputs/charts", quizz_id, "question_{:0>2d}.csv".format(numero_question)))
				list_of_df_questions.append(df_question)
			numero_question = (int)(line.split("### Question")[-1].split("/")[0])
			Quizz, Question, Username, Answer, Time, Points = list(), list(), list(), list(), list(), list()
		nombre_barres = len(line.split("|"))
		nombre_tirrets = len(line.split("-"))
		if nombre_barres == 6 and line.split("|")[1].strip() not in "Username" and nombre_tirrets < 30:
			reponse = line.split("|")
			Question.append(numero_question)
			Quizz.append(quizz_id)
			Username.append("#"+reponse[1].split("#")[-1].strip())
			Answer.append(reponse[2].strip())
			try:
				Time.append((float)(reponse[3].replace("0:00:", "")))
			except:
				Time.append(0)
			try:
				Points.append((int)(reponse[4]))
			except:
				Points.append(0)

	if len(Username)> 0:
		dict = {'Quizz': Quizz, 'Question': Question, 'Username': Username, 'Answer': Answer, 'Time': Time, 'Points': Points}
		df_question = pd.DataFrame(dict)
		df_question = df_users.merge(df_question, left_on='Id', right_on='Username')
		chart_classement(df_question,
						 path=os.path.join("outputs/charts", quizz_id, "question_{:0>2d}.csv".format(numero_question)))
		list_of_df_questions.append(df_question)
	df_fusion = pd.concat(list_of_df_questions)

	# df_fusion = df_users.merge(df_fusion, left_on='Id', right_on='Username')
	if not os.path.exists(os.path.join("outputs/charts", quizz_id)):
		os.makedirs(os.path.join("outputs/charts", quizz_id))
	chart_classement(df_fusion,
					 path=os.path.join("outputs/charts", quizz_id, "main.csv"))

	return quizz_id, quizz_date, df_fusion

def chart_nombre_bonnes_reponses(df, path="outputs/charts/nombre_bonnes_reponses.csv"):
	x = df[df["Points"]>0].groupby(['Username'])['Points'].count().sort_values(ascending=False)
	x.to_csv(path)

def chart_moyenne_points_par_question(df, path="outputs/charts/moyenne_points_par_question.csv"):
	x = df[df["Points"]>0].groupby(['Username'])['Points'].mean().sort_values(ascending=False)
	x.to_csv(path)

def chart_moyenne_temps(df, path="outputs/charts/moyenne_temps.csv"):
	x = df[df["Time"]>0].groupby(['Username'])['Time'].mean().sort_values(ascending=False)
	x.to_csv(path)

def chart_moyenne_temps_bonnes_reponses(df, path="outputs/charts/moyenne_temps_bonnes_reponses.csv"):
	df_temp = df[df["Time"]>0]
	x = df_temp[df_temp["Points"]>0].groupby(['Username'])['Time'].mean().sort_values(ascending=False)
	x.to_csv(path)

def chart_joueurs_par_refuge(df, path="outputs/charts/joueurs_par_refuge.csv"):
	x = df.groupby(['CJ'])['Username'].nunique().sort_values(ascending=False)
	x.to_csv(path)


def chart_classement(df, path="outputs/charts/classement.csv"):
	x = df.groupby(['Username', 'CJ'])['Points'].sum().sort_values(ascending=False)
	x.to_csv(path)

def chart_classement_par_refuge(df, path="outputs/charts/classement_par_refuge.csv"):
	x = df.groupby(['CJ'])['Username'].nunique().sort_values(ascending=False)
	list_refuges = list()
	list_points = list()
	for key in x.keys():
		if x[key] >=2 :
			df_temp = df[df["CJ"].str.match(key)]
			y = df_temp.groupby(['Username'])['Points'].sum().sort_values(ascending=False)
			summ = 0
			for key_ in y.keys()[:2]:
				summ += y[key_]
			list_refuges.append(key)
			list_points.append(summ)
		else :
			df_temp = df[df["CJ"].str.match(key)]
			y = df_temp.groupby(['Username'])['Points'].sum().sort_values(ascending=False)
			summ = 0
			for key_ in y.keys():
				summ += y[key_]
			list_refuges.append(key)
			list_points.append(summ)
	dict = {'CJ': list_refuges, 'Points': list_points}
	df_final = pd.DataFrame(dict)
	df_final.sort_values(by="Points")
	df_final.to_csv(path)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def prepare_csv():
	for root, dirs, files in os.walk("inputs/Liste_membres"):
		for file in files:
			list_of_ids = list()
			list_of_users = list()
			list_of_urls = list()
			list_of_roles = list()
			list_of_kennels = list()
			list_of_club = list()
			list_of_colors = list()
			list_of_date_joined = list()
			list_of_date_created = list()
			file1 = open(os.path.join(root, file), 'r')
			for line in file1.readlines():
				items = line.strip().split(";")
				if len(items) >3:
					# ID
					list_of_ids.append(items[3])
					# COLORS
					list_of_colors.append(items[5])
					# DATE JOINED
					list_of_date_joined.append(items[7])
					# DATE CREATED
					list_of_date_created.append(items[8])
					# USER
					if len(items[2])>0:
						list_of_users.append(items[4].split(" - ")[0])
						list_of_kennels.append(items[4].replace(list_of_users[-1]+" - ", ""))
					else:
						list_of_users.append(items[0].split("#")[0])
						list_of_kennels.append("Inconnu")
					# URL
					list_of_urls.append(items[6].split("#")[-1])
					# ROLE
					roles = items[10:]
					role_given = False
					roles_order = ["Responsables de refuge", "Agents animaliers", "Référents", "Encadrants", "Jeunes"]
					for r in roles_order:
						if r in roles and not role_given:
							list_of_roles.append(r)
							role_given = True
					if not role_given:
						list_of_roles.append("Autre")

					# KENNEL
					has_a_role = False
					for role in roles:
						if "Club Jeunes" in role and not has_a_role:
							list_of_club.append(role)
							has_a_role = True
					if not has_a_role:
						list_of_club.append("Inconnu")

	dict = {'Id': list_of_ids, 'User': list_of_users,
			'URL': list_of_urls, 'Role': list_of_roles, 'Refuge': list_of_kennels,
			'CJ': list_of_club,
			'Date Joined' : list_of_date_joined,
			'Date Created' : list_of_date_created,
			'Color': list_of_colors}
	df_users = pd.DataFrame(dict)
	df_users.to_csv("outputs/charts/Info_users.csv")
	df_users.to_excel("outputs/charts/Info_users.xlsx")


	list_of_df_by_month = {}
	list_of_df = list()
	for root, dirs, files in os.walk("inputs/QUIZZ_reports"):
		for file in files:
			quizz_id, quizz_date, df_report = read_report(os.path.join(root, file), df_users)

			if "{}-{}".format(quizz_date[1],quizz_date[0]) not in list_of_df_by_month:
				list_of_df_by_month["{}-{}".format(quizz_date[1],quizz_date[0])] = list()
			list_of_df_by_month["{}-{}".format(quizz_date[1],quizz_date[0])].append(df_report)
			list_of_df.append(df_report)
	df = pd.concat(list_of_df)

	chart_moyenne_points_par_question(df)
	chart_moyenne_temps(df)
	chart_moyenne_temps_bonnes_reponses(df)

	chart_joueurs_par_refuge(df)

	chart_classement(df)
	chart_classement_par_refuge(df)
	for id in list_of_df_by_month:
		df_month = pd.concat(list_of_df_by_month[id])
		chart_nombre_bonnes_reponses(df, path="outputs/charts/nombre_bonnes_reponses_{}.csv".format(id))
		chart_classement(df_month, path="outputs/charts/classement_{}.csv".format(id))
		chart_classement_par_refuge(df_month, path="outputs/charts/classement_par_refuge_{}.csv".format(id))

