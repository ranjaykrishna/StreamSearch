from twython import Twython
from twython import TwythonStreamer
import json
import pprint
from flask import Flask
from flask import render_template
import threading
from threading import Thread

MAX_SIZE = 200

app = Flask(__name__)
pics_arr = []
counter = int(0)

@app.route('/')
def render_images():
    return render_template('jinjadisplay.html', mylist=pics_arr)

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'entities' in data:
            if 'media' in data['entities']:
                if 'media_url' in data['entities']['media'][0]:
                    url = data['entities']['media'][0]['media_url']
                    # cap at MAX_SIZE 
                    if (counter == MAX_SIZE): 
                        del pics_arr[-1]
                        counter-=1
                    pics_arr.insert(0,url)
                    global counter 
                    counter+=1
                    pprint.pprint(url)
                    print counter
    def on_error(self, status_code, data):
        print status_code
        self.disconnect()

def runServer():
    app.run()

def streamTwitter():
    streamer = TweetStreamer(creds['APP_KEY'], creds['APP_SECRET'],
                             creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
    streamer.statuses.filter(track = 'news photo')

# Extract the user credentials
creds = json.load(open('config.json'))

if __name__ == '__main__':
    Thread(target = runServer).start()
    Thread(target = streamTwitter).start()
