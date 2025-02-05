// Screen navigation
function showSelectionScreen() {
    document.getElementById("welcome-screen").classList.add("hidden");
    document.getElementById("selection-screen").classList.remove("hidden");
}

function showEncodeScreen() {
    sessionStorage.setItem("mode", "encrypt");
    document.getElementById("selection-screen").classList.add("hidden");
    document.getElementById("stego-type-screen").classList.remove("hidden");
}

function showDecodeScreen() {
    sessionStorage.setItem("mode", "decrypt");
    document.getElementById("selection-screen").classList.add("hidden");
    document.getElementById("stego-type-screen").classList.remove("hidden");
}

function showFileScreen(type) {
    sessionStorage.setItem("fileType", type);
    document.getElementById("stego-type-screen").classList.add("hidden");
    document.getElementById("file-screen").classList.remove("hidden");

    let mode = sessionStorage.getItem("mode");
    document.getElementById("action-title").innerText = (mode === "encrypt") ? "Encrypt File" : "Decrypt File";

    if (mode === "encrypt") {
        document.getElementById("encrypt-fields").style.display = "block";
    } else {
        document.getElementById("encrypt-fields").style.display = "none";
    }
}

function goBack() {
    document.getElementById("selection-screen").classList.add("hidden");
    document.getElementById("welcome-screen").classList.remove("hidden");
}

function goBackToSelection() {
    document.getElementById("stego-type-screen").classList.add("hidden");
    document.getElementById("selection-screen").classList.remove("hidden");
}

function goBackToTypeSelection() {
    document.getElementById("file-screen").classList.add("hidden");
    document.getElementById("stego-type-screen").classList.remove("hidden");
}

// Caesar Cipher Functions
function caesarCipherEncrypt(text, shift) {
    return text.split('').map(char => {
        if (char.match(/[a-z]/i)) {
            let code = char.charCodeAt(0);
            let base = char >= 'a' ? 97 : 65;
            return String.fromCharCode(((code - base + shift) % 26) + base);
        }
        return char;
    }).join('');
}

function caesarCipherDecrypt(text, shift) {
    return caesarCipherEncrypt(text, 26 - shift);
}

// File Processing (Encrypt/Decrypt)
function processFile() {
    let mode = sessionStorage.getItem("mode");
    let fileType = sessionStorage.getItem("fileType");
    let shift = parseInt(document.getElementById("shift-value").value);
    let fileInput = document.getElementById("file-upload").files[0];

    if (!fileInput || isNaN(shift)) {
        alert("Please upload a file and enter a shift value.");
        return;
    }

    let reader = new FileReader();
    reader.onload = function(event) {
        let content = event.target.result;

        if (mode === "encrypt") {
            let text = document.getElementById("text-input").value;
            let encryptedText = caesarCipherEncrypt(text, shift);
            content += `\n[ENCRYPTED]: ${encryptedText}`;
        } else {
            let match = content.match(/\[ENCRYPTED\]: (.*)/);
            if (match) {
                let decryptedText = caesarCipherDecrypt(match[1], shift);
                content = content.replace(match[0], `\n[DECRYPTED]: ${decryptedText}`);
            } else {
                alert("No encrypted text found in the file.");
                return;
            }
        }

        // Create a downloadable file
        let blob = new Blob([content], { type: "text/plain" });
        let url = URL.createObjectURL(blob);
        let downloadLink = document.getElementById("download-link");
        downloadLink.href = url;
        downloadLink.style.display = "block";
    };
    reader.readAsText(fileInput);
}
