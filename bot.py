import telebot
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
bot = telebot.TeleBot("6145463945:AAE81VE7bu421E4GcBh1mQkW3itlf5F5NVI")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am your Homai bot. Please send me an audio message and I will convert it to text.")
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    # download the audio message
    file_info = bot.get_file(message.voice.file_id)
    file_content = bot.download_file(file_info.file_path)

    # convert the audio message to text
    audio = AudioSegment.from_file(BytesIO(file_content), format="ogg")
    audio.export("temp.wav", format="wav")
    r = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="en-US")

    # send the text message
    bot.reply_to(message, text)
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)
bot.polling()
