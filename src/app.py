import os
import signal
import json
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, redirect, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

def read_config():
    config = {}
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        pass
    return config

# Write the bot settings to the config file
def write_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file)

# Handle the settings page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        bot_token = request.form['token']
        weather_api_key = request.form['api_key']
        weather_channel_id = request.form['channel_id']
        google_application_credentials = request.form['credentials']
        city_country = request.form['location']
        bot_prefix = request.form['prefix']
        config = {
            'PREFIX': bot_prefix,
            'BOT_TOKEN': bot_token,
            'API_KEY': weather_api_key,
            'CHANNEL_ID': weather_channel_id,
            'GOOGLE_APPLICATION_CREDENTIALS': google_application_credentials,
            'LOCATION': city_country
        }
        write_config(config)
        return redirect('/settings')
    else:
        config = read_config()
        return render_template('settings.html', bot_token=config.get('BOT_TOKEN', ''), weather_api_key=config.get('API_KEY', ''), weather_channel_id=config.get('CHANNEL_ID', ''), google_application_credentials=config.get('GOOGLE_APPLICATION_CREDENTIALS', ''), city_country=config.get('LOCATION'), bot_prefix=config.get('PREFIX'))

# Handle the home page
@app.route('/')
def home():
    return render_template('index.html')

# Handle the commands page
@app.route('/commands')
def commands():
    return render_template('commands.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route to serve the logs page
@app.route('/logs')
def logs():
    # Read the bot logs from a file or database
    with open('bot_logs.txt', 'r') as f:
        logs_data = f.read()
    return render_template('logs.html', logs=logs_data)

import sys

bot_process = None  # Variable to store the bot process

@app.route('/start', methods=['GET', 'POST'])
def start_bot():
    global bot_process

    try:
        # Start the bot.py script
        bot_process = subprocess.Popen(['python', 'bot.py'])
        return jsonify({'status': 'success', 'message': 'Bot started.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown_bot():
    global bot_process

    try:
        if bot_process is not None:
            # Terminate the bot process
            bot_process.terminate()
            bot_process = None

            return jsonify({'status': 'success', 'message': 'Bot shut down.'})
        else:
            return jsonify({'status': 'error', 'message': 'Bot is not running.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/logs-content')
def get_logs_content():
    with open('bot_logs.txt', 'r') as file:
        content = file.read()
    return content

# Run the Flask server
if __name__ == '__main__':
    app.run()
