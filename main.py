from Data_Scraping_func import *
from Songs2DF_func import dataframe_artists, merge_dataframes
from Model import lemm, TFIDF_fit_transform, GS_Model
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd

model = spacy.load('en_core_web_md')
tv = TfidfVectorizer()

if __name__ == '__main__':
    loc = os.getcwd()
    os.chdir(loc)

    st_name = create_artist_directory(namelist)
    dataframe_artists(st_name, loc)
    datafr = merge_dataframes(st_name)
    X_train, y_train = datafr[['Song_name','Lyrics', 'Artist']], datafr['ydata']
    X_train['Token'] = X_train['Lyrics'].apply(lemm, model=model)
    tv_vector = TFIDF_fit_transform(X_train['Token'], tv)
    alpha_gs = GS_Model(tv_vector, y_train, MultinomialNB, [0.0001, 0.001, 0.1 ,1])

# final fit_transform, this part can take user input
    #user input here use Argparse in the end
    #Train the model with GS parameters
    m = MultinomialNB(alpha = alpha_gs)
    m.fit(tv_vector, y_train)

    #Take input
    inp =input('Tell me a line from a song, I\'ll predict the artist!')
    new_song = [f'{inp}']
    new_song_test = tv.transform(new_song)
    new_song_df = pd.DataFrame(new_song_test.todense(), columns=tv.get_feature_names())
    y_pred_test_song = m.predict(new_song_df)
    print(m.predict_proba(new_song_df))
    # if max(m.predict_proba(new_song_df)) >= 0.6:
    #     print('This song is written by:', y_pred_test_song)
    # else:
    #     print('I cannot conclude this with my training data')
