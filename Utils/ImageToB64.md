---
parent: Utils
nav_order: 2
layout: default
---

# Base 64 Image Converter

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Resizer & Base64 Converter</title>
    <style>
        body { font-family: system-ui, sans-serif; padding: 2rem; background: #f8f9fa; color: #333; }
        #drop-zone {
            width: 100%; max-width: 600px; height: 150px;
            border: 3px dashed #cbd5e0; border-radius: 12px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            background: white; cursor: pointer; margin: 1rem auto; transition: 0.2s;
        }
        #drop-zone.dragover { border-color: #4299e1; background: #ebf8ff; }
        .controls { text-align: center; margin-bottom: 2rem; }
        input[type="number"] { padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 100px; }
        .result-card { background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 80px; margin-top: 10px; font-family: monospace; font-size: 11px; }
        img { max-width: 150px; display: block; margin-bottom: 10px; border: 1px solid #eee; }
        button { background: #4299e1; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; margin-top: 5px; }
        button:hover { background: #3182ce; }
    </style>
</head>
<body>

    <h2 style="text-align:center;">🖼️ Resize & Convert to Base64</h2>

    <div class="controls">
        <label>Target Width (px): </label>
        <input type="number" id="target-width" placeholder="Original">
        <p><small>Leave blank to keep original size. Aspect ratio is preserved.</small></p>
    </div>

    <div id="drop-zone">
        <p>Drop image or click to upload</p>
        <input type="file" id="file-input" accept="image/*" hidden>
    </div>

    <div id="results" style="max-width: 800px; margin: 0 auto;"></div>

    <script>
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('file-input');
        const widthInput = document.getElementById('target-width');
        const results = document.getElementById('results');

        dropZone.onclick = () => fileInput.click();

        dropZone.ondragover = (e) => { e.preventDefault(); dropZone.classList.add('dragover'); };
        dropZone.ondragleave = () => dropZone.classList.remove('dragover');
        dropZone.ondrop = (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        };

        fileInput.onchange = (e) => handleFiles(e.target.files);

        function handleFiles(files) {
            [...files].forEach(file => {
                if (file.type.startsWith('image/')) {
                    processImage(file);
                }
            });
        }

        function processImage(file) {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (event) => {
                const img = new Image();
                img.src = event.target.result;

                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');

                    let width = img.width;
                    let height = img.height;
                    const targetWidth = parseInt(widthInput.value);

                    if (targetWidth && targetWidth < width) {
                        const scaleFactor = targetWidth / width;
                        width = targetWidth;
                        height = img.height * scaleFactor;
                    }

                    canvas.width = width;
                    canvas.height = height;
                    ctx.drawImage(img, 0, 0, width, height);

                    const base64String = canvas.toDataURL(file.type);
                    displayResult(file.name, base64String, width, height);
                };
            };
        }

        function displayResult(name, base64, w, h) {
            const div = document.createElement('div');
            div.className = 'result-card';
            div.innerHTML = `
                <strong>${name}</strong> (${Math.round(w)} x ${Math.round(h)})
                <img src="${base64}">
                <textarea readonly>${base64}</textarea>
                <button onclick="copyText(this)">Copy Base64</button>
            `;
            results.prepend(div);
        }

        function copyText(btn) {
            const area = btn.previousElementSibling;
            area.select();
            document.execCommand('copy');
            btn.innerText = 'Copied!';
            setTimeout(() => btn.innerText = 'Copy Base64', 2000);
        }
    </script>