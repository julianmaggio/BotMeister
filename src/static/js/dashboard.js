document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/dashboard')
        .then(response => response.json())
        .then(data => {
            document.getElementById('serverCount').textContent = data.serverCount;
            document.getElementById('onlineUsers').textContent = data.onlineUsers;
            document.getElementById('commandCount').textContent = data.commandCount;
        })
        .catch(error => console.log(error));
});
