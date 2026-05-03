# 🪐 AI-Powered Vedic Kundli Analyzer

**🌍 [🔴 Live Demo: Try the Application Here!](https://kundli-analyzer-ai.onrender.com)**

![Kundli App Screenshot](assets/screenshot.png)

A full-stack web application that generates personalized Vedic astrological birth charts (North Indian style) and provides comprehensive life readings using Google's Gemini AI.

## ✨ Features
* **Interactive UI:** Sleek, dark-mode interface with animated cosmic elements.
* **Dynamic Chart Generation:** Dynamically builds a 4x4 North Indian Kundli grid based on astrological data.
* **AI Analysis:** Leverages the `gemini-2.5-flash` REST API for nuanced, JSON-structured astrological interpretations, including Dasha timelines and remedies.
* **Multilingual Support:** Offers dynamic analysis in both English and conversational Hindi.
* **Secure Backend:** Flask server architecture to safely manage API keys and process cross-origin requests.

## 🛠️ Tech Stack
* **Frontend:** HTML5, Vanilla JavaScript, CSS3 (Custom Animations & Glassmorphism)
* **Backend:** Python, Flask, Flask-CORS
* **AI Integration:** Google Gemini REST API
* **Environment Management:** python-dotenv

## 🚀 Running the Project Locally

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/Bijendra78/kundli-analyzer.git
cd kundli-analyzer
\`\`\`

### 2. Install dependencies
Ensure you have Python 3 installed, then run:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Set up Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API key:
\`\`\`env
GEMINI_API_KEY=your_api_key_here
\`\`\`

### 4. Start the Server
\`\`\`bash
python app.py
\`\`\`
Then open your web browser and navigate to `http://127.0.0.1:5000`.

## 🔒 Security Note
The `.env` file containing the API key is intentionally excluded from this repository via `.gitignore`. You must supply your own Google AI Studio key to run the analysis.