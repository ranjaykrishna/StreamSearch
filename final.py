from twython import TwythonStreamer
from flask import Flask, jsonify, render_template, request
from multiprocessing import Process, Queue
import json

MAX_SIZE = 200
app = Flask(__name__)
pics_arr = []
counter = int(0)
query = ""
allProcesses = []
queue = Queue()
# Extract the user credentials
creds = json.load(open('config.json'))


@app.route('/', methods = ['POST', 'GET'])
def render_images():
    if request.method == 'POST':
        for process in allProcesses:
            process.terminate()    
        global query
        query = request.form['query-input']
        stream = Process(target = streamTwitter, args=(query,))
        stream.start()
        allProcesses.append(stream)
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
                    if (counter == MAX_SIZE): 
                        pics_arr.pop([0])
                        counter-=1
                    if (url not in pics_arr):
                        print str(counter)+" "+query+" "+url
                        queue.put(url)
                        pics_arr.append(url)
                        counter+=1

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