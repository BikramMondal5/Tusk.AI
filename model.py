import os
import sys
import torch
import numpy as np
import tempfile
import shutil
from pathlib import Path

# Add SoniTranslate to path
sys.path.append(os.path.join(os.path.dirname(__file__), "SoniTranslate"))

# Import SoniTranslate modules
from SoniTranslate.app_rvc import SoniTranslate
from SoniTranslate.soni_translate.language_configuration import LANGUAGES
from SoniTranslate.soni_translate.utils import run_command, remove_files, copy_files
import gradio as gr

# Initialize SoniTranslate instance
soni_translator = SoniTranslate(cpu_mode=not torch.cuda.is_available())

# Language code mapping for TTS and translation
LANGUAGE_CODES = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Japanese": "ja",
    "Dutch": "nl",
    "Ukrainian": "uk",
    "Portuguese": "pt",
    "Arabic": "ar",
    "Chinese - Simplified": "zh",
    "Chinese - Traditional": "zh-TW",
    "Czech": "cs",
    "Danish": "da",
    "Finnish": "fi",
    "Greek": "el",
    "Hebrew": "he",
    "Hungarian": "hu",
    "Korean": "ko",
    "Persian": "fa",
    "Polish": "pl",
    "Russian": "ru",
    "Turkish": "tr",
    "Urdu": "ur",
    "Hindi": "hi",
    "Vietnamese": "vi",
    "Indonesian": "id",
    "Bengali": "bn",
    "Telugu": "te",
    "Marathi": "mr",
    "Tamil": "ta",
    "Javanese": "jv",
    "Catalan": "ca",
    "Nepali": "ne",
    "Thai": "th",
    "Swedish": "sv",
    "Amharic": "am",
    "Welsh": "cy",
    "Croatian": "hr",
    "Icelandic": "is",
    "Georgian": "ka",
    "Khmer": "km",
    "Slovak": "sk",
    "Albanian": "sq",
    "Serbian": "sr",
    "Azerbaijani": "az",
    "Bulgarian": "bg",
    "Galician": "gl",
    "Gujarati": "gu",
    "Kazakh": "kk",
    "Kannada": "kn",
    "Lithuanian": "lt",
    "Latvian": "lv",
    "Malayalam": "ml",
    "Romanian": "ro",
    "Sinhala": "si",
    "Sundanese": "su",
    "Estonian": "et",
    "Macedonian": "mk",
    "Swahili": "sw",
    "Afrikaans": "af",
    "Bosnian": "bs",
    "Latin": "la",
    "Myanmar Burmese": "my",
    "Norwegian": "no",
    "Assamese": "as",
    "Basque": "eu",
    "Hausa": "ha",
    "Haitian Creole": "ht",
    "Armenian": "hy",
    "Lao": "lo",
    "Malagasy": "mg",
    "Mongolian": "mn",
    "Maltese": "mt",
    "Punjabi": "pa",
    "Pashto": "ps",
    "Slovenian": "sl",
    "Shona": "sn",
    "Somali": "so",
    "Tajik": "tg",
    "Turkmen": "tk",
    "Tatar": "tt",
    "Uzbek": "uz",
    "Yoruba": "yo"
}

def translate_and_dub(audio_path, target_language, gender="male"):
    """
    Main function to translate and dub audio using SoniTranslate.
    
    Args:
        audio_path: Path to the audio file
        target_language: Target language for translation
        gender: Gender of the voice (male/female)
        
    Returns:
        Path to the dubbed video
    """
    try:
        # Get the directory and filename
        dir_path = os.path.dirname(audio_path)
        video_path = audio_path.replace('.wav', '.mp4')
        
        # Ensure video file exists
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found at {video_path}")
            
        print(f"Processing video: {video_path}")
        print(f"Target language: {target_language}")
        
        # Configure TTS voice based on gender and language
        language_code = LANGUAGE_CODES.get(target_language, "en")
        
        # Select appropriate voice based on gender and language
        if gender == "male":
            # Default to multilingual voice if specific language not found
            tts_voice = "en-US-AndrewMultilingualNeural-Male"
            
            if language_code == "fr":
                tts_voice = "fr-FR-RemyMultilingualNeural-Male"
            elif language_code == "es":
                tts_voice = "es-ES-AlvaroMultilingualNeural-Male"
            elif language_code == "de":
                tts_voice = "de-DE-FlorianMultilingualNeural-Male"
            elif language_code == "it":
                tts_voice = "it-IT-DiegoMultilingualNeural-Male"
            elif language_code == "pt":
                tts_voice = "pt-PT-DuarteMultilingualNeural-Male"
            elif language_code == "ru":
                tts_voice = "ru-RU-DmitryMultilingualNeural-Male"
            elif language_code == "ja":
                tts_voice = "ja-JP-KeitaMultilingualNeural-Male"
            elif language_code == "zh":
                tts_voice = "zh-CN-YunxiMultilingualNeural-Male"
            elif language_code == "ar":
                tts_voice = "ar-SA-HamedMultilingualNeural-Male"
            elif language_code == "hi":
                tts_voice = "hi-IN-MadhurMultilingualNeural-Male"
        else:
            # Default to multilingual voice if specific language not found
            tts_voice = "en-US-EmmaMultilingualNeural-Female"
            
            if language_code == "fr":
                tts_voice = "fr-FR-VivienneMultilingualNeural-Female"
            elif language_code == "es":
                tts_voice = "es-ES-ElviraMultilingualNeural-Female"
            elif language_code == "de":
                tts_voice = "de-DE-SeraphinaMultilingualNeural-Female"
            elif language_code == "it":
                tts_voice = "it-IT-ElsaMultilingualNeural-Female"
            elif language_code == "pt":
                tts_voice = "pt-PT-FernandaMultilingualNeural-Female"
            elif language_code == "ru":
                tts_voice = "ru-RU-SvetlanaMultilingualNeural-Female"
            elif language_code == "ja":
                tts_voice = "ja-JP-NanamiMultilingualNeural-Female"
            elif language_code == "zh":
                tts_voice = "zh-CN-XiaoxiaoMultilingualNeural-Female"
            elif language_code == "ar":
                tts_voice = "ar-SA-ZariyahMultilingualNeural-Female"
            elif language_code == "hi":
                tts_voice = "hi-IN-SwaraMultilingualNeural-Female"
        
        print(f"Selected TTS voice: {tts_voice}")
        
        # Prepare target language format for SoniTranslate
        target_lang_soni = f"{target_language} ({LANGUAGE_CODES.get(target_language, 'en')})"
        
        # Create a dummy progress object since we're not in the Gradio context
        dummy_progress = gr.Progress()
        
        # Make sure the video file is in a properly accessible location
        # Create a working directory inside SoniTranslate for better file access
        soni_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SoniTranslate")
        work_dir = os.path.join(soni_dir, "working")
        os.makedirs(work_dir, exist_ok=True)
        
        # Create normalized file paths using the working directory
        soni_video_path = os.path.join(work_dir, "input_video.mp4")
        
        # Clean up any existing files to avoid conflicts
        if os.path.exists(soni_video_path):
            os.remove(soni_video_path)
        
        # Copy the video file to working directory - using shutil instead of run_command for better reliability
        print(f"Copying video from {video_path} to {soni_video_path}")
        shutil.copyfile(video_path, soni_video_path)
        
        if not os.path.exists(soni_video_path):
            raise FileNotFoundError(f"Failed to copy video to SoniTranslate working directory: {soni_video_path}")
        
        # Set current directory to SoniTranslate dir for proper file access
        original_dir = os.getcwd()
        os.chdir(soni_dir)
        
        try:
            # Use the multilingual_media_conversion method to process the video
            print("Starting SoniTranslate processing...")
            output_path = soni_translator.multilingual_media_conversion(
                media_file=soni_video_path,
                link_media="",
                directory_input="",
                YOUR_HF_TOKEN="",
                preview=False,
                transcriber_model="large-v3" if torch.cuda.is_available() else "medium",
                batch_size=4 if torch.cuda.is_available() else 1,
                compute_type="auto",
                origin_language="Automatic detection",
                target_language=target_lang_soni,
                min_speakers=1,
                max_speakers=1,
                tts_voice00=tts_voice,
                translate_process="google_translator",
                output_type="video (mp4)",
                is_gui=False,
                progress=dummy_progress
            )
            
            print(f"SoniTranslate output: {output_path}")
            
            # Return to original directory
            os.chdir(original_dir)
            
            # Handle output path (may be a list or a single string)
            if isinstance(output_path, list):
                output_path = output_path[0]
            
            # Make sure the output file exists
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"SoniTranslate did not produce an output file at {output_path}")
            
            # Copy the output to the original directory
            result_filename = f"translated_{os.path.basename(video_path)}"
            result_path = os.path.join(dir_path, result_filename)
            
            print(f"Copying result from {output_path} to {result_path}")
            shutil.copyfile(output_path, result_path)
            
            # Clean up temporary files
            try:
                if os.path.exists(soni_video_path):
                    os.remove(soni_video_path)
            except Exception as cleanup_error:
                print(f"Warning: Could not clean up temporary file: {cleanup_error}")
                
            return result_path
            
        except Exception as process_error:
            # Return to original directory in case of error
            os.chdir(original_dir)
            raise process_error
    
    except Exception as e:
        print(f"Error in translate_and_dub: {e}")
        import traceback
        traceback.print_exc()
        raise