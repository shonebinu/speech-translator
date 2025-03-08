import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import threading

# Available Indian Languages
LANGUAGES = {
    "Hindi": "hi",
    "Malayalam": "ml",
    "Tamil": "ta",
    "Telugu": "te"
}

st.set_page_config(page_title='Speech Translator', page_icon='🌍')

# Streamlit UI
st.title("Speech Translator 🌍🎤")
st.markdown("Convert English speech to text, translate, and play audio in Indian languages.")

# Speech to Text Function
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio, language="en")
        st.write(f"**Recognized Text (English):** {text}")
        return text
    except sr.UnknownValueError:
        st.error("Could not understand the audio.")
    except sr.RequestError:
        st.error("Error with the speech recognition service.")
    return None

# Translate Function
def translate_text(text, target_lang):
    translated = GoogleTranslator(source="en", target=LANGUAGES[target_lang]).translate(text)
    return translated

# Text to Speech Function
def text_to_speech(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    return audio_stream

# Speech to Translation Button
if st.button("Start Recording"):
    spoken_text = speech_to_text()
    if spoken_text:
        translations = {}
        audio_streams = {}

        avatar_placeholder = st.columns(3)[1]
        
        # Generate translations and audio streams concurrently
        threads = []
        for lang, lang_code in LANGUAGES.items():
            def process_translation(lang, lang_code):
                translations[lang] = translate_text(spoken_text, lang)
                audio_streams[lang] = text_to_speech(translations[lang], lang_code)
            
            thread = threading.Thread(target=process_translation, args=(lang, lang_code))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Display translations and play audio
        for lang in LANGUAGES.keys():
            st.markdown(f"##### {lang} Translation:")
            st.write(translations[lang])
            st.audio(audio_streams[lang], format="audio/mp3")
        
        # Show avatar after translations and audio are rendered
        avatar_placeholder.image("./avatar-moving.gif")
