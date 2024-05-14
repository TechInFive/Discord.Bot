
import threading
from playsound import playsound
from pydub import AudioSegment

import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

class AudioService:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.stream = None
        self.is_recording = False

    def start_recording(self, wav_file_path):
        self.wav_file_path = wav_file_path
        self.is_recording = True
        self.frames = []
        
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK)
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self):
        while self.is_recording:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            self.frames.append(data)
    
    def stop_recording(self):
        self.is_recording = False
        self.thread.join()
        
        self.stream.stop_stream()
        self.stream.close()
        
        waveFile = wave.open(self.wav_file_path, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

        self.audio.terminate()
        self.audio = None
        self.audio = pyaudio.PyAudio()

    def record(self, record_seconds, wav_file_path):
        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        frames = []

        for i in range(0, int(RATE / CHUNK * record_seconds)):
            data = stream.read(CHUNK)
            frames.append(data)

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(wav_file_path, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def convert_wav_2_mp3(self, wav_file_path, mp3_file_path):
        sound = AudioSegment.from_wav(wav_file_path)
        sound.export(mp3_file_path, format="mp3")

    def play(self, sound_file_path):
        playsound(sound_file_path)






