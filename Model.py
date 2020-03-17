import pandas as pd
import numpy as np
import spacy
import re

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler, NearMiss
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sys import argv
import warnings
warnings.filterwarnings('ignore')

def train_test(datafr, size_test):
    """ OPTIONAL Performs train/test split on the data """
    X_train, X_test, y_train, y_test = train_test_split(datafr[['Song_name','Lyrics', 'Artist']]
    , datafr['ydata'],test_size=size_test, random_state=42)
    test = pd.concat([X_test, y_test], axis = 1)
    test.to_csv('Song_Test.csv')
    return X_train, y_train

def lemm(x, model):
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
