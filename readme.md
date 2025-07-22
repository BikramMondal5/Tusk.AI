# 🧠🐘 Tusk.AI

Tusk.AI is a professional full-stack web application that enables users to input a YouTube video URL and translate/dub the audio into a target language using advanced machine learning models. This tool is designed to make video content accessible to a global audience by breaking language barriers.

## 🌟 Features
- **Modern User Interface**: Professional layout with branding and easy navigation.
- **YouTube Integration**: Paste a YouTube URL to fetch and process videos.
- **Language Translation & Dubbing**: Translate and dub audio into a target language using advanced ML models.
- **Voice Gender Selection**: Choose between male/female voices for dubbing.
- **Multiple Languages**: Support for French, Spanish, German, Italian, Portuguese, Russian, Japanese, Chinese, Arabic, and Hindi.
- **Downloadable Output**: Download the dubbed video with ease.
- **Error Handling**: Robust error handling for invalid URLs, network issues, and model failures.

## 🛠️ Technologies Used
- **Frontend**: Streamlit for the user interface.
- **Backend**: Python with libraries for audio processing and machine learning.
- **Speech Processing**: SoniTranslate, WhisperX for speech recognition and translation.
- **Voice Conversion**: PyWorld, FAISS, and Torch-based voice conversion models.
- **File Handling**: Temporary file management with `tempfile` and `os`.

## 🔧 Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Tusk.AI
   ```
2. Install core dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install additional required dependencies:
   ```bash
   pip install git+https://github.com/R3gm/whisperX.git@cuda_11_8
   pip install rarfile
   pip install librosa
   pip install srt
   pip install faiss-cpu==1.7.3
   pip install praat-parselmouth
   pip install torchcrepe
   pip install pyworld
   ```
4. Run the application locally:
   ```bash
   streamlit run main.py
   ```

## 🚀 How to Use
1. Open the app.
2. Paste the YouTube video URL in the input field.
3. Select the target language from the dropdown menu.
4. Choose the voice gender (Male/Female).
5. Click the "Translate & Dub" button.
6. Wait for the process to complete - you'll see a progress bar with status updates.
7. The original and translated videos will be displayed for comparison.
8. Download the dubbed video using the provided download button.

## 🌍 Why It Matters
Tusk.AI bridges the gap between content creators and global audiences by:
- **Enhancing Global Accessibility**: Making educational, entertainment, and informational content available to non-native speakers
- **Breaking Language Barriers**: Allowing creators to reach audiences in multiple languages without creating separate content
- **Preserving Original Delivery**: Maintaining the original speaker's vocal characteristics while changing the language
- **Democratizing Content**: Making specialized knowledge accessible regardless of the viewer's native language
- **Saving Time and Resources**: Eliminating the need for professional dubbing studios for basic content translation

## 💻 System Requirements
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 8GB recommended, 16GB for better performance
- **Storage**: At least 2GB of free disk space for dependencies and temporary files
- **GPU**: Optional but recommended for faster processing

## ⚠️ Troubleshooting
If you encounter import errors, ensure all dependencies are properly installed. The application relies on several specialized audio and speech processing libraries that must be installed in the correct order.

Common issues:
- 🔍 **WhisperX installation errors**: Try the direct GitHub installation method
- ⚠️ **NumPy version conflicts**: The application requires NumPy 1.24.3 for compatibility with all dependencies
- 🔊 **Missing audio processing libraries**: Ensure librosa, pyworld, and torchcrepe are installed

## 🤝 Contribution
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Commit your changes and push to your branch.
4. Open a pull request.

## 📜 License
This project is licensed under the `MIT License`.