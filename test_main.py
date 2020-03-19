import pytest
from Lyrics_Classifier.Data_Scraping_func import create_artist_directory, song_parsing
from Lyrics_Classifier.Songs2DF_func import dataframe_artists
import os

#------Data Scraping Tests ----------#

def test_createfolder():
    """
    Assert for a given number of artists, folders are created
    and the newly formatted names are returned"""
    namelist = ['pearl-jam', 'pink', 'd']
    names_ = create_artist_directory(namelist)
    assert len(names_) == len(namelist)
    for name in namelist:
        assert os.path.isdir(f'./{name}')

def test_song_parsing():
    """Check if every file has .txt
    and there is more than 1 text file"""
    namelist = ['pink']
    song_parsing(namelist)
    for file in os.listdir('./pink'):
        assert file.endswith('.txt')
    text_files = [f for f in os.listdir('./pink') if f.endswith('.txt')]
    assert len(text_files) > 1

# Test dataframe conversion
def test_dataframe_conversion():
    """ Tests if the songs are written into the dataframe,
    if omitted clauses still exists or not,
    if .csv is created """
    namelist = ['pink']
    loc = os.getcwd()
    df_ = dataframe_artists(namelist, loc)
    str_unf =  df_[df_['eric-clapton'].str.contains("Unfortunately, we are not authorized to show these lyrics")]
    assert len(str_unf) == 0
    assert os.path.isfile('./pink.csv') == True
    num_row = 0
    for row in open("./eric-clapton.csv"):
        num_row+=1
    assert num_row > 1
