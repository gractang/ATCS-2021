import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# function to keep only necessary columns and write to csv
def cleanData(filepath_in, filepath_out, cols_keep):
	df_mess = pd.read_csv(filepath_in)
	df_mess.to_csv(path_or_buf=filepath_out, columns=cols_keep, index=False)

# returns a series of the fraction of republican reps per state for the given year
def get_frac_r(rd, yr):
	r_d_counts = rd[yr].str.split(":", n = 1, expand=True)
	r = pd.to_numeric(r_d_counts[0], errors="coerce")
	d = pd.to_numeric(r_d_counts[1], errors="coerce")
	return r / (r + d)

# returns series of average fraction of republican representatives per state
def get_avg_frac_r(filepath):
	rd = pd.read_csv(filepath)

	# get only the years, not the state names
	years = list(rd.columns)[1:]
	rd["avg_frac_r"] = 0

	# add together, div by # years
	for col in years:
		rd["avg_frac_r"] += (get_frac_r(rd, col))
	rd["avg_frac_r"] /= len(years)
	return rd[["state", "avg_frac_r"]]

def eval_color(row):
	return "red" if row["avg_frac_r"] > 0.5 else "blue"

# merges relevant data into one dataframe
def merge_all(df, mult):
	# group deaths and injuries by state, create new column with deaths and injuries
	df = df.groupby("state").sum()
	df["n_k_i"] = df["n_killed"] + df["n_injured"]

	# read in file with state abbreviations, merge
	abv = pd.read_csv("data/state_abbreviations.csv")
	df = pd.merge(df, abv, on="state")

	# read in population data, calc mean population, merge
	pop = pd.read_csv("data/state_populations.csv")
	pop["mean_pop"] = pop.mean(axis=1)
	df = pd.merge(df, pop[["state", "mean_pop"]], on="state")

	# calculate & make column for scaled killed, injured, combined
	df["scaled_killed"] = df["n_killed"] / df["mean_pop"] * mult
	df["scaled_injured"] = df["n_injured"] / df["mean_pop"] * mult
	df["scaled_n_k_i"] = df["n_k_i"] / df["mean_pop"] * mult


	df = pd.merge(df, get_avg_frac_r("data/Ratio R_D Seats by State.csv"), on="state")
	df["color"] = df.apply(eval_color, axis=1)

	return df

# ranks based on column, prints or writes
def rank_write(df, col, to_print=False, to_write=False, filepath=""):
	rank = df.sort_values(by=col, ascending=False)

	if to_print:
		print("ranking based on: " + col)
		print(rank)

	if to_write:
		rank.to_csv(path_or_buf=filepath, index=False)

	return rank

# ranks all the relevant things
def rank_stuff(df):
	# rank states based on original (unscaled) deaths and injuries
	orig_rank = rank_write(df, "n_k_i")

	# rank scaled
	scaled_rank = rank_write(df, "scaled_n_k_i")

	# rank deaths
	deaths_rank = rank_write(df, "n_killed")

	# rank scaled deaths
	scaled_deaths_rank = rank_write(df, "scaled_killed")

	# rank injuries
	injured_rank = rank_write(df, "n_injured")

	# rank scaled injuries
	scaled_injury_rank = rank_write(df, "scaled_injured")

#******************************************************

# initial cleaning process
# mess_fp = "dataRaw/gun-violence-data_01-2013_03-2018.csv"
# cols_keep = ["date", "state", "n_killed", "n_injured"]
# clean_data(mess_fp, clean_fp, cols_keep)

#******************************************************

pd.set_option("display.max_columns", None)

# read pre-cleaned data
clean_fp = "data/gun_violence_clean.csv"
df = pd.read_csv(clean_fp)

# how much to scale the data by. doesn't particularly matter.
mult = 10000
df = merge_all(df, mult)

#******************************************************

# stacked bar chart of number killed, number injured by state
fig, ax = plt.subplots()
labels = df["abbreviation"]
killed = df["n_killed"]
injured = df["n_injured"]
ax.bar(labels, killed, label="Number Killed", edgecolor="black", color="gray")
ax.bar(labels, injured, bottom=killed, label="Number Injured", edgecolor="black", color="lightgray")
ax.legend()
ax.set_title("Total Number Killed and Injured by State From 2013-2018")
ax.set_xlabel("State Abbreviation")
ax.set_ylabel("Total # People Killed and Injured")

#******************************************************

# stacked bar chart of number killed, number injured by state, scaled by population
fig, ax = plt.subplots()
s_killed = df["scaled_killed"]
s_injured = df["scaled_injured"]
ax.bar(labels, s_killed, label="Scaled Killed", edgecolor="black", color="gray")
ax.bar(labels, s_injured, bottom=s_killed, label="Scaled Injured", edgecolor="black", color="lightgray")
ax.legend()
ax.set_title("Number Killed and Injured by State From 2013-2018, Scaled by Population")
ax.set_xlabel("State Abbreviation")
ax.set_ylabel("Total # People Killed and Injured Scaled by Population")

#******************************************************

# various rankings by state
# rank_stuff(df)

#******************************************************

#print(df)

#******************************************************

# pie chart showing total # and scaled # of injuries and deaths
df1 = df.groupby("color").sum()[["n_killed", "n_injured", "n_k_i", "mean_pop"]]
ax = df1.plot(kind="pie", y="n_k_i", labels=df1.index, colors=["tab:blue", "tab:red", "tab:purple"], title="Total Injuries and Deaths by Political Affiliation", autopct='%1.1f%%')
ax.set_ylabel("")

df1["scaled_n_k_i"] = df1["n_k_i"] / df1["mean_pop"] * mult
ax = df1.plot(kind="pie", y="scaled_n_k_i", labels=df1.index, colors=["tab:blue", "tab:red", "tab:purple"], title="Scaled Injuries and Deaths by Political Affiliation", autopct='%1.1f%%')
ax.set_ylabel("")


#******************************************************

# scatter
ax = df.plot(kind="scatter", x="avg_frac_r", y="n_k_i", title="Number Killed and Injured vs Percent Republican", color="darkgray")

annotations=list(df["abbreviation"])
for i, label in enumerate(annotations):
    plt.annotate(label, (df["avg_frac_r"][i], df["n_k_i"][i]), fontsize=8)
ax.set_ylabel("Combined Number Killed and Injured")
ax.set_xlabel("Average Fraction of Republican Representatives")

# best fit line
m, b = np.polyfit(df["avg_frac_r"], df["n_k_i"], 1)
ax.plot(df["avg_frac_r"], m*df["avg_frac_r"]+b)


ax = df.plot(kind="scatter", x="avg_frac_r", y="scaled_n_k_i", title="Scaled Number Killed and Injured vs Percent Republican", color="darkgray")
for i, label in enumerate(annotations):
    plt.annotate(label, (df["avg_frac_r"][i], df["scaled_n_k_i"][i]), fontsize=8)
ax.set_ylabel("Combined Number Killed and Injured")
ax.set_xlabel("Average Fraction of Republican Representatives")

# best fit line
m, b = np.polyfit(df["avg_frac_r"], df["scaled_n_k_i"], 1)
ax.plot(df["avg_frac_r"], m*df["avg_frac_r"]+b)



plt.show()
#******************************************************
# misc. investigations
# investigation on Illinois since it had such a large number of injuries
# print(df.loc[df["state"] == "Illinois"].sort_values(by="n_injured"))
# print(df.loc[df["state"] == "Illinois"].sum())

# total incidents
# print(df["state"].value_counts())

#******************************************************
# TODO:
# do scatter: ratio vs # tot, # killed, # injured
#******************************************************