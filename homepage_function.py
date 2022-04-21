import pandas as pd
import difflib

def MakeHomePage(history_path):
    hist = pd.read_csv(history_path)
    netflix = pd.read_csv("netflix_titles.csv")

    bestMatches = hist['Title'].apply(lambda x: difflib.get_close_matches(x, netflix['title']))

    genres = []
    for i in range(len(bestMatches)):
        itemGenres = []
        for j in range(len(bestMatches[i])):
            itemGenres.append(netflix['listed_in'].values[netflix['title'] == bestMatches[i][j]])
        genres.append(itemGenres)

    finalGenres = []
    for i in range(len(genres)):
        for j in range(len(genres[i])):
            for k in range(len(genres[i][j])):
                finalGenres += list(genres[i][j])

    genreCounts = pd.Series(finalGenres).value_counts()

    listOfGenres = list(genreCounts.keys())

    genresAndMovies = {}
    for i in range(netflix.shape[0]):
        if not genresAndMovies.get(netflix.iloc[i]['listed_in']):
            genresAndMovies[netflix.iloc[i]['listed_in']] = []
        genresAndMovies[netflix.iloc[i]['listed_in']].append(netflix.iloc[i]['title'])

    closeMovies = {}
    for i in range(10):
        key = listOfGenres[i]
        movies = genresAndMovies.get(key)
        closeMovies[key] = []
        listOfLists = list(hist["Title"].apply(lambda x: difflib.get_close_matches(x, movies)))
        for subList in listOfLists:
            closeMovies[key] += subList

    for key, value in closeMovies.items():
        print(key)
        print(list(pd.Series(value).value_counts().keys())[:20])
        print()