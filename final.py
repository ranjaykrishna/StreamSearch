from twython import Twython
from twython import TwythonStreamer
import json
import pprint
from flask import Flask, jsonify
from flask import render_template, request, url_for, redirect
import threading
from multiprocessing import Process, Queue
import time

MAX_SIZE = 200
app = Flask(__name__)
pics_arr = []
counter = int(0)
query = ""
searchThread = []
streamer = None
disconnectCounter = int(0)
queue = Queue()
# Extract the user credentials
creds = json.load(open('config.json'))


@app.route('/', methods = ['POST', 'GET'])
def render_images():
    if request.method == 'POST':
        # if streamer != None:
        #     streamer.disconnect()

        for thread in searchThread:
            print thread 
            thread.terminate()

            
        global query
        query = request.form['query-input']

        # print "updated query: "+ query
        # global searchThread
        # print "searchThread:" 
        # print searchThread
        # print " ".join((''.join(elems) for elems in searchThread))
        # print "creating new searchhread"
        stream = Process(target = streamTwitter, args=(query,))
        stream.start()
        searchThread.append(stream)
        print "thread after return"
        print searchThread

    return render_template('jinjadisplay.html', mylist=pics_arr)

@app.route('/data', methods = ['GET'])
def return_data():
    result = []
    while not queue.empty():
        result.append(queue.get())
    return jsonify(results = result)

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'entities' in data:
            if 'media' in data['entities']:
                if 'media_url' in data['entities']['media'][0]:
                    url = data['entities']['media'][0]['media_url']
                    global counter
                    print str(counter)+" "+url
                    # if (disconnectCounter == 5):
                    #     streamer.disconnect()
                    #     print "DISCONNECTED"
                    #     disconnectCounter = 0
                    #     global searchThread
                    #     print "searchThread:"
                    #     print searchThread
                    #     global query
                    #     print "current query: "+query
                    #     searchThread.append(Thread(target = streamTwitter(query)))
                    #     print "after appending in success"
                    #     return

                    if (counter == MAX_SIZE): 
                        pics_arr.pop([0])
                        counter-=1
                    if (url not in pics_arr):
                        queue.put(url)
                        pics_arr.append(url)
                        counter+=1
                        global disconnectCounter
                        disconnectCounter+=1
                        
    def on_error(self, status_code, data):
        print status_code
        self.disconnect()

def runServer():
    app.debug = True
    app.run(use_reloader=False, threaded=True)

def streamTwitter(query):
    global streamer
    streamer = TweetStreamer(creds['APP_KEY'], creds['APP_SECRET'],
                             creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
    streamer.statuses.filter(track = query)

if __name__ == '__main__':
    Process(target = runServer).start() 