from Data_Scraping_func import *
from Songs2DF_func import dataframe_artists, merge_dataframes
from Model import *
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np
from sklearn import preprocessing

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
            print (f"{name}.csv file does not exist, fetching songs")
            song_parsing([name])
    dataframe_artists(st_name, loc) # creates individual dfs from each csv
    datafr = merge_dataframes(st_name) # merges the df
    X_train, y_train = preprocess_data(datafr, spacy_model, le)
    tv_vector = TFIDF_fit_transform(X_train, tv)
    alpha_gs = GS_Model(tv_vector, y_train, [0.0001, 0.001, 0.1 ,1])


#------------------ MODEL TRAININIG -------------------#

    m = MultinomialNB(alpha = alpha_gs)
    m.fit(tv_vector, y_train)

#----------------------Take input-----------------------------------#

    take_input(tv, m, le)
