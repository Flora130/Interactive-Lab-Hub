# Chatterboxes

**NAMES OF COLLABORATORS HERE**

Flora Zhang

[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://youtu.be/LZ0VJClIlRI?si=Yy84mcyVYuVV19mn)


## Prep for Part 1: Get the Latest Content and Pick up Additional Parts

Please check instructions in [prep.md](prep.md) and complete the setup.

Pick up Web Camera If You Don't Have One

Get the Latest Content


# Part 1

## Setup

```
pi@ixe00:~$ cd Interactive-Lab-Hub/Lab\ 3
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python3 -m venv .venv
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ source .venv/bin/activate
(.venv) pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $
```

Install the Python dependencies:

```
(.venv) $ pip install -r requirements.txt
```

This takes a few minutes. If you would like it to take considerably less time, [`uv`](https://docs.astral.sh/uv/) is a drop-in replacement for `pip` that is dramatically faster on the Pi:

```
(.venv) $ pip install uv && uv pip install -r requirements.txt
```

Then run the setup script, which installs the classic speech synthesizers, downloads the voice activity detection model, and pre-fetches a neural voice and a speech recognition model so you are not waiting on downloads during lab:

```
(.venv):~$ cd speech-scripts
(.venv) $ ./setup.sh
```


## A. Text to Speech

### The classic engines

```
(.venv) $ cd speech-scripts

(.venv) $ sudo apt update
(.venv) $ sudo apt install -y espeak festival festvox-kallpc16k

(.venv) $ ./espeak_demo.sh
(.venv) $ ./festival_demo.sh
```

### Neural TTS with Piper


```
(.venv) $ python3 -m piper.download_voices en_US-lessac-medium
```

[Piper](https://github.com/OHF-Voice/piper1-gpl) synthesizes speech with a small neural network, runs comfortably on the Pi 5, and sounds markedly better than the above.

```
(.venv) $ ./piper_demo.sh
```



\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*

I wrote flora_greeting.sh in the speech-scripts folder.

\*\***Then answer: Is the same greeting, in these different voices, the same greeting? Describe one concrete way the voice changed what the utterance seemed to mean or who seemed to be speaking.**\*\*

I don't think the same greeting feels exactly the same when spoken in different voices, even if the words are identical. 

For example, one voice sounded more robotic and formal, which made the greeting feel like a system notification. In comparison, the more natural Piper voice made “Hello Flora” feel more like it was coming from a person or an assistant speaking directly to me.

## B. Speech to Text

We use [faster-whisper](https://github.com/SYSTRAN/faster-whisper), a reimplementation of OpenAI's Whisper model that runs several times faster on CPU and does not require PyTorch. All processing happens on the Pi; nothing is sent to a server.

```
(.venv) $ python transcribe.py lookdave.wav
```

The transcript is not the interesting output here — the timings are. Run it again with a larger model and compare:

```
(.venv) $ python transcribe.py lookdave.wav --model base.en
(.venv) $ python transcribe.py lookdave.wav --model small.en
#  noted that the first run may take longer because the model is downloaded, and that the HF unauthenticated-request warning is expected and not an error.
```


\*\***Record a few seconds of your own speech (`arecord -d 5 -f cd -c 1 -r 16000 test.wav`) and transcribe it with at least two model sizes. Report the real-time factor for each. At what point does the accuracy improvement stop being worth the delay, for a system that has to answer you?**\*\*

For a conversational system, I don't think this small improvement is worth the additional delay. Once the model can correctly understand the meaning of the user's question, I would prioritize lower latency over minor improvements in transcription.

```
(.venv) pi@raspberrypiflora130:~/Interactive-Lab-Hub/Lab 3/speech-scripts $ python transcribe.py test.wav --model base.en

Test, test, 1, 2, 3, 1, 2, 3, test.

model            base.en (int8, beam=1)
audio duration   5.00s
model load       2.26s
transcription    2.45s
real-time factor 0.49x

(Model load is a one-time cost per process. In an interactive system you load once and keep the model resident  which is what listen.py does.)
(.venv) pi@raspberrypiflora130:~/Interactive-Lab-Hub/Lab 3/speech-scripts $ python transcribe.py test.wav --model base.en

Test, test, 1, 2, 3, 1, 2, 3, test.

model            base.en (int8, beam=1)
audio duration   5.00s
model load       0.67s
transcription    2.25s
real-time factor 0.45x

(Model load is a one-time cost per process. In an interactive system you load once and keep the model resident  which is what listen.py does.)
```

\*\***Write your own script that verbally asks for a numerical input (a phone number, zipcode, number of pets) and records the answer the respondent provides.**\*\* 

I asked the number of tote bags, and then record the answer as answer.wav in the folder


## C. Turn-taking: knowing when someone has stopped talking


We use a **voice activity detector** (VAD) to segment the microphone stream into utterances. `listen.py` runs Silero VAD continuously and hands each detected utterance to faster-whisper:

```
(.venv) $ cd speech-scripts
(.venv) $ python listen.py
```

Speak, pause, and watch it transcribe. Now change the endpointing threshold — the amount of silence the system requires before it decides your turn is over:

```
(.venv) $ python listen.py --min-silence 0.2
(.venv) $ python listen.py --min-silence 1.5
```

\*\***Try both extremes, and something in between. Describe what each one feels like to talk to. Note specifically: at 0.2s, what kinds of normal speech get cut off? At 1.5s, what does the delay make the system seem like?**\*\*

There is no correct value. A system that takes drink orders and a system that listens to someone think out loud want very different thresholds, and the right one depends on what your users are doing with their pauses.

### The complete loop

`echo_bot.py` puts the pieces together: it listens, endpoints, transcribes, and speaks a reply through Piper. The dialogue policy is deliberately trivial — it repeats what you said — so that everything you notice is a property of the timing rather than the content.

```
(.venv) $ python echo_bot.py
```

## D. Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.)

\*\***Post your storyboard and diagram here.**\*\*

My idea is a small owl-shaped speech assistant that sits on the user’s shoulder. The user presses the owl’s wing to activate listening, then whispers their message. After detecting a short pause, the owl stops listening, processes the speech, and repeats the message aloud at a normal volume. The user can press the wing again to cancel or stop the owl.

<img width="586" height="442" alt="截屏 2026-09-27 20 46 35" src="https://github.com/user-attachments/assets/c7446fb1-8e5c-4cbb-83b9-562522462371" />

**User whispers:** “Excuse me, Is this seat taken? Yes”

**[Owl waits for 1.5 seconds of silence to determine that the user has finished speaking by ending "Yes".]**

**[Owl processes the speech for approximately 1 seconds.]**

**Owl:** “Excuse me, is this seat taken?”

**Other person:** “No, you can sit here.”

\*\***Please describe and document your process.**\*\*


I started by thinking about situations where speech is useful but speaking at a normal volume may be difficult or uncomfortable. This led me to the idea of a small wearable speaker that could translate quiet speech into normal-volume speech.

I chose an owl-shaped device that sits on the user's shoulder because its position keeps the microphone close to the user's mouth without requiring them to hold another device. I then mapped the interaction into three main stages: listening to the user's quiet speech, processing it with speech-to-text, and speaking the message aloud with text-to-speech.

While developing the dialogue, I realized that deciding when the user has finished speaking is an important part of the interaction. I chose approximately 1–1.5 seconds of silence as the initial threshold. A shorter pause could interrupt users who pause naturally while speaking, while a longer pause could make the conversation feel unresponsive. I also added simple visual feedback so the user can tell when the owl is listening and processing.



## E. Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing. Please record this interaction (for example, using Zoom's record feature).

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*


https://github.com/user-attachments/assets/e9c63922-981b-4abe-ab8e-8816889b7516



---

# Lab 3 Part 2


## Prep for Part 2

One major improvement was making the interaction more automatic. In my original design, the user needed to manually activate the owl before speaking. In the redesigned version, the system continuously monitors microphone volume and uses different sound thresholds to decide what is happening.

I designed three main states:

Idle: Background noise stays below the threshold, so the owl does nothing.

Aware: A moderate sound level indicates that someone nearby may be speaking, but the owl does not record or respond yet.

Listening: A louder signal, which is more likely to come from the wearer because the microphone is closer to their mouth, triggers recording.

After the user stops speaking for a short period of time, the system transcribes the recorded speech and repeats it aloud through the speaker.



## Prototype your system

The redesigned interaction is:

Background noise → Idle

Nearby speech → Aware

Wearer speaks close to the microphone → Listening

User stops speaking → Processing

Whisper converts speech to text → Piper converts text back to speech

Owl repeats the message aloud → Return to Idle

The current system uses the microphone as its primary sensing input. Because the owl is intended to sit on the user's shoulder, the microphone is physically closer to the wearer than to other people. The prototype therefore uses sound intensity as a simple way of estimating whether the wearer or someone farther away is speaking.

Code file: (https://github.com/Flora130/Interactive-Lab-Hub/edit/Fall2026/Lab%203/owl_project)

## Test the system

In the current prototype, the system states are displayed in the terminal as IDLE, AWARE, LISTENING, PROCESSING, and SPEAKING. In a future version, these states could be communicated through the owl's LED eyes.

Video: (https://drive.google.com/file/d/1SgClAwjyc51_FreB8Bq7BL5Hw4T5WAG5/view?usp=sharing)

### What worked well about the system and what didn't?

The overall speech interaction worked well. During testing, the device did not trigger randomly under normal background noise, and it was able to recognize and accurately repeat short spoken sentences. The different sound thresholds also provided a simple way to distinguish background noise, nearby conversation, and speech directed toward the device.

The pre-buffer significantly improved transcription because the beginning of the user's sentence was no longer missed when the listening state was triggered.

One limitation is that sound intensity alone cannot reliably identify the wearer in every environment. A nearby loud sound or another person speaking close to the microphone could still trigger the listening state. The current system also has only a small number of preset phrases. Testers suggested adding more common expressions to make the device more useful in everyday situations.


### What worked well about the controller and what didn't?

The controller successfully managed the transitions between the different interaction states based on microphone input. The thresholds prevented low-level background noise from triggering the system, while louder close-range speech could automatically begin recording. Silence detection also allowed the device to stop recording without requiring the user to press a button.

One challenge was choosing the correct thresholds. If the listening threshold is too low, environmental speech may trigger the device. If it is too high, quiet speech from the wearer may not be detected. These values therefore need to be calibrated for the microphone, physical placement of the owl, and surrounding environment.

The current controller also communicates its state mainly through terminal messages. Adding LED feedback would make the interaction much easier to understand without looking at the computer.

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

One important lesson is that users should not need to think too much about when the device is ready to listen. The interaction felt more natural when the device automatically detected speech instead of requiring an explicit button press.

The testing also showed that turn-taking is very important. The system needs to recognize the beginning of the user's speech without cutting off the first words, while also waiting long enough after a pause before deciding that the user is finished. The pre-buffer and silence threshold were both important for making the interaction feel more reliable.

Feedback also suggested that predefined common phrases could complement direct transcription. A more autonomous version could combine accurate repetition with a larger library of frequently used expressions.

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

The system could record interaction data such as microphone audio, RMS volume, detected state, transcription, recording duration, silence duration, and whether the final speech output was correct. These data could be compared across users and environments to determine better thresholds for distinguishing the wearer from surrounding speakers.


Additional sensing modalities could improve the system. For example, an IMU could detect whether the owl is currently being worn on the user's shoulder, while proximity or directional audio sensing could help estimate whether speech is coming from the wearer or another person. Visual or LED feedback could also be logged to study whether users correctly understand the device's listening and processing states.


<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>

  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
</details>
