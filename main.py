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

def take_input():
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

if __name__ == '__main__':
    loc = os.getcwd()
    os.chdir(loc)
    st_name = create_artist_directory(namelist)
    for name in st_name:
        if os.path.isfile(f'{name}.csv'):
            print ("CSV File exists")
        else:
            print ("File does not exist")
            song_parsing(name)
    dataframe_artists(st_name, loc) # creates individual dfs from each csv
    datafr = merge_dataframes(st_name) # merges the df
    X_train, y_train = preprocess_data(datafr, spacy_model, le)
    tv_vector = TFIDF_fit_transform(X_train, tv)
    alpha_gs = GS_Model(tv_vector, y_train, [0.0001, 0.001, 0.1 ,1])


#------------------ MODEL TRAININIG -------------------#

    m = MultinomialNB(alpha = alpha_gs)
    m.fit(tv_vector, y_train)

#----------------------Take input-----------------------------------#

    take_input()
