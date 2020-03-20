import os
from sys import argv

from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

import spacy
from Lyrics_Classifier.Data_Scraping_func import (collect_artist_song_pages, collect_song_urls,
                                create_artist_directory, create_artist_url,
                                song_parsing)
from Lyrics_Classifier.Model import (GS_Model, TFIDF_fit_transform, lemm, preprocess_data,
                   take_input)
from Lyrics_Classifier.Songs2DF_func import merge_dataframes, text_dataframe_csv

#Take command line interface argument from the user
namelist = argv[1:]

#----------- Instantiate Necessary Classes and Models----------------#
spacy_model = spacy.load('en_core_web_md')
le = preprocessing.LabelEncoder()
tv = TfidfVectorizer()

if __name__ == '__main__':
    loc = os.getcwd()
    os.chdir(loc)
    st_name = create_artist_directory(namelist)
    for name in st_name:
        if os.path.isfile(f'{name}.csv'):
            print (f"CSV File {name} exists")
        else:
            new_name = [name]
            print (f"{name}.csv file does not exist, fetching songs")
            print(new_name)
            artist_link = create_artist_url(new_name)
            print(artist_link)
            http_links=collect_artist_song_pages(artist_link)
            song_http = collect_song_urls(http_links)
            song_parsing(song_http)
            text_dataframe_csv(new_name, loc)

    df_lyrics_all = merge_dataframes(st_name) # merges the df
    X_train, y_train = preprocess_data(df_lyrics_all, spacy_model, le)
    tv_vector = TFIDF_fit_transform(X_train, tv)
    alpha_gs = GS_Model(tv_vector, y_train, [0.0001, 0.001, 0.1 ,1])
#------------------ MODEL TRAININIG -------------------#

    m = MultinomialNB(alpha = alpha_gs)
    m.fit(tv_vector, y_train)

#----------------------Take input-----------------------------------#

    take_input(tv, m, le, 0.5)
