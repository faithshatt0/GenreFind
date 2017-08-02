#Authors: Faith Shatto, Miguel Aceves, Priscilla Nunez
#Name of File: MainFile.py
#Last Modified: March 15, 2017

from flask import Flask, render_template, request, redirect, url_for
import os
import spotipy 
import sys
import pprint
import shutil

app = Flask(__name__)

spotify = spotipy.Spotify()

#finds artist's information from spotify
def get_artist(name):
    spotify = spotipy.Spotify()
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

#shows the artist's information by writing it onto html file
def show_artist(artist):
    
    #creates file with genres
    if len(artist['genres']) > 0:
        f = open("templates/results.html","a+")
        
        #outputs name of artist
        f.write('\n' '<div class="output" >'+ artist['name'] + '</div>' ' <br />')
        
        #outputs image of artist
        f.write('<div class="output" ><img src = "' + artist['images'][0]['url'] + '" /></div>' + '<br />')
        
        #outputs list of genres associated with artist
        f.write('<div class ="output">''Genres associated with this artist:''</div>''</br/>')
        f.write('<div class="output"></div''Genres associated with this artist: ')
        f.write('<br/S>'.join(artist['genres'])) 
        f.close

#outputs the user's input
def show_from_form():
    fromForm = request.form['music-form']
    return fromForm

#actually runs the page
@app.route('/', methods=['GET', 'POST'])
def spotify():
    
    if request.method == "POST":
        spot()
        return redirect(url_for('results.html'))
    return render_template('index.html')

@app.route('/spotify', methods =['GET', 'POST'])
def spot():
    
    #copies template file over old results file to refresh results
    shutil.copyfile("templates/index.html", "templates/results.html")
    
    #user's input is set as artist's name
    artistName = show_from_form()
    
    #searches spotify library and outputs results (genre only)
    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = artistName
        artist = get_artist(name)
        show_artist(artist)

        return render_template ('results.html')
    
if __name__ == '__main__':
    app.run(
        debug =True,
        port = int(os.getenv('PORT', 8080)),
        host = os.getenv('IP', '0.0.0.0')
        )