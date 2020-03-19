import os
from sys import argv

from Model import (
lemm, preprocess_data, TFIDF_fit_transform, GS_Model, take_input,
predict_artist_from_lyrics, run_model
)

from sklearn.naive_bayes import MultinomialNB

#Take command line interface argument from the user
namelist = argv[1:]

if __name__ == '__main__':
    take_input = predict_artist_from_lyrics(namelist, take_input = True)
    run_model(tv, m, le, 0.5, take_input)
