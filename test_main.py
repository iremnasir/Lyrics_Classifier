import pytest
from Lyrics_Classifier.Data_Scraping_func import (
create_artist_directory, create_artist_url, collect_artist_song_pages,
collect_song_urls, song_parsing
)
from Lyrics_Classifier.Songs2DF_func import text_dataframe_csv, merge_dataframes
import os
import shutil
import spacy
from Lyrics_Classifier.Model import lemm, preprocess_data, train_test
from sklearn import preprocessing


#------Data Scraping Tests ----------#


namelist = ['pearl-jam', 'pink']

def test_createfolder():
    """
    Assert for a given number of artists, folders are created
    and the newly formatted names are returned"""
    #remove the files if they are There
    for direc in namelist:
        try:
            shutil.rmtree(direc)
            print(f'{direc} removed')
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
    names_ = create_artist_directory(namelist)
    assert len(names_) == len(namelist)
    for name in namelist:
        assert os.path.isdir(f'./{name}')
    for direc in namelist:
        try:
            shutil.rmtree(direc)
            print(f'{direc} removed')
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))

#Test for creating artist urls

def test_create_artist_url():
    assert len(namelist) == len(artist_url)
    assert artist_url[1].count('pink') == 1

#Test for collecting collect_artist_song_pages
artist_url = create_artist_url(namelist)
def test_collect_song_pages_artist():
    song_http = collect_artist_song_pages(artist_url)
    assert len(song_http) >= len(artist_url)

# Test for collect_song_urls
song_http = collect_artist_song_pages(artist_url)
def test_collecting_song_url():
    song_url = collect_song_urls(song_http)
    assert song_url[0].count('pearl-jam') >= 1

#Test for parsing songs
URL = ['https://www.metrolyrics.com/alive-lyrics-pearl-jam.html']
def test_parse_song():
    create_artist_directory(['pearl-jam'])
    artist_name, song_name = song_parsing(URL)
    for file in os.listdir('./pearl-jam'):
        assert file.endswith('.txt')
    text_files = [f for f in os.listdir('./pearl-jam') if f.endswith('.txt')]
    assert len(text_files) == 1
    assert artist_name == 'pearl-jam'
    assert song_name == 'alive-lyrics-pearl-jam'
    #remove the folder created
    shutil.rmtree('pearl-jam')

# # Test dataframe conversion
def test_text_dataframe_csv():
    """ Tests if the songs are written into the dataframe,
    if omitted clauses still exists or not,
    if .csv is created """
    namelist = ['eric-clapton']
    loc = os.getcwd()
    df_ = text_dataframe_csv(namelist, loc)
    str_unf =  df_[df_['eric-clapton'].str.contains("Unfortunately, we are not authorized to show these lyrics")]
    assert len(str_unf) == 0
    assert os.path.isfile('./eric-clapton.csv') == True
    num_row = 0
    for row in open("./eric-clapton.csv"):
        num_row+=1
    assert num_row > 1

#Test Merge dataframes
def test_merge_df():
    df_all = merge_dataframes(['eric-clapton', 'pink'])
    assert len(df_all.groupby('Artist').count()) == 2

#Test train-test train_test_split
def test_tts():
    df_all = merge_dataframes(['eric-clapton', 'pink'])
    X_train, y_train = train_test(df_all, 0.2)
    assert len(X_train) == round(0.8 * len(df_all))

spacy_model = spacy.load('en_core_web_md')
le = preprocessing.LabelEncoder()

#Test preprocessing
def test_preprocessing():
    df_all = merge_dataframes(['eric-clapton', 'pink'])
    X_train, y_train = preprocess_data(df_all, spacy_model, le)
    assert X_train.shape[0] > 10
