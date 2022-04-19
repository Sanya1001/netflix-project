import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# Input is a viewing history csv

def clean_history(viewing_history):
    split_titles_list = []

    for i in range(len(viewing_history)):
        split_title = viewing_history.iloc[i,0].split()
        split_titles_list.append(split_title)
    
    items_watched = len(split_titles_list)
    
    short_titles_list = []
    for i in range(items_watched):
        current_item = split_titles_list[i]
        words = len(current_item)
        j = 0
        while j < words:
            if ":" in current_item[j]:
                current_item[j] = current_item[j].replace(":", "")
                short_titles_list.append(current_item[0:j+1])
                j = words
                # If there is a colon, take only the words before the colon
            else:
                j += 1
                # Move to next word
            if (j == words-1) == True:
                short_titles_list.append(current_item[0:j+1])
                j = words
                # If there is no colon by the end of the word, take the whole title (it's a movie and doesn't need shortening)
                
    # Create list of unique titles (i.e. only one entry per series) and list of episodes of each series watched (movies will
    # only have one)
    # Number of episodes watched per series could be used to create a bias so we are more likely to reccomend items similar to
    # shows the viewer watched many episodes of instead of treating them equally to a single episode
    # Dummy check to make sure lengths match
    # We could combine these into a dictionary or 2D array if it makes life easier

    unique_titles = []
    for movie in short_titles_list:
        if movie not in unique_titles:
            unique_titles.append(movie)

    number_episodes = []
    for title in unique_titles:
        title_count = 0
        for title_2 in short_titles_list:
            if title == title_2:
                title_count += 1
        number_episodes.append(title_count)
        
    view_dates = []
    for i in range(len(viewing_history)):
        view_date_list = viewing_history.iloc[i,1].split("/")
        view_dates.append(view_date_list)

    days_since_viewing = []
    today = date.today()
    for j in range(len(view_dates)):
        view_date = date(int(view_dates[j][2])+2000, int(view_dates[j][0]), int(view_dates[j][1]))
        delta = today - view_date
        days_since_viewing.append(delta.days)
        
    average_days_since_viewing = []
    for title in unique_titles:
        duplicate_title_index_list = []
        for i in range(items_watched):
            if short_titles_list[i] == title:
                duplicate_title_index_list.append(i)
        days_since_viewing_all_duplicates = []
        for j in range(len(duplicate_title_index_list)):
            days_since_viewing_all_duplicates.append(days_since_viewing[duplicate_title_index_list[j]])
        avg = np.mean(days_since_viewing_all_duplicates)
        average_days_since_viewing.append(avg)
        
    return unique_titles, number_episodes, average_days_since_viewing