# Importing necessary libraries to begin with:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob

# Getting the csv files:
csv_files = glob("zippedData\\*.csv.gz")

####################################################################

# Creating data frames from each file to check the information and clean the data:

# df_title_basics
df_title_basics= pd.read_csv(csv_files[3])

# Getting basic information of the dataframe:
print("df_title_basics.columns: \n", df_title_basics.columns, "\n\n")
df_title_basics.isna().sum()
df_title_basics.info()
df_title_basics.shape

# Cleaning the data frame and comparing results:
df_title_basics_clean=df_title_basics.dropna(subset=["genres"], how="any")
df_title_basics.shape
df_title_basics.dropna(subset=["genres"], how="any").shape

# Changing column names from "primary_title" to "movie":
df_title_basics_clean.columns=["tconst", "movie", "original_title", "start_year", "runtime_minutes", "genres"]

####################################################################

# writing a function to count genres and their number of occurrence in the table:
def genre_count(df, col):
    genre_dict = {}
    for genres in df[col]:
        for genre in genres.split(","):
            if genre in genre_dict:
                genre_dict[genre] += 1
            else:
                genre_dict[genre] = 1

    return genre_dict

####################################################################

# df_movies
df_movies=pd.read_csv(csv_files[7])
df_movies.columns
df_movies.isna().sum()
df_movies.info()

# Cleaning the dataframe and sorting values of required column:
df_movies_clean=df_movies.drop(["Unnamed: 0","id","original_title","genre_ids"],axis=1, inplace=False)
movie_clean_sorted=df_movies_clean.sort_values("popularity",ascending=False).head(10)

# Creating a plot to show the top 10 popular movie names:
plt.figure(figsize=(30,10))
plt.style.use("fivethirtyeight")
plt.plot(movie_clean_sorted.title.head(10),movie_clean_sorted.popularity.head(10),color="r",label="most popular movies")
plt.legend(fontsize=20)
plt.title("10 most popular movies", fontsize=20)
plt.tight_layout()
plt.ylabel("Popularity-rate", fontsize=20)
plt.xlabel("Movie-names", fontsize=20)
plt.xticks(fontsize=10, rotation=25)
plt.yticks(fontsize=15)
plt.show()
#plt.savefig('Popularity-rate.png')

####################################################################

# df_movie_budgets
df_movie_budgets=pd.read_csv(csv_files[8])
df_movie_budgets.columns
df_movie_budgets.isna().sum()
df_movie_budgets.info()

# Converting dollars to int to sort values based on the budget numbers:
movie_budgets_clean = df_movie_budgets.production_budget.str.replace(",", "").str.replace("$", "").astype(float)
domestic_gross_clean = df_movie_budgets.domestic_gross.str.replace(",", "").str.replace("$", "").astype(float)
worldwide_gross_clean = df_movie_budgets.worldwide_gross.str.replace(",", "").str.replace("$", "").astype(float)

# Creating a new data frame with the cleaned data:
movie_net_clean=worldwide_gross_clean - movie_budgets_clean
frame={"movie":df_movie_budgets["movie"] ,"movie_budgets":movie_budgets_clean, "domestic_gross":domestic_gross_clean,"worldwide_gross":worldwide_gross_clean,"movie_net":movie_net_clean}
df_movie_budgets_clean=pd.DataFrame(frame)

# Joining two dataframes on movie columns:
pd_merge = pd.merge(df_title_basics_clean, df_movie_budgets_clean, how='inner', on="movie")

# Reviewing the top 100 movies based on their net sales:
df_title_basics_budget=pd_merge.sort_values("movie_net", ascending=False).head(100)

final_genre_count=genre_count(df_title_basics_budget,"genres")
final_genre_count

# Preparing elements of the bar chart from our dictionary:
values = []
labels = []

for genre, count in final_genre_count.items():
    labels.append(genre)
    values.append(count)

plt.figure(figsize=(25, 5))
plt.bar(labels,values)
plt.title("Genre counts for Top 100 profitable movies")
plt.ylabel("Genre-count")
plt.xticks(fontsize=8)
plt.show()

# Incremental quantile movie budget
total_genre = genre_count(pd_merge, "genres")
step = 4
total_genre_count = len(total_genre)
df2 = pd.DataFrame(np.zeros((total_genre_count, step)), index=total_genre.keys())

for q in range(0, step):
    start_q = pd_merge["movie_budgets"].quantile(q / step)
    end_q = pd_merge["movie_budgets"].quantile(q / step + 1.0 / step)
    print("Budget ", q, " $", start_q, " to $", end_q)

    p = pd_merge[(pd_merge.movie_budgets < end_q) & (start_q < pd_merge.movie_budgets)]
    p_genre_count = genre_count(p, "genres")

    for key, value in total_genre.items():
        if key in p_genre_count.keys():
            # print("genre: ", key, " : ", p_genre_count[key])
            df2.loc[key, q] = p_genre_count[key]

df2.plot(figsize=(35, 10), linewidth=4, fontsize=15)
plt.xticks(range(len(total_genre)), total_genre.keys(),fontsize=13, rotation=25)
plt.title("The most profitable Genres based on investment budgets", fontsize=20)
plt.ylabel("Genre-Count", fontsize=15)
plt.xlabel("Movie-Genres", fontsize=15)
plt.legend(['Budget  0  $ 1400.0  to $ 4550000.0', 'Budget  1  $ 4550000.0  to $ 16000000.0',
            'Budget  2  $ 16000000.0  to $ 40000000.0','Budget  3  $ 40000000.0  to $ 425000000.0'], fontsize=13);
plt.show()
df2

####################################################################

# Exploring information regarding the movie crews by joining dataframes df_movies_clean and df_title_basics_budget:
df_movies_clean.columns=["original_language","popularity","release_date","movie","vote_average","vote_count"]
df_title_basics_budget_popularity=pd.merge(df_movies_clean, df_title_basics_budget, how="inner", on="movie")
df_title_basics_budget_popularity.head()

# df_title_crew:
df_title_crew= pd.read_csv(csv_files[4])
df_title_crew.shape
df_title_crew.dropna(subset=["directors","writers"], how="any").shape
df_title_crew_clean = df_title_crew.dropna(subset=["directors","writers"], how="any")

df_title_principals=pd.read_csv(csv_files[5])
df_title_principals.dropna(subset=["tconst","nconst", "job"], how="any")
df_title_principals_clean=df_title_principals.drop(["ordering","characters"], axis=1, inplace=False)

merged_crew_principals=pd.merge(df_title_crew_clean,df_title_principals_clean,how="inner", on="tconst")

df_name_basics= pd.read_csv(csv_files[1])
df_name_basics.head(100)
df_name_basics.dropna(subset=["nconst","primary_name"], how="any")
df_name_basics_clean=df_name_basics.drop(["birth_year","death_year","known_for_titles"],axis=1, inplace=False)

merged_basic_principals=pd.merge(df_name_basics_clean,df_title_principals_clean,how="inner", on="nconst")

merged=pd.merge(merged_crew_principals,merged_basic_principals, how="inner", on=("tconst","nconst","job","category"))
merged_clean=merged.dropna(subset=["primary_profession"], how="any").drop(["job"],axis=1,inplace=False)

df=pd.merge(merged_clean,df_title_basics_budget,how="inner",on="tconst")
crew=df.sort_values('movie_net', ascending=False).head(1000)

# Ctreating a movie_crew dictionary to put all crews related to top movies
def crew_count(df, col):
    genre_dict = {}
    for genres in df[col]:
        for genre in genres.split(","):
            if genre in genre_dict:
                genre_dict[genre] += 1
            else:
                genre_dict[genre] = 1

    return genre_dict

a = crew_count(crew, "primary_name")
df_a = pd.DataFrame(list(a.items()), columns=['actor', 'count'])

best_actors = df_a.sort_values(by='count', ascending=False).head(20)
plt.figure(figsize=(20, 15))
plt.barh(best_actors["actor"], best_actors["count"])
plt.title("The most popular film-crews for top 20 profitable movies", fontsize=20)
plt.xlabel("number of paticipations in different roles for top 20 profitable movies", fontsize=15)
plt.show()