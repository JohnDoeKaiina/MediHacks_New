import asyncio
import requests
import pyaudio
import os
import wave
import io
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
print("hiii")

# Deepgram API Key
DEEPGRAM_API_KEY = "key"
DEEPGRAM_URL = 'https://api.deepgram.com/v1/listen'

# Audio stream settings
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1  # Mono channel
RATE = 16000  # 16kHz sampling rate
CHUNK = 1024  # 1KB chunks

def transcribe_audio_stream(audio_data):
    headers = {
        'Authorization': f'Token {DEEPGRAM_API_KEY}',
        'Content-Type': 'audio/wav'
    }
    response = requests.post(DEEPGRAM_URL, headers=headers, data=audio_data)
    return response.json()

def convert_to_wav(audio_data):
    # Convert raw audio data to WAV format in memory
    with io.BytesIO() as wav_io:
        with wave.open(wav_io, 'wb') as wav_file:
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(pyaudio.get_sample_size(FORMAT))
            wav_file.setframerate(RATE)
            wav_file.writeframes(audio_data)
        wav_io.seek(0)
        return wav_io.read()

def callback(in_data, frame_count, time_info, status):
    # Convert the raw audio data to WAV format
    wav_data = convert_to_wav(in_data)
    
    # Transcribe the WAV audio data
    transcription_result = transcribe_audio_stream(wav_data)
    print(transcription_result)
    return (in_data, pyaudio.paContinue)

async def main():
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

    print("Listening...")

    # Start the stream
    stream.start_stream()

    # Keep the stream active
    try:
        while stream.is_active():
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping...")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    asyncio.run(main())
