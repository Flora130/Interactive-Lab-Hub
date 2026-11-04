# Observant Systems: Overnight Sensation

**NAMES OF COLLABORATORS HERE**

Flora Zhang   Simone Xu 

## Overview

**Part 1: the tools**

**Part 2: Overnight Sensation**


# Part 1

## Part A. 
### Set up your Pi for on-device AI


```
pi@raspberrypi:~$ cd Interactive-Lab-Hub/Lab\ 5
pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python3 -m venv .venv
pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ source .venv/bin/activate
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ pip install -r requirements.txt
```

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python -c "from ultralytics import YOLO; YOLO('yolo26n.pt').export(format='ncnn')"
```

Test it on an image from the internet. `project=runs` keeps the output in this folder; without it, ultralytics writes to a `runs/` folder at the top of your git repo, where you will not think to look.

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ yolo predict model=yolo26n_ncnn_model source=https://ultralytics.com/images/bus.jpg project=runs
```

The result is in `runs/predict/bus.jpg`: boxes around the people and the bus.

Now a photo of your own. Plug in the webcam and take one with `snap.py` (`--delay 3` gives you three seconds to get into the frame), or copy a photo from your phone to the Pi with `scp`. Then run the same command on it:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python snap.py --delay 3
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ yolo predict model=yolo26n_ncnn_model source=snap.jpg project=runs
```


\*\*\***Include a screenshot of `ollama list` showing your models, and the `bus.jpg` result and your own photo with their boxes.**\*\*\*

<img height="400" alt="findPeople_Bus" src="https://github.com/user-attachments/assets/fd91d9bc-7e48-409c-8845-54b653b60a1a" />
<img height="400" alt="ollamaList" src="https://github.com/user-attachments/assets/cdf7baeb-08d2-4599-8230-732b721914c6" />


## Part B. 
### See: recognize people in real time with YOLO

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_person.py
```

Then press q to quit and run it again with a flag. Each one changes a single thing:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_person.py --conf 0.2     # lower the bar: see what the model is unsure about
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_person.py --conf 0.7     # raise the bar: see what you lose
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_person.py --all          # all 80 classes, not only people: what else is on your desk, and what does it get wrong?
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_person.py --headless     # no window, only the printed readings: how it runs over ssh, and at night
```

\*\*\***Include a short video or screenshots of the person detection. Write down three situations where it did not see you, or saw a person who was not there, and what you think the cause was.**\*\*\*

The three scenarios I have chosen in which the figures remain unseen are: the frame captures only a portion of a person’s clothing; the frame captures only a person’s accessories; and the figure appears elusive or indistinct.

Since the human face is a key element in identifying a person, the absence of facial features makes it easy for a model to confuse a person with other objects, resulting in a low detection rate for humans.

<p align="center">
<img width="200"  alt="yoloPerson" src="https://github.com/user-attachments/assets/effbb268-9926-45a0-a4c5-e5bd99ee8c9d" />
<img width="200" alt="yoloPerson2" src="https://github.com/user-attachments/assets/a1e66b09-02e0-4213-aeba-6b3e8834f28f" />
<img width="200" alt="yoloPerson3" src="https://github.com/user-attachments/assets/5e79bd22-5af4-4347-9eff-ccd59b9f1afe" />
<img width="200" alt="yoloPerson4" src="https://github.com/user-attachments/assets/49ecd464-5182-416b-a0ec-b29c2cd4eb79" />
</p>


## Part C. 
### See more: hands and pose with MediaPipe

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

\*\*\***Include a screenshot or short video of the hand pose demo, and write how you might use face, hand or body pose tracking in your observant system.**\*\*\*

I have found that the model is quite sensitive in its tracking of the hands, particularly regarding the movements of the fingers. The area of ​​the shape formed by connecting the fingertips can also be used to control music.
<p align="center">
<img width="300" alt="handpose" src="https://github.com/user-attachments/assets/c433ad8e-b019-458b-ac90-707a84966f2c" />
<img width="300" alt="yoloPerson5" src="https://github.com/user-attachments/assets/bee58700-3f3d-40b9-9cc6-70555089f8bf" />
</p>

## Part D. 
### Reason: run Qwen on the Pi with Ollama


```
pi@raspberrypi:~ $ ollama run qwen3.5:0.8b
>>> /set nothink
>>> Tell me a bit about the history of Roosevelt Island. Three sentences.
>>> /bye
```

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python ask_qwen.py "Tell me a bit about the history of Roosevelt Island."
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python ask_qwen.py --model qwen3:0.6b "Tell me a bit about the history of Roosevelt Island."
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python ask_qwen.py --image snap.jpg "What is in this photo?"
```


\*\*\***Ask Qwen three questions a bedside device might need to answer. Paste the questions, the answers and how long each took. Try one of them with `qwen3:0.6b` and compare.**\*\*\*

```
(.venv) pi@raspberrypiflora130:~/Interactive-Lab-Hub/Lab 5 $ ask_qwen.py "does a cup of warm milk help good sleep"
-bash: ask_qwen.py: command not found
(.venv) pi@raspberrypiflora130:~/Interactive-Lab-Hub/Lab 5 $ python ask_qwen.py "does a cup of warm milk help good sleep"
Yes, drinking warm milk can help improve sleep quality by soothing the stomach and providing warmth to the body.
[qwen3.5:0.8b, 3.8 s]
(.venv) pi@raspberrypiflora130:~/Interactive-Lab-Hub/Lab 5 $ python ask_qwen.py "What if I get a nightmare and wake up at 4am"
If you wake up at 4 AM, the first thing to do is ensure your room is dark before trying to sleep.
[qwen3.5:0.8b, 4.2 s]
(.venv) pi@raspberrypiflora130:~/Interactive-Lab-Hub/Lab 5 $ python ask_qwen.py "Does light music help a good sleep"
Yes, soft instrumental music can help improve sleep quality by reducing anxiety and lowering heart rate.
[qwen3.5:0.8b, 3.2 s]
(.venv) pi@raspberrypiflora130:~/Interactive-Lab-Hub/Lab 5 $ python ask_qwen.py --model qwen3:0.6b "What if I get a nightmare and wake up at 4am"
If you wake up at 4am, it's likely that the nightmare was a dream you had while you were asleep. You might feel confused or anxious, but it's okay to feel that way. If you're worried, you can try to stay calm and focus on the present moment. Let me know if you'd like help with anything else.
[qwen3:0.6b, 4.0 s]
```

## Part E. 
### Connect: from YOLO readings to Qwen reasoning

* `interpret(r)` is the interpreter. It takes one YOLO result and returns one reading. A person is *left*, *center* or *right* by which third of the frame the middle of their box is in, and *close* if the box is taller than 60% of the frame, *far* otherwise. The reading is a string like `1 person(s) at center/close`, or `nobody`. Fifteen lines, and they decide everything the model can know.
* `watch(seconds)` is the detector and the log. Twice a second it reads a frame, runs YOLO on it and calls `interpret()`. A time-stamped reading goes into the log **only when it differs from the previous one**, so a minute of sitting still is one line, not 120.
* `ask(log, question)` is the reasoner. It pastes the log and your question into one prompt, tells Qwen to answer in at most three sentences using only what is in the log, and sends it to Ollama with thinking off.


* **The question.** `--question "Did anyone leave?"`, `--question "Should I be worried?"`, `--question "Write one sentence a sleepy person would want to hear."` Same log, different job for the reasoner.
* **The interpreter.** Edit `interpret()`: drop the positions, add "standing" versus "sitting" (a sitting person's box is shorter and squarer), count only people who are close. Qwen's answers change because its world changed.
* **The other objects.** By default the detector is told to look for people only. With `--all` it reports all 80 classes and the interpreter adds them to the reading, as in `1 person(s) at center/close; also chair, cup`. Look closely at what it names: at 320 pixels a white chair, a bucket or a sink is a "toilet" often enough, and Qwen will faithfully report the toilet in your bedroom. Deciding which objects deserve a mention is interpreter work.
* **The log.** Every run saves `watch_log.txt`. Edit it so it contradicts itself and feed it back with `--log watch_log.txt`: the camera is skipped and Qwen reasons over your edited file. Does it notice?
* **The format.** `--json` gets `{"people": 1, "activity": "...", "unusual": false}` back, which is what you will want in Part 2 to drive a display or a sound.
* **The timing.** `--seconds 300` watches longer. `--every` logs every reading instead of only changes, so the log grows to hundreds of lines and Qwen has to find the changes itself. See whether it still can.

\*\*\***Document the pipeline: at least three runs with the log, the question, Qwen's answer, and whether it was right. Include one case where Qwen got it wrong, and say what you changed in the interpreter and why.**\*\*\*

In one experiment, I asked whether anyone had left the frame during a one-minute recording. Although I had stepped away from my seat—disappearing from the view entirely—the model concluded that no one had left. I suspect this occurred because the model’s confidence scores for detecting the person were consistently low; consequently, when the person was no longer visible, the model interpreted this as a detection error rather than an instance of someone leaving the frame. In a second attempt, I enabled all detection features and switched to a larger model, which then provided the correct answer along with a valid explanation.

<p align="center">
<img width="200"  alt="yolo1" src="https://github.com/user-attachments/assets/60f25027-deb4-4a87-b6dd-547f2b558d3e" />
<img width="200" alt="yolo2" src="https://github.com/user-attachments/assets/2d7b5d8e-f374-45b5-9a40-707f470a372b" />
<img width="200" alt="yolo3" src="https://github.com/user-attachments/assets/ed84b6e8-dbe2-455d-a634-ecfc91ed415f" />
</p>


# Lab 5 Part 2: Overnight Sensation
## Part F. 
### Read Part 2 and storyboard your night-time interaction

**Sleep Symphony** is a personalized alarm clock that tracks body movements during sleep and transforms them into a unique morning melody. More movement creates energetic music, while less movement produces calmer sounds.

Before Bed: Before going to sleep, the user activates sleep mode on their alarm clock. The clock responds with a soft light to acknowledge that it has started monitoring the user's body movements.

While Asleep: Throughout the night, the clock tracks how often the user moves or changes sleeping positions. It translates these movements into a personalized alarm melody. The more the user moves, the faster and more energetic the music becomes. A calmer night produces a softer, slower melody.

When Awake: In the morning, the user wakes up to their unique alarm melody, generated from the previous night's movements. Instead of viewing sleep statistics, they experience their night's activity through music, turning invisible sleep patterns into an auditory experience.

\*\*\***Insert ideas, sketches, Verplank diagrams and storyboards for your night-time interaction here.**\*\*\*

<img width="967" height="287" alt="sketch" src="https://github.com/user-attachments/assets/183d6da4-5514-41b6-a79a-e38c1ce51b06" />


## Prep for Part 2

 **Put the feedback for your ideas here.**

 My peers find this creative alarm clock concept quite interesting; it adds a pleasant surprise to the otherwise dull morning wake-up routine. However, tracking sleeping positions is a challenging design aspect—it not only tests the alarm clock’s recording angle but also raises the question of whether movements made beneath a duvet can be accurately detected.

\*\*\***Post your revised storyboard here.**\*\*\*

I’ve chosen to work with Simone on a project about pet monitoring.
\*\*\***Post your revised storyboard here.**\*\*\*

<img width="800" alt="image" src="https://github.com/user-attachments/assets/2889c2e6-b246-46d1-9bad-cbc68f617459" />

Simin drew this improved version by hand, using the feedback above and what the real run showed us (Part H).

Before: Fill the bowl, turn on a small lamp, hold an OK sign to the camera on the floor next to the bowl.

While asleep or busy: The cat comes to eat. Every 5s the camera writes where the cat is and saves a time-lapse frame. Sometimes it will break, logged a cat as a dog.

After: open "pipi.local:8000" on the phone to visit the website, which include the time-lapse video and motions of the cat.

What changed from the first storyboard: the camera now sits on the floor next to the bowl with a small lamp on, the middle panel shows where the pipeline breaks (one cat logged as a dog), the night also saves a time-lapse (1 frame every 10 s), and the morning is a web page on the phone plus the cat's line read out loud.

## Part G. 
### Design the interaction before

<details>
<summary>Instructions</summary>

The hand-off: the person tells the device what to watch tonight, and the device acknowledges it. Keep it to a thirty-second ritual. A button or a touch (Lab 4), a spoken sentence (Lab 3), a wave or a Quiet Coyote at the camera (Part C). The acknowledgement can be a line on the display, a tone, or an LED that dims rather than lights up. At its simplest, the hand-off just sets the question that the morning will answer.

</details>

\*\*\***Describe the interaction before.**\*\*\*

The hand-off uses the OK 👌 gesture from Simin's Part C answer: a gesture lets the user hand the night over while lying down, without getting close to the device.

How it works ([bedtime.py](bedtime.py)), run inside tmux as the README asks:

1. `tmux new -s night`, then `python bedtime.py` (add `--show` for a window on the Pi desktop).
2. The camera waits for an OK sign: thumb tip touching index tip while the middle, ring and pinky fingers stay straight. This is a rule over MediaPipe's 21 hand landmarks, like the gestures in `hand_pose.py`.
3. The sign has to be held for 15 frames in a row (about a second), so a hand passing by does not start the night.
4. The device acknowledges with "Good night. I will watch for your pet until morning." in the terminal, "Good night" in the window with `--show`, or out loud with `--speak` (off by default).
5. It writes the hand-off time into `night_log.jsonl` and starts the night shift, `overnight.py --all`.

In fake nights 3 and 4 the OK sign was recognized and the night shift started at 01:14:36 and 01:18:50.

For the real run on Nov 1, the OK sign got recognized at 20:27:56, it said good night, and the night shift started right after. `bedtime.py` now also passes any extra options on to `overnight.py`, so the whole thing starts with one command: `python bedtime.py --minutes 30 --lapse 10` (more on those options in Part H).

## Part H. 
### Incorporate the observant system

<details>
<summary>Instructions</summary>

The Part E pipeline becomes the night shift. `overnight.py` runs your `interpret()` from `yolo_to_qwen.py` every few seconds, people only unless you pass `--all`, and writes the readings to `night_log.jsonl`; the reasoning waits for the morning. Start it inside `tmux` so it keeps running after you close your laptop, and stop it with Ctrl-C in the morning:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ tmux new -s night
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python overnight.py
```

Fake a night first: run it for thirty seconds while you walk around, stop it, and run `morning.py` from Part I. When that looks right, run a real night. If your storyboard needs a sensor rather than the camera, swap in the Lab 4 example code and log its reading the same way.

</details>

\*\*\***Screenshots or videos of the running system.**\*\*\*

We changed `interpret()` in [yolo_to_qwen.py](yolo_to_qwen.py) so cats and dogs get a position, like people. A reading now looks like `nobody; 1 cat(s) at left/far`. `overnight.py` imports this function, so the night shift logs pets without other changes.

**Fake nights.** As the README says, we first ran `overnight.py --all` for about 40 seconds and then `morning.py`. The second fake night (full output in [logs/partH_fake_night2.log](logs/partH_fake_night2.log); the first is in [logs/partH_fake_night1.log](logs/partH_fake_night1.log)):

```
{"t": "2026-10-31T18:47:48", "reading": "1 person(s) at left/close"}
{"t": "2026-10-31T18:47:48", "alive": true}
{"t": "2026-10-31T18:48:09", "reading": "1 person(s) at center/close"}
{"t": "2026-10-31T18:48:19", "reading": "1 person(s) at left/close"}
{"t": "2026-10-31T18:48:24", "reading": "1 person(s) at center/close"}
```

`morning.py` said one person was observed at close range the whole time, which matches the log. It also said "the camera shifted focus to the center of the room at 18:48:09"; the camera did not move, the person moved from left to center. No cat appeared in the log, and the reading never became "nobody".

In the third fake night we ran the whole chain (`bedtime.py` → `overnight.py --all`) and held up a photo of a cat on a phone. YOLO labeled it "teddy bear", never "cat" ([logs/partH_fake_night3_full.log](logs/partH_fake_night3_full.log)). So we changed `overnight.py` to look at 640-pixel frames instead of 320, with a confidence bar of 0.25; `interpret()` keeps the old 0.4 bar for everything except cats and dogs. In the fourth fake night the same cat photo was logged 5 times in about a minute ([logs/partH_fake_night4_full.log](logs/partH_fake_night4_full.log)):

```
{"t": "2026-11-01T01:18:50", "handoff": "ok sign"}
{"t": "2026-11-01T01:18:58", "reading": "1 person(s) at center/close"}
{"t": "2026-11-01T01:19:08", "reading": "nobody; 1 cat(s) at left/close"}
{"t": "2026-11-01T01:19:13", "reading": "1 person(s) at center/close"}
{"t": "2026-11-01T01:19:18", "reading": "1 person(s) at center/close; 1 cat(s) at left/close; also laptop"}
{"t": "2026-11-01T01:19:29", "reading": "1 person(s) at center/close; 1 cat(s) at left/far"}
{"t": "2026-11-01T01:19:44", "reading": "1 person(s) at left/far; 1 cat(s) at left/far"}
```

Then the real run. To be upfront, it wasn't a whole night. The lab was due that same night, so on Nov 1 we ran it for 30 minutes, 20:28 to 20:58, with the camera on the floor next to the cat's food bowl (not pointed at a bed). For this we gave [overnight.py](overnight.py) two new options. `--minutes 30` makes it stop by itself. `--lapse 10` saves a frame with YOLO's boxes and the current reading every 10 seconds, and when the run ends it calls the new [lapse.py](lapse.py) to turn those frames into a time-lapse video. We wanted the time-lapse to be something the device leaves behind every night, not something we stitch together by hand afterwards. We also made `overnight.py` write a `stopped` line when it ends, because during a quiet stretch nothing new goes into the log, and then the log can't tell you when the watch actually ended.

Here's the time-lapse from those 30 minutes: [videos/sleepbot_timelapse_30min.mp4](videos/sleepbot_timelapse_30min.mp4) (180 frames, 18 seconds). The full log is [logs/real_night1_30min.jsonl](logs/real_night1_30min.jsonl). The cat came by twice, around 20:32 and again around 20:53. A piece of the log from the first visit:

```
{"t": "2026-11-01T20:27:56", "handoff": "ok sign"}
{"t": "2026-11-01T20:28:15", "reading": "nobody"}
{"t": "2026-11-01T20:32:14", "reading": "nobody; 1 cat(s) at right/close"}
{"t": "2026-11-01T20:32:19", "reading": "nobody"}
{"t": "2026-11-01T20:32:51", "reading": "nobody; 1 cat(s) at right/far"}
{"t": "2026-11-01T20:33:06", "reading": "nobody"}
{"t": "2026-11-01T20:33:48", "reading": "nobody; 1 cat(s) at right/far"}
{"t": "2026-11-01T20:33:53", "reading": "nobody; 1 dog(s) at right/far"}
{"t": "2026-11-01T20:33:58", "reading": "nobody; 1 dog(s) at right/far; also refrigerator"}
{"t": "2026-11-01T20:34:03", "reading": "nobody; 1 dog(s) at right/far"}
{"t": "2026-11-01T20:34:09", "reading": "nobody; 1 cat(s) at right/far"}
{"t": "2026-11-01T20:34:14", "reading": "nobody; 1 cat(s) at right/far; 1 dog(s) at right/far"}
```

<img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/a3ad1ba1-f5fa-49e2-8457-d38d1fac8154" />


That's the snapshot `overnight.py` saved at 20:34:14. There's one cat in it, but the log line for that moment says `1 cat(s) at right/far; 1 dog(s) at right/far`. YOLO put a cat box and a dog box on the same cat, and `interpret()` counts every box, so one cat turned into two pets. That's where our pipeline breaks. We only checked this one snapshot, but our guess is that the other "dog" lines are the same cat too.

We also did a second run right after: 10 minutes, with a look and a time-lapse frame every 3 seconds (`--interval 3 --lapse 3`). That's faster than the README's "one look every 5 to 30 seconds", but it was only for 10 minutes, and the Pi ended at 63.7°C. The cat didn't come back this time, so the whole log is just `nobody` (the quiet-night output is in Part I).

## Part I. 
### Design the interaction after

<details>
<summary>Instructions</summary>

The reveal. The night produced a log; the morning turns it into something a half-awake person can take in. `morning.py` is the smallest version: it asks Qwen for a three-sentence report.

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python morning.py
```

Make it yours: show the report on the Mini PiTFT, read it aloud with Piper from Lab 3, plot the night as a timeline, or ask for JSON (`--json`, Part D) and move a servo. Whatever you pick, make sure it is honest about a night in which nothing happened.

</details>

Our reveal is [morning_pet.py](morning_pet.py). The first version lists what the camera actually saw of the pet, taken from the log. Then Qwen guesses what the pet might have been saying at up to three of those moments, in the pet's own voice. The output is labeled as a guess, and the prompt tells Qwen to use only times and places from the log. If the log never shows a pet, it says so and does not ask the model. `--speak` reads the guess aloud with espeak-ng.

Run on the second fake night, which had no pet in it:

```
Watched 18:47 to 18:48
4 changes, 0 with a pet in view, 1 heartbeats
pet sightings per hour: {}

Quiet night. The camera watched from 18:47 to 18:48 and did not see your pet.
```

Run on the fourth fake night, with the cat photo:

```
Watched 01:18 to 01:19, handed over at 01:18 with an OK sign
10 changes, 5 with a pet in view, 1 heartbeats

What your pet might have said (a guess by Qwen):
01:19:08 "I'm just waiting for you to come back."
01:19:18 "Let me check if I missed my treat."
01:19:29 "Can we grab a snack before the sun goes down?"
```

The times are real sightings from the log. The words are Qwen's guess, and "before the sun goes down" does not fit a sighting at 1 a.m.

Then came the real run, and a few changes to `morning_pet.py`.

The first time we ran it on the real log, Qwen didn't guess anything. It just copied three log lines back, like `20:54:36 nobody; 1 cat(s) at right/far`. The small model gets lost in a long list of raw readings. So now `morning_pet.py` groups the sightings into visits to the bowls (if the cat is out of frame for less than 2 minutes, it's still the same visit) and only gives Qwen the visit times and how long each one lasted. It also tells Qwen the camera sits next to the food and water bowls. YOLO can't tell what the cat is doing, only where it is, but next to the bowls it's most likely eating or drinking, so the lines should be about food and water. Last, it asks for the answer in the form `[time] "what the cat says"`. We tried giving it example lines like "I'm full now" instead, and it just repeated them, so the format is all it gets.

Here's the real morning on the 30-minute log:

```
Watched 20:27 to 20:58, handed over at 20:27 with an OK sign
31 changes, 24 with a pet in view, 3 heartbeats
pet sightings per hour: {'20:00': 24}
visits to the bowls: 20:32-20:35 (3 min), 20:53-20:55 (2 min)

What your pet might have said (a guess by Qwen):

[20:32] "Oh wow, those bowls are so full! I'm starving."
[20:53] "Finally, enough to eat. Thanks for feeding me!"
```

With `--speak`, the Pi reads the lines out loud through the speaker. We ran it a few times and got something different every time, like "I'm so hungry right now!" / "It's been a long wait!", or "The water is so cold!". Once it skipped the 20:32 visit and only wrote one line. The visit times come from the log; the words are just Qwen's guess, and both the terminal and the page say so.

On the 10-minute run where the cat never showed up, it stays honest and doesn't call the model at all:

```
Watched 21:05 to 21:15
1 changes, 0 with a pet in view, 1 heartbeats
pet sightings per hour: {}
visits to the bowls: none

Quiet night. The camera watched from 21:05 to 21:15 and did not see your pet.
```

One more piece: we wanted the owner to be able to check on the cat the next day without opening a terminal. So `morning_pet.py` also writes a small web page, `report/index.html`, with the visits, the guessed lines, the time-lapse and some snapshots. `python morning_pet.py --serve` serves it from the Pi, and anyone on the home Wi-Fi can open http://pipi.local:8000 on their phone. It only serves that one folder, so everything stays on the Pi and the home network.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/c2664204-fc08-436c-9d6f-e34cc032be5b" />


(We made this screenshot on a laptop from the same log and one of the real Qwen replies, because the Pi was at home and we weren't. So it only has 3 of the 24 snapshots, and it says 20:55 instead of 20:58, since the laptop copy didn't have the time-lapse frames it uses to find the end time.)

The page itself is in [report/index.html](report/index.html) (GitHub shows it as code, so download the `report` folder and open `index.html` in a browser). And here's a screen recording of it at phone size, scrolling down while the time-lapse plays: [videos/sleepbot_morning_page.mp4](videos/sleepbot_morning_page.mp4). It was recorded from the same laptop copy, so it has the same two differences.

## Final documentation

<details>
<summary>Instructions</summary>

Document all the prototypes and iterations you have designed and worked on. The deliverables for this lab are writings, sketches, photos, and videos that show what your system:

* "Looks like": how the device sits in the room at night, and what it looks like at bedtime and in the morning.
* "Works like": the pipeline from detector to interpreter to log to reasoner, with a real night's data.
* "Acts like": how a person hands the night over and what they get back.

</details>

\*\*\***Include a short video of the whole system**\*\*\*

Here's our video of the whole system: [https://youtu.be/TojQvalwqxw](https://youtu.be/TojQvalwqxw)

[![Sleep bot for pet video](https://img.youtube.com/vi/TojQvalwqxw/hqdefault.jpg)](https://youtu.be/TojQvalwqxw)

**Looks like:** the webcam sits low on the floor, pointed at the cat's food bowl, not at a bed. This is what it sees (a time-lapse frame from 20:28:41, before the cat came):

<img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/4f19106c-e3b3-4f98-9610-76018262e3dc" />


And here's the webcam itself, on its little tripod on the floor, with the cable going off to the Pi. The cat came over to check it out right away:

<img width="150"  alt="image" src="https://github.com/user-attachments/assets/3a6482f2-0871-44e9-8d5f-ef4e6c703a23" />
<img width="150" alt="image" src="https://github.com/user-attachments/assets/f1afc9c1-ccb5-4997-b249-41218694029e" />



**Works like:** webcam → YOLO (`yolo26n`, all 80 classes, 640-pixel frames, one look every 5 s; every 3 s in the second run) → `interpret()` turns each look into one reading like `nobody; 1 cat(s) at right/far` → only changes go into `night_log.jsonl`, plus a snapshot whenever something's in view, plus a time-lapse frame every 10 s → when the run ends, `lapse.py` makes `lapse.mp4` → in the morning `morning_pet.py` groups the sightings into visits, asks Qwen (`qwen3.5:0.8b`) to guess what the cat said, reads it out loud and writes the web page. Real data: [logs/real_night1_30min.jsonl](logs/real_night1_30min.jsonl), with an excerpt in Part H.

**Acts like:** before, you hold up an OK sign, it says good night and starts watching. After, you get the visit times, the cat's "lines" read out loud, and a page on your phone with the time-lapse and snapshots. The video above shows the whole thing.

<details>
<summary>Instructions</summary>

As always, make sure you document contributions and ideas from others (and AI) explicitly in your writeup.

You are permitted (but not required) to work in groups and share a turn in; you are expected to make equal contribution on any group work you do, and N people's group project should look like N times the work of a single person's lab. Make sure the page for the group turn in is linked to your personal Interactive Lab Hub page.

</details>

## Deliverables & Submission for Lab 5

<details>
<summary>Instructions</summary>

For submission, the readme.md page for this lab should be edited to include the work you have done:
* Upload any materials that explain what you did, including your code and night log, into your Lab 5 repository, and link them in your Lab 5 readme.md.
* Labs are due on Sundays, make sure to submit your Lab 5 readme.md to Canvas.

</details>

<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>

  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
</details>
