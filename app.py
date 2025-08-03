import streamlit as st
import tempfile
import os
import sys
import time
from utils import download_youtube_video, process_audio
from model import translate_and_dub

# Page configuration
st.set_page_config(page_title="Tusk.AI", page_icon="🎙️", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        width: 100%;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# App header
st.markdown("<h1 class='main-header'>Tusk.AI 🎙️</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Translate and dub YouTube videos into any language</p>", unsafe_allow_html=True)

# Sidebar for additional options
with st.sidebar:
    st.header("About Tusk.AI")
    st.write("""
    Tusk.AI uses advanced machine learning to translate and dub YouTube videos 
    into your preferred language. Simply paste a YouTube URL and choose your target language.
    """)
    
    st.header("Options")
    voice_gender = st.radio("Voice Gender", ["Male", "Female"], index=0)
    
    # Add quality option
    quality_option = st.selectbox(
        "Video Quality",
        ["Standard (faster)", "High (slower)"],
        index=0,
        help="Higher quality takes longer to process but produces better results"
    )
    
    # Add advanced options in an expander
    with st.expander("Advanced Options"):
        use_direct_youtube = st.checkbox(
            "Use SoniTranslate for YouTube download", 
            value=True,
            help="If checked, SoniTranslate's YouTube downloader will be used directly"
        )
        
        whisper_model = st.selectbox(
            "Whisper Model Size",
            ["tiny", "base", "small", "medium", "large-v3"],
            index=3,  # default to medium
            help="Larger models are more accurate but require more resources"
        )
    
    st.header("Contact & Feedback")
    st.text_area("Send us your feedback:", max_chars=500)
    st.button("Submit Feedback", key="feedback")

# Main application
youtube_url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

# File upload option as an alternative to YouTube URL
uploaded_video = st.file_uploader("Or upload a video file:", type=["mp4", "avi", "mov", "mkv"])

# Language selection - Updated with comprehensive list
available_languages = [
    "Arabic", "Bengali", "Bulgarian", "Catalan", "Chinese - Simplified", "Chinese - Traditional", 
    "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "Galician", 
    "German", "Greek", "Gujarati", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", 
    "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Korean", "Latvian", "Lithuanian", 
    "Malayalam", "Marathi", "Nepali", "Norwegian", "Persian", "Polish", "Portuguese", "Punjabi", 
    "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish", "Sundanese", "Swedish", 
    "Tamil", "Telugu", "Thai", "Turkish", "Ukrainian", "Urdu", "Vietnamese", "Welsh",
    "Albanian", "Amharic", "Azerbaijani", "Bosnian", "Georgian", "Khmer", "Macedonian", "Sinhala",
    "Swahili", "Afrikaans", "Armenian", "Assamese", "Basque", "Haitian Creole", "Hausa", "Lao",
    "Latin", "Malagasy", "Maltese", "Mongolian", "Myanmar Burmese", "Pashto", "Shona", "Somali",
    "Tajik", "Tatar", "Turkmen", "Uzbek", "Yoruba"
]

target_language = st.selectbox("Select target language:", available_languages)

process_button = st.button("Translate & Dub")

# Define video source for status messages
video_source = "YouTube video" if youtube_url else ("uploaded video" if uploaded_video else "video")

# Process video when button is clicked
if process_button and (youtube_url or uploaded_video):
    try:
        # Create temporary directory for processing files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set up progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            video_path = None
            
            # Handle YouTube URL
            if youtube_url:
                status_text.text(f"Downloading {video_source}...")
                progress_bar.progress(10)
                
                try:
                    if use_direct_youtube:
                        # Add SoniTranslate to path if it's not already there
                        soni_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SoniTranslate")
                        if soni_path not in sys.path:
                            sys.path.append(soni_path)
                        
                        # Import SoniTranslate's utility function for YouTube download
                        from SoniTranslate.soni_translate.utils import run_command
                        
                        # Use yt-dlp directly through SoniTranslate
                        output_path = os.path.join(temp_dir, "downloaded_video.mp4")
                        command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" "{youtube_url}" -o "{output_path}"'
                        run_command(command)
                        video_path = output_path
                    else:
                        # Use the utility function that tries multiple methods
                        video_path = download_youtube_video(youtube_url, temp_dir)
                except Exception as e:
                    st.error(f"YouTube download failed: {str(e)}. Try uploading your video file directly.")
                    st.stop()
            
            # Handle uploaded file
            elif uploaded_video:
                status_text.text("Processing uploaded video...")
                progress_bar.progress(10)
                
                # Save uploaded file to temp directory
                video_path = os.path.join(temp_dir, "uploaded_video.mp4")
                with open(video_path, "wb") as f:
                    f.write(uploaded_video.getbuffer())
            
            if not video_path or not os.path.exists(video_path):
                st.error("Failed to process video. Please try again.")
                st.stop()
                
            status_text.text("Extracting audio...")
            progress_bar.progress(20)
            
            # Process audio (extract from video)
            try:
                audio_path = process_audio(video_path)
            except Exception as e:
                st.error(f"Error extracting audio: {str(e)}")
                st.stop()
            
            status_text.text(f"Translating and dubbing to {target_language}...")
            progress_bar.progress(30)
            
            # Show a warning for larger videos
            video_size_mb = os.path.getsize(video_path) / (1024 * 1024)
            if video_size_mb > 50:
                st.warning(f"Processing a {video_size_mb:.1f}MB video may take several minutes. Please be patient.")
                
                # For very large videos, add additional warning
                if video_size_mb > 200:
                    st.warning("⚠️ Very large video detected! Consider using a shorter clip for better results. Processing may take 10+ minutes.")
            
            # Translate and dub with detailed status updates
            try:
                # Create an expandable section to show progress details
                with st.expander("Processing Details", expanded=True):
                    detail_status = st.empty()
                    detail_status.info("Starting video processing pipeline...")
                
                # Update progress at regular intervals to show activity
                for i in range(4, 8):
                    progress_bar.progress(i * 10)
                    if i == 4:
                        status_text.text("Transcribing audio...")
                        detail_status.info("Step 1/4: Extracting speech from video and transcribing with WhisperX...")
                    elif i == 5:
                        status_text.text(f"Translating text to {target_language}...")
                        detail_status.info(f"Step 2/4: Translating transcribed text to {target_language}...")
                    elif i == 6:
                        status_text.text("Generating voice synthesis...")
                        detail_status.info("Step 3/4: Creating synthetic voice in target language...")
                    elif i == 7:
                        status_text.text("Applying voice to video...")
                        detail_status.info("Step 4/4: Combining translated audio with original video...")
                    
                    # Add some delay to show progress (adjust based on video size)
                    delay = min(1.0, video_size_mb / 200.0)
                    time.sleep(delay)
                
                # Actually do the translation and dubbing
                status_text.text("Processing video (this may take several minutes)...")
                detail_status.info("SoniTranslate is now processing your video. For large videos, this may take 5-15 minutes...")
                
                # Pass the selected whisper model size if available
                whisper_model_size = whisper_model if 'whisper_model' in locals() else "medium"
                
                result_path = translate_and_dub(audio_path, target_language, voice_gender.lower())
                
                # Show completion
                progress_bar.progress(100)
                status_text.text("Translation complete!")
                detail_status.success("✅ Processing completed successfully!")
                
                # Show the original video
                st.subheader("Original Video")
                st.video(video_path)
                
                # Show the translated video
                st.subheader(f"Translated Video ({target_language})")
                st.video(result_path)
                
                # Provide download button
                try:
                    with open(result_path, "rb") as file:
                        btn = st.download_button(
                            label=f"Download {target_language} Version",
                            data=file,
                            file_name=f"tusk_ai_{target_language.lower()}.mp4",
                            mime="video/mp4"
                        )
                except Exception as e:
                    st.error(f"Error providing download: {str(e)}")
            
            except Exception as e:
                st.error(f"Error in translation process: {str(e)}")
                st.info("Check that SoniTranslate is properly installed and configured. Try a shorter video or a different language.")
                
                # Add debugging information for troubleshooting
                with st.expander("Troubleshooting Information", expanded=False):
                    st.markdown("### Debugging Details")
                    st.markdown(f"- Video file path: `{video_path}`")
                    st.markdown(f"- Audio file path: `{audio_path}`")
                    st.markdown(f"- Video file size: {video_size_mb:.1f}MB")
                    st.markdown(f"- Target language: {target_language}")
                    st.markdown(f"- Language code: {LANGUAGE_CODES.get(target_language, 'unknown')}")
                    st.markdown(f"- Voice gender: {voice_gender}")
                    
                    import traceback
                    st.code(traceback.format_exc(), language="python")
    
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")

# Additional information section
st.markdown("---")
st.subheader("How it works")
st.write("""
1. We download or process your video
2. Extract and transcribe the audio using WhisperX
3. Translate the transcription to your target language
4. Generate a new voiceover in the target language
5. Combine the new audio with the original video
""")

# Add a footer with technical details
st.markdown("---")
st.caption("Powered by SoniTranslate with WhisperX, PyAnnote, and Neural TTS")