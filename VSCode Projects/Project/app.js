// app.js
function showSection(section) {
    const sections = document.querySelectorAll('.stego-section');
    sections.forEach((sec) => {
        sec.classList.remove('active');
    });
    document.getElementById(section).classList.add('active');
}

function encodeText() {
    const message = document.getElementById('text-input').value;
    fetch('/encode-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function decodeText() {
    const fileInput = document.getElementById('text-file');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/decode-text', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        alert('Decoded text: ' + data.secret);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function encodeImage() {
    const fileInput = document.getElementById('image-upload');
    const message = document.getElementById('image-input').value;
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('message', message);

    fetch('/encode-image', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function decodeImage() {
    const fileInput = document.getElementById('image-upload');
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    fetch('/decode-image', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        alert('Decoded message: ' + data.secret);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function encodeVideo() {
    const fileInput = document.getElementById('video-upload');
    const message = document.getElementById('video-input').value;
    const formData = new FormData();
    formData.append('video', fileInput.files[0]);
    formData.append('message', message);

    fetch('/encode-video', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function decodeVideo() {
    const fileInput = document.getElementById('video-upload');
    const formData = new FormData();
    formData.append('video', fileInput.files[0]);

    fetch('/decode-video', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        alert('Decoded message: ' + data.secret);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
