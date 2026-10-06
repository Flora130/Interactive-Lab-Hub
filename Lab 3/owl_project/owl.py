import time
import queue
import subprocess
import threading

import numpy as np
import sounddevice as sd
import soundfile as sf

from gpiozero import PWMLED
from faster_whisper import WhisperModel


# =========================
# SETTINGS
# =========================

LED_PIN = 17

SAMPLE_RATE = 16000
CHANNELS = 1

# 这些值后面需要根据你的麦克风重新 calibrate
SOUND_THRESHOLD = 0.015
WHISPER_THRESHOLD = 0.035

SILENCE_THRESHOLD = 0.012
SILENCE_DURATION = 1.2

AUDIO_FILE = "/tmp/owl_recording.wav"

WHISPER_MODEL = "base.en"

PIPER_MODEL = "en_US-lessac-medium"


# =========================
# LED
# =========================

led = PWMLED(LED_PIN)


def led_idle():
    led.value = 0


def led_aware():
    # 有人在附近讲话
    led.value = 0.3


def led_listening():
    # 用户正在对猫头鹰讲话
    led.value = 1.0


def led_speaking():
    led.value = 0.6


processing = False


def blink_processing():
    global processing

    while processing:
        led.value = 0.2
        time.sleep(0.25)

        led.value = 0.8
        time.sleep(0.25)


# =========================
# WHISPER
# =========================

print("Loading Whisper...")

whisper_model = WhisperModel(
    WHISPER_MODEL,
    device="cpu",
    compute_type="int8"
)

print("Whisper ready.")


def transcribe(filename):

    segments, info = whisper_model.transcribe(
        filename,
        beam_size=5
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()


# =========================
# PIPER
# =========================

def speak(text):

    print("OWL:", text)

    led_speaking()

    piper_process = subprocess.Popen(

        [
            "python3",
            "-m",
            "piper",

            "--model",
            PIPER_MODEL,

            "--output-raw"
        ],

        stdin=subprocess.PIPE,

        stdout=subprocess.PIPE
    )

    aplay_process = subprocess.Popen(

        [
            "aplay",
            "-r",
            "22050",
            "-f",
            "S16_LE",
            "-t",
            "raw",
            "-"
        ],

        stdin=piper_process.stdout
    )

    piper_process.stdin.write(
        text.encode()
    )

    piper_process.stdin.close()

    aplay_process.wait()

    led_idle()


# =========================
# COMMANDS
# =========================

def check_command(text):

    text_lower = text.lower()

    if "excuse me" in text_lower:

        speak("Excuse me.")

        return True


    if "thank you" in text_lower:

        speak("Thank you!")

        return True


    if "sorry" in text_lower:

        speak("I'm sorry.")

        return True


    return False


# =========================
# RECORD
# =========================

def record_until_silence():

    print("Listening...")

    led_listening()

    recorded_audio = []

    silence_start = None

    block_duration = 0.1

    block_size = int(
        SAMPLE_RATE * block_duration
    )

    while True:

        audio = sd.rec(
            block_size,
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32"
        )

        sd.wait()

        audio = audio.flatten()

        recorded_audio.append(audio)

        rms = np.sqrt(
            np.mean(audio ** 2)
        )

        print(
            f"\rRecording RMS: {rms:.4f}",
            end=""
        )

        # 检测 silence
        if rms < SILENCE_THRESHOLD:

            if silence_start is None:
                silence_start = time.time()

            elif (
                time.time() - silence_start
                >= SILENCE_DURATION
            ):

                print("\nUser stopped speaking.")

                break

        else:

            silence_start = None


    audio = np.concatenate(
        recorded_audio
    )

    sf.write(
        AUDIO_FILE,
        audio,
        SAMPLE_RATE
    )

    return AUDIO_FILE


# =========================
# PROCESS SPEECH
# =========================

def process_speech():

    global processing

    filename = record_until_silence()

    processing = True

    blink_thread = threading.Thread(
        target=blink_processing
    )

    blink_thread.start()

    print("Transcribing...")

    text = transcribe(filename)

    processing = False

    blink_thread.join()

    print("\nDetected:")
    print(text)

    if not text:

        led_idle()

        return


    # 看是不是 command
    if check_command(text):

        return


    # 普通情况：
    # 猫头鹰直接大声复述用户内容
    speak(text)


# =========================
# MAIN LOOP
# =========================

def main():

    print("Owl started.")

    led_idle()

    block_duration = 0.1

    block_size = int(
        SAMPLE_RATE * block_duration
    )

    while True:

        audio = sd.rec(
            block_size,
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32"
        )

        sd.wait()

        audio = audio.flatten()

        rms = np.sqrt(
            np.mean(audio ** 2)
        )

        print(
            f"\rRMS: {rms:.4f}",
            end=""
        )

        # -----------------
        # IDLE
        # -----------------

        if rms < SOUND_THRESHOLD:

            led_idle()


        # -----------------
        # AWARE
        # -----------------

        elif rms < WHISPER_THRESHOLD:

            led_aware()


        # -----------------
        # LISTENING
        # -----------------

        else:

            print(
                "\nUser detected."
            )

            process_speech()

            # 防止 speaker 声音
            # 又被 microphone 捕捉
            time.sleep(0.8)


# =========================

try:

    main()

except KeyboardInterrupt:

    print("\nStopping Owl.")

finally:

    led.off()
