from twython import Twython
from twython import TwythonStreamer
import json
import pprint
import sys

pics_arr = []
counter = 0

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'entities' in data:
            if 'media' in data['entities']:
                if 'media_url' in data['entities']['media'][0]:
                    url = data['entities']['media'][0]['media_url']
                    pics_arr.insert(0,url)
                    global counter 
                    counter+=1
                    print counter
                    pprint.pprint(url)         
    def on_error(self, status_code, data):
        print status_code
        self.disconnect()
    
creds = json.load(open('config.json')) # Extract the user credentials
streamer = TweetStreamer(creds['APP_KEY'], creds['APP_SECRET'], creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
query = sys.argv[1]
streamer.statuses.filter(track = query)