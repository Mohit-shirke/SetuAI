# SetuAI — 3-Minute Pitch Script

Use this as a spoken guide, not a script to read word-for-word. Timings assume a ~3 minute slot; cut the bracketed sections first if you're given less time.

---

**[0:00–0:30] Open with the number, not the tech**

"India has about 18 million deaf people. It has about 300 certified sign language interpreters. That's one interpreter for every 60,000 deaf Indians. For almost everyone in that gap, a hospital visit, a bank appointment, a classroom — depends on a family member translating, or doesn't happen at all.

I didn't want to build another app that needs a data plan to fix that. I wanted something that works in a village clinic with no signal, for free, forever. That's SetuAI."

**[0:30–1:15] Show, don't tell — live demo**

*(Turn on the camera live in front of the judges.)*

"This is running right now, in this browser tab, with no internet connection required for the vision part. Watch — [hold up 1, 2, 3 fingers] — those are genuine ISL numerals. [Make a fist, then a thumbs-up] — these are common gestures I'm using to show the pipeline handles more than counting.

Every one of these is being read by a hand-tracking model running as WebAssembly, locally, in this tab. No frame of this video is going anywhere. That's the entire point."

**[1:15–2:00] Be honest about scope — this builds trust with judges**

"I want to be upfront about something, including a mistake I caught and fixed. My first draft labeled a fist, a thumbs-up, and a couple of other shapes as ISL signs for 'no,' 'yes,' and 'I love you.' When I actually checked ISL references, that was wrong — those are ASL or generic international gestures, not ISL. The only genuinely ISL part of this vocabulary is the numbers 1 through 5, which do follow the real ISL finger-counting convention. I've corrected every label in the demo and the docs to reflect that, and I'd rather show you a smaller, fully accurate claim than a bigger, wrong one."

But the architecture is real, and it's exactly the shape of a production Snapdragon app: Qualcomm AI Hub already publishes this exact hand-landmark model, benchmarked at 1.36 milliseconds on a Snapdragon X Elite NPU. Swap my in-browser rule-based classifier for a trained model on the ISLTranslate corpus — 31,000 real ISL sentence pairs from IIT Kanpur — and you have a genuine two-handed, continuous ISL interpreter, still running entirely offline on the Hexagon NPU."

**[2:00–2:30] Why Snapdragon, specifically**

"This only works if it's on-device. A cloud API charges per call — this needs to run dozens of times a day, for free, forever, for people who often can't afford a subscription. A cloud API needs connectivity — this needs to work exactly where connectivity is worst. And a cloud API means a camera feed of someone's medical visit or bank appointment leaves their device. None of those are acceptable for this use case. The NPU isn't a nice-to-have here — it's the only way this actually reaches the people it's for."

**[2:30–3:00] Close**

"This is a bridge — 'setu' — between silence and speech, and I built it to need nothing but the device it's running on. Thank you."

---

## Anticipated judge questions (and honest answers)

**"How accurate is the gesture recognition really?"**
> "For the 9 static, single-hand shapes in this demo, quite reliable — it's the same geometric approach production libraries use for coarse gesture classification, and the 8-frame stabilizer filters out motion blur. It will not recognize continuous ISL sentences; that requires the trained temporal model described in the roadmap, which is future work, not something I'm claiming today."

**"Why not just use an existing ISL dataset to train a real classifier right now?"**
> "That's exactly phase 2 of the roadmap. Given the timeline, I chose to ship something completely real and testable today — genuine on-device inference, not a mockup — rather than a training pipeline I couldn't fully validate in time. I'd rather hand you something honest and working than something impressive-sounding and untested."

**"How is this different from [SignAble / other ISL apps]?"**
> "Most existing tools are either video-relay services that need a live human interpreter and a connection, or they translate text into signed animation — the opposite direction from what a deaf person needs to communicate outward. This is sign-to-speech, with no interpreter and no connection required, in either direction."

**"What happens if the camera can't see the whole hand?"**
> "The demo requires the hand mostly in frame; a production version would add prompts guiding hand placement, plus fallback to the reverse (type-to-display) channel, so communication never fully breaks even if a sign isn't caught."
