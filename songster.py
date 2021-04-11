from flask import Flask, render_template, request
import requests, bs4
import os
import json
import lyricsgenius
import argparse
from pathlib import Path
import csv
from scripts import pull_data
from scripts import train

# Constants
DATA_DIR = Path(os.getcwd() + '/data/')
SECRETS = Path(os.getcwd() + '/scripts/secrets.json')

app = Flask(__name__, template_folder='templates')
@app.route('/', methods=['GET', 'POST'])
def songster():
    if request.method == 'POST':
        render_template('about.html')
        artist = request.form['artist'].strip()
        limit = request.form['limit'].strip()
        limit = int(limit)
        genre = None
        with open(SECRETS) as secrets_f:
            secrets = json.load(secrets_f)
            genius = lyricsgenius.Genius(secrets['keys']['genius'])
            print('Key: {}\n'.format(secrets['keys']['genius']))

        print('*****Passed Arguments*****\nGenre: {}\nArtist: '
              '{}\nLimit: {}'.format(genre, artist, limit))
        print('This is the data directory: {}'.format(DATA_DIR))

        song_count_limit = limit

        if artist is not None:
            pull_data.download_artist(genius, artist, song_count_limit)
        if genre is not None:
            pull_data.download_genre(genius, genre, song_count_limit)

        formatted_artist_name = ""
        for name in artist.split(" "):
            formatted_artist_name += name + "_"

        file_name = formatted_artist_name + "lyrics.txt"
        generator = train.TextGenerator(os.getcwd() + '/data/' + file_name)

        return render_template('return.html', artist=artist, limit=limit, lyrics=generator.generate_text())
    else:
        return render_template('base.html')

if __name__ == "__main__":
    app.debug = True
    app.run()