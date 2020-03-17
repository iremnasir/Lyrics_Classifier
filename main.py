from Data_Scraping_func import *
from Songs2DF_func import dataframe_artists, merge_dataframes
from Model import lemm, TFIDF_fit_transform, GS_Model
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np
from sklearn import preprocessing


model = spacy.load('en_core_web_md')
tv = TfidfVectorizer()

if __name__ == '__main__':
    loc = os.getcwd()
    os.chdir(loc)

    st_name = create_artist_directory(namelist)
    #song_parsing(st_name)
    dataframe_artists(st_name, loc) # creates individual dfs from each csv
    datafr = merge_dataframes(st_name) # merges the df


#------------------ TRAININIG - MAKE IT OPTIONAL -------------------#
    #Define train-test
    le = preprocessing.LabelEncoder()
    datafr['ydata'] = le.fit_transform(datafr['Artist'])
    datafr['Token'] = datafr['Lyrics'].apply(lemm, model=model)
    tv_vector = TFIDF_fit_transform(datafr['Token'], tv)
    y_train = datafr['ydata']
    alpha_gs = GS_Model(tv_vector, y_train, MultinomialNB, [0.0001, 0.001, 0.1 ,1])

    m = MultinomialNB(alpha = alpha_gs)
    m.fit(tv_vector, y_train)

#----------------------Take input-----------------------------------#

    inp =input('Tell me a line from a song, I\'ll predict the artist!')
    new_song = [f'{inp}']
    new_song_test = tv.transform(new_song)
    new_song_df = pd.DataFrame(new_song_test.todense(), columns=tv.get_feature_names())
    y_pred_test_song = m.predict(new_song_df)

    probabilities = (m.predict_proba(new_song_df)[0])
    if np.max(probabilities) >= 0.5:
        pred_artist = le.inverse_transform(y_pred_test_song)[0]
        print('This song is predicted to belong to', pred_artist)
    else:
        class_dict = dict(zip(le.classes_, probabilities))
        print('Results are inconclusive, the probabilies are: ', class_dict)
    #result_artist = m.predict_proba(max(new_song_df)[0])
    #print(result_artist)
    #if (m.predict_proba(new_song_df)).any >= 0.55:
    #    print('This song is written by:', y_pred_test_song)
    #else:
    #    print('I cannot conclude this with my training data')
