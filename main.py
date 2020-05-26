# import necessary libraries to begin with:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob

#get the csv files
csv_files = glob("zippedData\\*.csv.gz")
print(csv_files)

#create data frames from each file to check the information and clean the data :
df_title_basics= pd.read_csv(csv_files[3])

#getting basic information of the dataframe:
print("df_title_basics.columns: \n", df_title_basics.columns, "\n\n")
print(df_title_basics.isna().sum(), "\n\n" )
print(df_title_basics.info(), "\n\n")
print(df_title_basics.shape, )

# cleaning the dataframe and comparing the results,
df_title_basics_clean=df_title_basics.dropna(subset=["genres"], how="any")
print(df_title_basics.shape)
print(df_title_basics.dropna(subset=["genres"], how="any").shape)

# to join datadrames, we match the column names we want to join on, in this data frame changing the primary_title to movie,
df_title_basics_clean.columns=["tconst", "movie", "original_title", "start_year", "runtime_minutes", "genres"]
print(df_title_basics_clean)

# writing a function to count genres and their number of accurance in the table:
def genre_count(df, col):
    genre_dict = {}
    for genres in df[col]:
        for genre in genres.split(","):
            if genre in genre_dict:
                genre_dict[genre] += 1
            else:
                genre_dict[genre] = 1

    return genre_dict


df_movies=pd.read_csv(csv_files[7])
print(df_movies)
print(df_movies.columns, "\n\n")
print(df_movies.isna().sum(), "\n\n" )
print(df_movies.info())

# clean the data frame and sort values of required column:
df_movies_clean=df_movies.drop(["Unnamed: 0","id","original_title","genre_ids"],axis=1, inplace=False)
movie_clean_sorted=df_movies_clean.sort_values("popularity",ascending=False).head(10)

# create a plot to show the top 10 popular movies name:
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

df_movie_budgets=pd.read_csv(csv_files[8])
#df_movie_budgets
print(df_movie_budgets.columns, "\n\n")
print(df_movie_budgets.isna().sum(), "\n\n" )
print(df_movie_budgets.info())

# convert dollors to int to sort the values based on the budget numbers:
movie_budgets_clean = df_movie_budgets.production_budget.str.replace(",", "").str.replace("$", "").astype(float)
domestic_gross_clean = df_movie_budgets.domestic_gross.str.replace(",", "").str.replace("$", "").astype(float)
worldwide_gross_clean = df_movie_budgets.worldwide_gross.str.replace(",", "").str.replace("$", "").astype(float)

#create a new data frame with the cleaned datas:
movie_net_clean=worldwide_gross_clean - movie_budgets_clean
frame={"movie":df_movie_budgets["movie"] ,"movie_budgets":movie_budgets_clean, "domestic_gross":domestic_gross_clean,"worldwide_gross":worldwide_gross_clean,"movie_net":movie_net_clean}
df_movie_budgets_clean=pd.DataFrame(frame)
#df_movie_budgets_clean

#now we join the two dataframes on movie columns:
pd_merge = pd.merge(df_title_basics_clean, df_movie_budgets_clean, how='inner', on="movie")
#pd_merge

# review the top 100 movies based on their net sales:
df_title_basics_budget=pd_merge.sort_values("movie_net", ascending=False).head(100)
#df_title_basics_budget

final_genre_count=genre_count(df_title_basics_budget,"genres")
print(final_genre_count)

#preparing elements of the bar chart from our dictionary:
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
#according to this graph adventure movies are more popular, we only consider the top 100 best selling movies

# increamental quantil movie budget
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
plt.title("The most ptofitable Genres based on movie budgets", fontsize=20)
plt.ylabel("Genre-Count", fontsize=20)
plt.ylabel("Movie-Genres", fontsize=20)
plt.legend(['Budget  0  $ 1400.0  to $ 4550000.0', 'Budget  1  $ 4550000.0  to $ 16000000.0',
            'Budget  2  $ 16000000.0  to $ 40000000.0','Budget  3  $ 40000000.0  to $ 425000000.0'], fontsize=13);
plt.show()
print(df2)


# another way of running the above code clock, without nested for loops:
q0 = pd_merge["movie_budgets"].quantile(0.0)
q1 = pd_merge["movie_budgets"].quantile(0.25)
q2 = pd_merge["movie_budgets"].quantile(0.5)
q3 = pd_merge["movie_budgets"].quantile(0.75)
q4 = pd_merge["movie_budgets"].quantile(1)
#print([q0, q1, q2, q3])

p1 = pd_merge[pd_merge.movie_budgets < q1]
p1_final_genre_count = genre_count(p1, "genres")

values_1 = []
labels_1 = []
for genre, count in p1_final_genre_count.items():
    labels_1.append(genre)
    values_1.append(count)

p2 = pd_merge[(pd_merge.movie_budgets > q1) & (pd_merge.movie_budgets <= q2)]
p2_final_genre_count = genre_count(p2, "genres")

values_2 = []
labels_2 = []
for genre, count in p2_final_genre_count.items():
    labels_2.append(genre)
    values_2.append(count)

p3 = pd_merge[(pd_merge.movie_budgets > q2) & (pd_merge.movie_budgets <= q3)]
p3_final_genre_count = genre_count(p3, "genres")

values_3 = []
labels_3 = []
for genre, count in p3_final_genre_count.items():
    labels_3.append(genre)
    values_3.append(count)

p4 = pd_merge[(pd_merge.movie_budgets > q3) & (pd_merge.movie_budgets <= q4)]
p4_final_genre_count = genre_count(p4, "genres")

values_4 = []
labels_4 = []
for genre, count in p4_final_genre_count.items():
    labels_4.append(genre)
    values_4.append(count)

# creating the bar chart for movie-budget ranges:
plt.figure(figsize=(30,15))
x=np.arange(23)
plt.bar(labels_1, values_1, color="r", width=0.7, label=" budget < $4550000.0")
plt.bar(labels_2,values_2, color="g", width=0.5, label=" $4550000.0 < budget < $16000000.0")
plt.bar(labels_3, values_3, color="y", width=0.35, label=" $16000000.0 < budget < $40000000.0")
plt.bar(labels_4, values_4, color="b", width=0.15, label=" $40000000.0 < budget < $425000000.0")
plt.title("movie genres count based on the budget")
plt.ylabel("Genre-count")
plt.xticks(fontsize=7)
plt.legend(fontsize=11)
plt.show()

# creating the scatter chart for movie-budget ranges:
plt.figure(figsize=(30,15))
labels=labels_1[:21]
values=values_1[:21]
plt.scatter(labels,values,color="r",s=200,label=" budget < $4550000.0")
plt.scatter(labels_2,values_2,color="g",s=200,label=" $4550000.0 < budget < $16000000.0")
plt.scatter(labels_3,values_3,color="y",s=200,label=" $16000000.0 < budget < $40000000.0")
plt.scatter(labels_4,values_4,color="b",s=200,label=" $40000000.0 < budget < $425000000.0")
plt.title("The most ptofitable Genres based on movie budgets")
plt.ylabel("Genre-count")
plt.xticks(fontsize=8)
plt.legend(fontsize=11)
plt.show()

#exploring information regarding the movie crews by joining dataframes df_movies_clean and df_title_basics_budget:
df_movies_clean.columns=["original_language","popularity","release_date","movie","vote_average","vote_count"]
df_title_basics_budget_popularity=pd.merge(df_movies_clean, df_title_basics_budget, how="inner", on="movie")
df_title_basics_budget_popularity.head()

#next step working on the title crew table to see among those top movie genres, what producers/writers are most popular:
df_title_crew= pd.read_csv(csv_files[4])
print(df_title_crew.shape)
print(df_title_crew.dropna(subset=["directors","writers"], how="any").shape)
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

#ctreating a movie_crew dictionary to put all crews related to top movies
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
# print(a)
df_a = pd.DataFrame(list(a.items()), columns=['actor', 'count'])

best_actors = df_a.sort_values(by='count', ascending=False).head(20)
print(best_actors)
plt.figure(figsize=(20, 15))
plt.barh(best_actors["actor"], best_actors["count"])
plt.title("The most popular film-crews for top 20 profitable movies", fontsize=20)
plt.xlabel("number of paticipations in different roles for top 20 profitable movies", fontsize=15)
plt.show()