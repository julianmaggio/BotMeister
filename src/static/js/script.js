document.addEventListener('DOMContentLoaded', () => {
    const logsContainer = document.getElementById('logs');
    const startBtn = document.getElementById('start-btn');
    const shutdownBtn = document.getElementById('shutdown-btn');
  
    // Function to append a log entry to the logs container
    const appendLog = (log) => {
      const logEntry = document.createElement('p');
      logEntry.textContent = log;
      logsContainer.appendChild(logEntry);
    };
  
    // Function to update the logs container with the initial logs
    const updateLogs = () => {
      // Fetch the bot logs from the server
      fetch('/logs')
        .then((response) => response.text())
        .then((data) => {
          // Split the logs by newline and append each entry to the logs container
          const logs = data.split('\n');
          logs.forEach((log) => {
            appendLog(log);
          });
        });
    };
  
    // Function to start the bot
    const startBot = () => {
      // Send a request to start the bot
      fetch('/start')
        .then(() => {
          appendLog('Bot started successfully.');
        });
    };
  
    // Function to shutdown the bot
    const shutdownBot = () => {
      // Send a request to shutdown the bot
      fetch('/shutdown')
        .then(() => {
          appendLog('Bot shutdown initiated.');
        });
    };
  
    // Event listener for the start button
    startBtn.addEventListener('click', startBot);
  
    // Event listener for the shutdown button
    shutdownBtn.addEventListener('click', shutdownBot);
  
    // Update the logs container with the initial logs
    updateLogs();
  });
  