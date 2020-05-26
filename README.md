# Module 1 Final Project Specifications

In this project, we will do some data analysis and presentation to explore what type of movies are currently doing the best at the box office and translate those findings into actionable insights that our client can use when deciding what type of movies they should produce.


## Dataset

For this project, we use some movie-related data from:

*Box Office Mojo
*IMDB
*Rotten Tomatoes
*TheMovieDB.org


## Insights

Q1: Categorize the top popular/profitable movies based on their genres.

Q2: Find the film-crew for the top profitable movies.

Q3: Categorize the top popular/profitable genres based on their investment budget.

Q4: Categorize the top popular/profitable genres based on their film crew.

Q5: With the available budget for our movie investment, what genre and what crew would be the best choice.


## Technical Aspect

To get to the question 5 which is the most practical result of our data analysis for our client, we need to answer all other questions by exploring our data sets, joining different tables and creating graphs.

1. In this project, Pandas DataFrame and matplotlib are **mainly** used for exploring and visualizing data.

2. Importing available data:

Use glob to import all the csv files:

```python
csv_files = glob("zippedData\\*.csv.gz")
```

3. Exploring data:

Creating dataframe from each file:

```python
df(i) = pd.read_csv(csv_files[i])
```

4. Getting basic information about each data frame.

5. Employing different data manipulation methods to clean  dataframes/tables,

6. Creating/joining different dataframes to combine multiple data sets.

7. Creating graphs to display the analysis outcomes,

![alt text](https://github.com/FarnazG/dsc-mod-1-project-v2-1-online-ds-ft-120919/blob/master/graphs/image.png "movie-budget")


According to this plot, for low budget movies(up to $ 40000000) **drama** is the recommended choice of genre, while for the higher budget movies **action** is the best choice.


The most popular film-crew for top 20 profitable movies:

![alt text](https://github.com/FarnazG/dsc-mod-1-project-v2-1-online-ds-ft-120919/blob/master/graphs/image.png "film-crew")