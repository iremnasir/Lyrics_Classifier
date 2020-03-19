import pandas as pd
import numpy as np
import spacy
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sys import argv
import spacy
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
import os
from Data_Scraping_func import (
create_artist_directory, create_artist_url, collect_artist_song_pages,
collect_song_urls, song_parsing )
from Songs2DF_func import (
text_dataframe_csv, merge_dataframes
)
warnings.filterwarnings('ignore')

spacy_model = spacy.load('en_core_web_md')
le = preprocessing.LabelEncoder()
tv = TfidfVectorizer()

def train_test(datafr, size_test):
    """ OPTIONAL Performs train/test split on the data """
    X_train, X_test, y_train, y_test = train_test_split(datafr,test_size=size_test, random_state=42)
    test = pd.concat([X_test, y_test], axis = 1)
    test.to_csv('Song_Test.csv')
    return X_train, y_train

def lemm(x, model):
    """ Lemmatize each word in a sentence"""

    clean = []
    tokens = model(x)
    for token in tokens:
        if not token.is_stop:
            clean.append(token.lemma_)
    return " ".join(clean)

def preprocess_data(datafr, x_tokenize_model, y_process_model):
    """Preprocesses training and target set """
    datafr['ydata'] = y_process_model.fit_transform(datafr['Artist'])
    datafr['Token'] = datafr['Lyrics'].apply(lemm, model=x_tokenize_model)
    X_train = datafr['Token']
    y_train = datafr['ydata']
    return X_train, y_train


def TFIDF_fit_transform(datafr, model_class):
    """ This is only done on X_train after tokenization"""
    vector = model_class.fit_transform(datafr)
    tv_train = pd.DataFrame(vector.todense()
    , columns = model_class.get_feature_names()) # dense because we save zeros
    return tv_train


def GS_Model(vectorized_df_Xtrain, y_train, param_range):
    """Perform grid search"""
    gs_model = MultinomialNB()
    gs_model_param = {'alpha': param_range}
    grid_m= GridSearchCV(gs_model,gs_model_param,cv=5)
    grid_m.fit(vectorized_df_Xtrain, y_train )
    ypred = grid_m.predict(vectorized_df_Xtrain)
    best_score = (grid_m.best_score_)
    print('Best score as a result of Grid Search is:',best_score, '\n',
    'Optimum grid search parameter is', grid_m.best_params_)
    return grid_m.best_params_['alpha']

def take_input():
    inp =input('Tell me a line from a song, I\'ll predict the artist!')
    new_song = [f'{inp}']
    return new_song

def run_model(model_class_vect, model_fit, label_encoder, prob_threshold, take_input):
    """
    OPTIONAL -> Take user input lyrics, perform prediction based on fit model
    print the artist depending on the threshold of probability set by user
    """
    if take_input == True:
        new_song = take_input()

    else: #This is for testing
        new_song = ['Dont let me get me']
    new_song_test = model_class_vect.transform(new_song)
    new_song_df = pd.DataFrame(new_song_test.todense(), columns=model_class_vect.get_feature_names())
    y_pred_test_song = model_fit.predict(new_song_df)

    probabilities = (model_fit.predict_proba(new_song_df)[0])
    if np.max(probabilities) >= prob_threshold:
        pred_artist = label_encoder.inverse_transform(y_pred_test_song)[0]
        print('This song is predicted to belong to', pred_artist)
    else:
        class_dict = dict(zip(label_encoder.classes_, probabilities))
        print('Results are inconclusive, the probabilies are: ', class_dict)
    return probabilities, take_input

def predict_artist_from_lyrics(namelist, take_input):
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

    return take_input

    #----------------------Take input-----------------------------------#

#    proba, take_input = run_model(tv, m, le, take_input)
