=================
Lyrics_Classifier
=================

## **WELCOME TO LYRICS CLASSIFIER!** ##

- This program takes artist input from the user to train a Multinomial Naive Bayes model via parsing artists' songs from the website www.metrolyrics.com

***Usage***

- The user is encouraged to enter as many artists as possible in following format to run the program:

`python ./Lyrics_Classifier/main.py <artist1> <artist2name-artist2lastname>`

`python ./Lyrics_Classifier/main.py Queen Red-Hot-Chili-Peppers Pearl-Jam`


- The program checks whether a .csv file already exists for the artist in the beginning, if true, it skips the song parsing option.

- The program then parses lyrics with BeautifulSoup for artists without a .csv file with all songs, creates an artist folder (if missing) and writes individual song into a .txt file.

- Each individual .csv file then converted into a dataframe of artist which eventually merged into a collective dataframe.

- The collective dataframe is tokenized and the elements are used as training set.

- At the end, the user is asked for lyrics input to be predicted based on the model trained.

* Free software: MIT license



### Features to be improved ###

- Documentation: https://Lyrics-Classifier.readthedocs.io.
--------


### Credits ###
-------

This package was created with Cookiecutter_ and the
`Spiced Academy Cookiecutter PyPackage <https://github.com/spicedacademy/spiced-cookiecutter-pypackage>`_ project template.

_Cookiecutter: https://github.com/audreyr/cookiecutter-pypackage
