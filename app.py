import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# Available Languages
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Malayalam": "ml",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja"
}

st.set_page_config(page_title='Speech Translator', page_icon = '🌍')

# Streamlit UI
st.title("Speech Translator 🌍🎤")
st.markdown("Convert speech to text, translate, and play audio in different languages.")

# Language selection
input_lang = st.selectbox("Select Input Language:", list(LANGUAGES.keys()))
output_lang = st.selectbox("Select Output Language:", list(LANGUAGES.keys()))

# Speech to Text Function
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=LANGUAGES[input_lang])
        st.success(f"Recognized Text ({input_lang}): {text}")
        return text
    except sr.UnknownValueError:
        st.error("Could not understand the audio.")
        return None
    except sr.RequestError:
        st.error("Error with the speech recognition service.")
        return None

# Translate Function
def translate_text(text, target_lang):
    translated = GoogleTranslator(source="auto", target=LANGUAGES[target_lang]).translate(text)
    st.success(f"Translated Text ({target_lang}): {translated}")
    return translated

# Text to Speech Function (No File Saving)
def text_to_speech(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    audio = AudioSegment.from_file(audio_stream, format="mp3")
    play(audio)

# Speech to Translation Button
if st.button("Start Recording"):
    spoken_text = speech_to_text()
    if spoken_text:
        translated_text = translate_text(spoken_text, output_lang)
        st.info("Playing Translated Audio...")
        text_to_speech(translated_text, LANGUAGES[output_lang])
