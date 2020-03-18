import pytest
from Data_Scraping_func import create_artist_directory, song_parsing
from Songs2DF_func import dataframe_artists
import os

#------Data Scraping Tests ----------#

def test_createfolder():
    """Assert for a given number of artists, folders are created"""
    namelist = ['pearl-jam', 'pink', 'd']
    names_ = create_artist_directory(namelist)
    assert len(names_) == len(namelist)
    for name in namelist:
        assert os.path.isdir(f'./{name}')

def test_song_parsing():
    """Check if every file has .txt and there is more than 1 text file"""
    namelist = ['pink']
    song_parsing(namelist)
    for file in os.listdir('./pink'):
        assert file.endswith('.txt')
    text_files = [f for f in os.listdir('./pink') if f.endswith('.txt')]
    assert len(text_files) > 1
