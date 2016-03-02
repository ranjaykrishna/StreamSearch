from twython import Twython
from twython import TwythonStreamer
from jinja2 import Environment, FileSystemLoader
import json
import os
import pprint

pics_arr = []
counter = int(0)

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def print_html_doc():
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    return j2_env.get_template('jinjadisplay.html').render(
        mylist=pics_arr
    )

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'entities' in data:
            if 'media' in data['entities']:
                if 'media_url' in data['entities']['media'][0]:
                    url = data['entities']['media'][0]['media_url']
                    pics_arr.insert(0,url)
                    global counter 
                    counter+=1
                    pprint.pprint(url)
                    print counter
                    if counter == 30:
                        myfile = open('array.html', 'w')
                        myfile.write(print_html_doc())
                        counter = 0
                        pprint.pprint(pics_arr)

    def on_error(self, status_code, data):
        print status_code
        self.disconnect()

# Extract the user credentials
creds = json.load(open('config.json'))

streamer = TweetStreamer(creds['APP_KEY'], creds['APP_SECRET'],
                         creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
streamer.statuses.filter(track = 'news photo')
