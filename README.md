Apologies for the oversight. Here's an updated version of the readme that includes the missing information:

# Botmeister

Botmeister is a versatile Discord bot built using Discord.py. It provides a range of useful features to enhance your Discord server's functionality. With Botmeister, you can get weather updates, set countdown timers, clear messages, and more. The bot is designed to be customizable and extendable, allowing you to tailor it to suit your specific server needs.

## Features

- Weather Updates: Get real-time weather updates for a specified location.
- Countdown Timer: Set a countdown in seconds and track the remaining time.
- Message Clearing: Clear a specified number of messages from a channel.
- Ping Command: Check the bot's response time.
- Server Information: Retrieve information about the Discord server.
- User Information: Get details about a user, including username, ID, and join date.
- Roll Command: Generate a random number within a specified range.

## Website

Botmeister also comes with a web interface that allows you to manage and configure the bot easily. The web interface provides a user-friendly dashboard where you can customize bot settings, view server statistics, and perform administrative tasks.

## Installation

1. Clone the repository:

   ```bash
   git clone https://git.kukikugames.com/Julian/Botmeister.git
   ```

2. Move the files and delete the original folder:
   - Run the following command to move the files from the `Botmeister/src` directory to the root directory:
     ```bash
     robocopy "Botmeister\src" . /E
     ```
   - Delete the empty `Botmeister/src` directory.

3. Set up and activate a virtual environment:
   - Open a new command prompt.
   - Navigate to the `Botmeister` directory.
   - Create a new virtual environment:
     ```bash
     python -m venv myenv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       myenv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source myenv/bin/activate
       ```

4. Install the required dependencies:
   - Make sure you have Python, Git, and Pip installed.
   - Use the following command to install the dependencies:
     ```bash
     pip install -r requirements.txt
     ```

5. Run the bot:
   ```bash
   python app.py
   ```

6. Access the web interface:
   - Open your web browser and navigate to the Botmeister website.
   - The app can be accessed by either `http://localhost:5000` or `http://127.0.0.1:5000`

7. Set up the configuration:
   - Go to the settings page and edit the settings to fit your needs.

## Usage

- Make sure the bot has the necessary permissions in your Discord server.
- Use the provided command prefix to interact with the bot and access its features.
- Utilize the web interface for convenient management and configuration of the bot.

## License

Botmeister is released under the MIT License.

## Usage

- Make sure the bot has the necessary permissions in your Discord server.
- Use the provided command prefix to interact with the bot and access its features.
- Utilize the web interface for convenient management and configuration of the bot.

## License

Botmeister is released under the MIT License.