import pandas as pd
import os


def dataframe_artists(namelist, loc):
    """ Creates a dataframe per artist, cleans the text and saves as .csv """
    for artist_name_re in namelist:
        df_ = []
        sn = []
        data = []
        path = loc+'/'+artist_name_re
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
        for f in files:
            with open(os.path.join(path,f),'r') as myfile:
                data.append(myfile.read())
                sn.append(str(f).strip())
                obj = zip(sn, data)
            df_ = pd.DataFrame(obj, columns = ['Song_name', f'{artist_name_re}'])
            df_['Song_name'] = df_['Song_name'].str.replace(r'(\.)(txt)$', '')
            df_['Song_name'] = df_['Song_name'].str.replace(f'{artist_name_re}', '')
            df_['Song_name'] = df_['Song_name'].str.replace('-', ' ')
            df_['Song_name'] = df_['Song_name'].str.replace('lyrics', ' ')
            df_[f'{artist_name_re}'] = df_[f'{artist_name_re}'].str.strip('[')
            df_[f'{artist_name_re}'] = df_[f'{artist_name_re}'].str.strip(']')
            df_ = df_[~df_[f'{artist_name_re}'].str.contains("Unfortunately, we are not authorized to show these lyrics")]
            df_ = df_[~df_[f'{artist_name_re}'].str.contains("(instrumental)")]
            df_ = df_[~df_[f'{artist_name_re}'].str.contains("Instrumental")]
            #df_[f'{artist_name_re}'] = df_[f'{artist_name_re}'].replace(r'[^\w\d]',' ', regex=True)
            df_ = df_.replace(r'\\n',' ', regex=True)

            df_.to_csv(f'{artist_name_re}.csv')
        print('There are ', len(df_), f'songs in {artist_name_re} dataframe')

def merge_dataframes(namelist):
    """ Merges individual artist dataframes, drops na and removes junk """

    df = pd.DataFrame() # this is a dictionary of dataframes with name
    for name in namelist:
        df_1 = pd.read_csv(f'{name}.csv', index_col = 0)
        df_1['Artist'] = f'{name}'
        df_1.rename(columns={f'{name}':'Lyrics'}, inplace=True)
        df = pd.concat([df, df_1], axis = 0, ignore_index = True)
    df_lyrics = df.dropna(axis = 0)
    key = list(range(0,len(namelist)))
    map_dict = dict(zip(namelist, key))
    df_lyrics['ydata'] = df_lyrics['Artist'].map(map_dict)
    print('There are ', len(df_lyrics), f'songs in merged dataframe after dropping string cleaning')
    return df_lyrics
