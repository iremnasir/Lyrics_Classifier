# Lyrics_Classifier

WELCOME TO LYRICS CLASSIFIER!

This program takes artist input from the user to train a Multinomial Naive Bayes model via parsing artists' songs from the website www.metrolyrics.com

The user is encouraged to enter as many artists as possible in following format to run the program:

"python main.py queen pearl-jam red-hot-chili-peppers"

The program checks whether a .csv file already exists for the artist in the beginning, if true, it skips the song parsing option.

The program then parses lyrics with BeautifulSoup for artists without a .csv file with all songs, creates an artist folder (if missing) and writes individual song into a .txt file.

Each individual .csv file then converted into a dataframe of artist which eventually merged into a collective dataframe.

The collective dataframe is tokenized and the elements are used as training set.

At the end, the user is asked for lyrics input to be predicted based on the model trained. 
