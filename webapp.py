#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session, logging
import os, json, subprocess

app = Flask(__name__)
app.secret_key = 'I46yJKa4KU5eQSDZyzmBGg'

def get_volume():
	return session.get("volume") or 50

def sounds():
	files = os.listdir('/home/pi/whitenoise/sounds')
	return files

def set_volume():
	os.system("amixer sset 'Master' " + str(get_volume()) + "%")

def increment_volume(direction):
	os.system("amixer set 'Master' 10%" + str(direction))

@app.route('/')
def index():
    return render_template('index.html', volume=get_volume(), sounds=sounds())

@app.route('/connect', methods = ['GET'])
def connect():
	os.system("~/btconnect.sh")
	return redirect('/')

@app.route('/volumedown', methods = ['get'])
def volumedown():
	increment_volume('-')
	return json.dumps({'message': 'volume decreased 10%'})

@app.route('/volumeup', methods = ['get'])
def volumeup():
	increment_volume('+')
	return json.dumps({'message': 'volume increased 10%'})

@app.route('/volume', methods = ['post'])
def volume():
	data = request.get_json()
	session['volume'] = data['volume']
	set_volume()
	return json.dumps({'message': 'volume set to ' + data['volume']})

@app.route('/rain', methods = ['GET'])
def rain():
	os.system("mpg123 -f 20000 --loop -1 ~/whitenoise/sounds/rain.mp3")
	return redirect('/')

@app.route('/waves', methods = ['GET'])
def waves():
	os.system("mpg123 -f 15500 --loop -1 ~/whitenoise/sounds/waves.mp3")
	return redirect('/')

@app.route('/whitenoise', methods = ['GET'])
def whitenoise():
	os.system("mpg123 -f 29000 --loop -1 ~/whitenoise/sounds/noise-only.mp3")
	return redirect('/')

@app.route('/play', methods = ['POST'])
def play():
	file = request.form.get('file')
	os.system("mpg123 -f 20000 --loop -1 ~/whitenoise/sounds/" + file)
	return redirect('/')

@app.route('/up', methods = ['GET'])
def volumn_up():
	session["volume"] = get_volume()+5
	set_volume()
	return redirect('/')

@app.route('/down', methods = ['GET'])
def volumn_down():
	session["volume"] = get_volume()-5
	set_volume()
	return redirect('/')

@app.route('/stop', methods = ['GET'])
def stop():
	os.system("killall mpg123")
	return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    session["volume"] = 100
