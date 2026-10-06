import time
import sys
import queue
import subprocess
import threading
from collections import deque

import numpy as np
import sounddevice as sd
import soundfile as sf

from faster_whisper import WhisperModel


# ============================================================
# SETTINGS
# ============================================================

SAMPLE_RATE = 16000
CHANNELS = 1

# 每个音频 block 的长度
BLOCK_DURATION = 0.1
BLOCK_SIZE = int(SAMPLE_RATE * BLOCK_DURATION)

# ------------------------------------------------------------
# Sound thresholds
# ------------------------------------------------------------

# 低于这个值：IDLE
SOUND_THRESHOLD = 0.015

# 超过这个值：认为用户在靠近猫头鹰讲话
WHISPER_THRESHOLD = 0.035

# 录音过程中，低于这个值认为是 silence
SILENCE_THRESHOLD = 0.012

# 连续安静多久后停止录音
SILENCE_DURATION = 1.2

# ------------------------------------------------------------
# Pre-buffer
# ------------------------------------------------------------

# 保存触发之前最近多少秒的声音
PRE_BUFFER_DURATION = 0.8

PRE_BUFFER_BLOCKS = int(
    PRE_BUFFER_DURATION / BLOCK_DURATION
)

# ------------------------------------------------------------
# Files / Models
# ------------------------------------------------------------

AUDIO_FILE = "/tmp/owl_recording.wav"

WHISPER_MODEL = "base.en"

PIPER_MODEL = "en_US-lessac-medium"

VOICES_DIR = "/home/pi/Interactive-Lab-Hub/Lab 3/voices"


# ============================================================
# AUDIO QUEUE
# ============================================================

audio_queue = queue.Queue()


def audio_callback(indata, frames, time_info, status):
    """
    Continuously receives microphone audio.
    """

    if status:
        print(status)

    audio_queue.put(indata.copy())


# ============================================================
# STATE DISPLAY
# ============================================================

def state_idle():
    print("\n[STATE] IDLE")


def state_aware(rms):
    print(
        f"\n[STATE] AWARE - RMS {rms:.4f}"
    )


def state_listening():
    print("\n[STATE] LISTENING")


def state_processing():
    print("[STATE] PROCESSING")


def state_speaking():
    print("\n[STATE] SPEAKING")


# ============================================================
# WHISPER
# ============================================================

print("Loading Whisper...")

whisper_model = WhisperModel(
    WHISPER_MODEL,
    device="cpu",
    compute_type="int8"
)

print("Whisper ready.")


def transcribe(filename):
    """
    Convert recorded audio to text.
    """

    segments, info = whisper_model.transcribe(
        filename,
        beam_size=5,
        vad_filter=True
    )

    text_parts = []

    for segment in segments:
        text_parts.append(
            segment.text.strip()
        )

    return " ".join(text_parts).strip()


# ============================================================
# PIPER
# ============================================================

def speak(text):
    """
    Convert text to speech using Piper
    and play it through aplay.
    """

    if not text:
        return

    print(f"\nOWL: {text}")

    state_speaking()

    piper_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "piper",

            "--model",
            PIPER_MODEL,

            "--data-dir",
            VOICES_DIR,

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

    # 清掉猫头鹰自己说话期间
    # microphone 收到的声音
    clear_audio_queue()

    # 给 speaker / microphone 一点缓冲
    time.sleep(0.8)

    clear_audio_queue()

    state_idle()


# ============================================================
# COMMANDS
# ============================================================

def check_command(text):
    """
    Check whether recognized speech matches
    one of the preset commands.
    """

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


# ============================================================
# QUEUE UTILITIES
# ============================================================

def clear_audio_queue():
    """
    Remove any old microphone audio.
    """

    while not audio_queue.empty():

        try:
            audio_queue.get_nowait()

        except queue.Empty:
            break


# ============================================================
# RECORDING
# ============================================================

def record_until_silence(pre_buffer):
    """
    Begin recording using audio that was already
    captured immediately before the trigger.

    This prevents the beginning of the user's
    sentence from being lost.
    """

    state_listening()

    print("Recording...")

    # Start with audio captured BEFORE trigger
    recorded_audio = list(pre_buffer)

    silence_start = None

    while True:

        audio = audio_queue.get()

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

        # ----------------------------------------
        # Silence detection
        # ----------------------------------------

        if rms < SILENCE_THRESHOLD:

            if silence_start is None:

                silence_start = time.time()

            elif (
                time.time() - silence_start
                >= SILENCE_DURATION
            ):

                print(
                    "\nUser stopped speaking."
                )

                break

        else:

            silence_start = None


    # ----------------------------------------
    # Save recording
    # ----------------------------------------

    audio = np.concatenate(
        recorded_audio
    )

    sf.write(
        AUDIO_FILE,
        audio,
        SAMPLE_RATE
    )

    print(
        f"Audio saved: {AUDIO_FILE}"
    )

    return AUDIO_FILE


# ============================================================
# PROCESS SPEECH
# ============================================================

def process_speech(pre_buffer):
    """
    Record -> Whisper -> command check -> Piper
    """

    filename = record_until_silence(
        pre_buffer
    )

    state_processing()

    print("Transcribing...")

    text = transcribe(filename)

    print("\nDetected:")
    print(text)


    # ----------------------------------------
    # Empty result
    # ----------------------------------------

    if not text:

        print(
            "No usable speech detected."
        )

        state_idle()

        return


    # ----------------------------------------
    # Preset command
    # ----------------------------------------

    if check_command(text):

        return


    # ----------------------------------------
    # Normal owl behavior:
    # repeat user's sentence loudly
    # ----------------------------------------

    speak(text)


# ============================================================
# MAIN
# ============================================================

def main():

    print("\nOwl started.")

    print(
        "Waiting for speech..."
    )

    state_idle()


    # Holds approximately the latest 0.8 seconds
    # of microphone audio
    pre_buffer = deque(
        maxlen=PRE_BUFFER_BLOCKS
    )


    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        blocksize=BLOCK_SIZE,
        callback=audio_callback
    ):

        while True:

            audio = audio_queue.get()

            audio = audio.flatten()

            # Keep recent audio
            pre_buffer.append(
                audio.copy()
            )

            rms = np.sqrt(
                np.mean(audio ** 2)
            )

            print(
                f"\rRMS: {rms:.4f}",
                end="",
                flush=True
            )


            # ==================================================
            # IDLE
            # ==================================================

            if rms < SOUND_THRESHOLD:

                continue


            # ==================================================
            # AWARE
            # ==================================================

            elif rms < WHISPER_THRESHOLD:

                state_aware(rms)

                continue


            # ==================================================
            # USER DETECTED
            # ==================================================

            else:

                print(
                    f"\nUser detected. "
                    f"RMS = {rms:.4f}"
                )

                # Copy current pre-buffer
                captured_pre_buffer = list(
                    pre_buffer
                )

                # Clear old samples so recording
                # continues from this point forward
                clear_audio_queue()

                process_speech(
                    captured_pre_buffer
                )

                # Reset after speaking
                pre_buffer.clear()

                clear_audio_queue()


# ============================================================
# START
# ============================================================

try:

    main()


except KeyboardInterrupt:

    print(
        "\n\nStopping Owl."
    )


except Exception as e:

    print(
        "\n\nAn error occurred:"
    )

    print(e)
