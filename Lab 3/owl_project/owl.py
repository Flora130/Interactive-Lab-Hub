import time
import subprocess
import threading
import sys

import numpy as np
import sounddevice as sd
import soundfile as sf

from faster_whisper import WhisperModel


# =========================
# SETTINGS
# =========================

SAMPLE_RATE = 16000
CHANNELS = 1

# 这些值之后根据实际麦克风数据继续 calibrate
SOUND_THRESHOLD = 0.015
WHISPER_THRESHOLD = 0.035

SILENCE_THRESHOLD = 0.012
SILENCE_DURATION = 1.2

AUDIO_FILE = "/tmp/owl_recording.wav"

WHISPER_MODEL = "base.en"

PIPER_MODEL = "en_US-lessac-medium"


# =========================
# STATE / LED PLACEHOLDER
# =========================

def led_idle():
    print("\n[STATE] IDLE")


def led_aware():
    print("\n[STATE] AWARE")


def led_listening():
    print("\n[STATE] LISTENING")


def led_speaking():
    print("\n[STATE] SPEAKING")


processing = False


def blink_processing():
    global processing

    while processing:
        print("[STATE] PROCESSING")
        time.sleep(0.5)


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
    print(f"\nOWL: {text}")

    led_speaking()

    piper_process = subprocess.Popen(
        [
            sys.executable,
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
        (text + "\n").encode("utf-8")
    )

    piper_process.stdin.close()

    aplay_process.wait()
    piper_process.wait()

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
    print("\nListening...")

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
            end="",
            flush=True
        )

        # -----------------
        # SILENCE DETECTION
        # -----------------

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

    print("\nTranscribing...")

    text = transcribe(filename)

    processing = False

    blink_thread.join()

    print("\nDetected:")
    print(text)

    if not text:
        print("No speech detected.")
        led_idle()
        return


    # -----------------
    # CHECK COMMANDS
    # -----------------

    if check_command(text):
        return


    # -----------------
    # NORMAL REPEAT
    # -----------------

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
            end="",
            flush=True
        )


        # =================
        # IDLE
        # =================

        if rms < SOUND_THRESHOLD:
            pass


        # =================
        # AWARE
        # =================

        elif rms < WHISPER_THRESHOLD:
            print(
                f"\n[STATE] AWARE - RMS {rms:.4f}"
            )


        # =================
        # LISTENING
        # =================

        else:
            print(
                f"\nUser detected. RMS = {rms:.4f}"
            )

            process_speech()

            # 防止猫头鹰自己播放的声音
            # 马上再次触发麦克风
            time.sleep(0.8)


# =========================
# START
# =========================

try:
    main()

except KeyboardInterrupt:
    print("\nStopping Owl.")

except Exception as e:
    print("\nError:")
    print(e)
