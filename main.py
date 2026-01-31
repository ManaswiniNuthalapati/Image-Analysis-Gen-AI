import os
import io
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# ===============================
# Load environment variables
# ===============================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Gemini API key is missing")

genai.configure(api_key=API_KEY)

app = FastAPI()

# ===============================
# HOME PAGE — ATTRACTIVE UI
# ===============================
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI Image Analyzer</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Segoe UI", sans-serif;
}

body {
    height: 100vh;
    background: linear-gradient(135deg, #0f172a, #020617);
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
}

.card {
    width: 420px;
    padding: 35px;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(18px);
    box-shadow: 0 0 40px rgba(0,0,0,0.6);
    text-align: center;
}

.card h2 {
    font-size: 26px;
    margin-bottom: 10px;
}

.card p {
    opacity: 0.8;
    margin-bottom: 20px;
}

input[type=file] {
    display: none;
}

label {
    display: block;
    padding: 14px;
    border-radius: 10px;
    background: rgba(255,255,255,0.15);
    cursor: pointer;
    margin-bottom: 15px;
    transition: 0.3s;
}

label:hover {
    background: rgba(255,255,255,0.25);
}

.preview {
    width: 100%;
    height: 220px;
    border-radius: 12px;
    border: 2px dashed rgba(255,255,255,0.3);
    margin-bottom: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #94a3b8;
    overflow: hidden;
}

.preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

button {
    width: 100%;
    padding: 14px;
    border-radius: 10px;
    border: none;
    background: linear-gradient(135deg, #38bdf8, #0ea5e9);
    color: #020617;
    font-size: 16px;
    cursor: pointer;
    transition: 0.3s;
}

button:hover {
    transform: scale(1.03);
}
</style>
</head>

<body>

<div class="card">
    <h2>🧠 AI Image Analyzer</h2>
    <p>Upload an image and let AI understand it</p>

    <form action="/result" method="post" enctype="multipart/form-data">

        <div class="preview" id="preview">
            Image Preview
        </div>

        <label for="file">Choose Image</label>
        <input type="file" id="file" name="file" accept="image/*" required>

        <button type="submit">Analyze Image</button>
    </form>
</div>

<script>
const fileInput = document.getElementById("file");
const preview = document.getElementById("preview");

fileInput.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            preview.innerHTML = `<img src="${reader.result}">`;
        };
        reader.readAsDataURL(file);
    }
});
</script>

</body>
</html>
"""

# ===============================
# RESULT PAGE
# ===============================
@app.post("/result", response_class=HTMLResponse)
async def analyze_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(image)

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Result</title>

<style>
body {{
    height: 100vh;
    background: linear-gradient(135deg, #020617, #0f172a);
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: "Segoe UI", sans-serif;
    color: white;
}}

.card {{
    width: 600px;
    padding: 35px;
    border-radius: 18px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    box-shadow: 0 0 40px rgba(0,0,0,0.7);
}}

a {{
    color: #38bdf8;
    text-decoration: none;
}}
</style>
</head>

<body>
<div class="card">
    <h2>📊 Analysis Result</h2>
    <br>
    <p>{response.text}</p>
    <br><br>
    <a href="/">← Analyze another image</a>
</div>
</body>
</html>
"""
