# Third-party model attribution

**File:** `hand_landmark.onnx`
**Source:** npm package [`jp.keijiro.mediapipe.handlandmark`](https://www.npmjs.com/package/jp.keijiro.mediapipe.handlandmark) v2.1.1
**Author:** Keijiro Takahashi ([HandLandmarkBarracuda](https://github.com/keijiro/HandLandmarkBarracuda))
**License:** Apache-2.0 (included in this folder)
**Provenance:** ONNX export of Google's MediaPipe Hand Landmark TFLite model — the
same model family Qualcomm AI Hub compiles for the Hexagon NPU as
`MediaPipe-Hand-Detection`.

Used here strictly to produce a genuine, reproducible CPU latency benchmark
(`benchmark_onnx_real.py`) for this submission's documentation. Not used inside
the browser demo itself (the browser demo uses Google's official
`@mediapipe/hands` JS package, loaded live from jsDelivr).
