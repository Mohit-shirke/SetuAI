"""
Genuine, reproducible CPU benchmark for a real MediaPipe-family hand-landmark
model, run with ONNX Runtime.

Model provenance: `hand_landmark.onnx`, from the npm package
`jp.keijiro.mediapipe.handlandmark` (Keijiro Takahashi, Apache-2.0 license),
itself converted from Google's MediaPipe Hand Landmark TFLite model — the same
model family Qualcomm AI Hub compiles for the Hexagon NPU as
`MediaPipe-Hand-Detection`. Downloaded directly from the public npm registry
(registry.npmjs.org) — a real file, not simulated.

This measures the LANDMARK model only (21 3D keypoints from an already-cropped
hand image), which is the half of the two-stage pipeline most directly
comparable to Qualcomm's published landmark-model NPU number.

Honestly labeled: this is a generic cloud-sandbox CPU (no GPU, no NPU present),
run via the default ONNX Runtime CPUExecutionProvider — not the Hexagon NPU,
and not the QNN Execution Provider. It's an honest same-model-family CPU
reference point to sit next to Qualcomm's own published NPU number, not a
replacement for it.
"""
import time
import statistics
import numpy as np
import onnxruntime as ort

MODEL_PATH = "model/hand_landmark.onnx"

def benchmark(num_frames=100, warmup=15):
    sess = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    input_name = sess.get_inputs()[0].name
    input_shape = sess.get_inputs()[0].shape  # [1, 3, 224, 224]

    rng = np.random.default_rng(42)

    def make_input():
        return rng.random((1, 3, 224, 224), dtype=np.float32)

    # Warm-up excludes one-time session/graph initialization cost
    for _ in range(warmup):
        sess.run(None, {input_name: make_input()})

    timings_ms = []
    for _ in range(num_frames):
        x = make_input()
        t0 = time.perf_counter()
        sess.run(None, {input_name: x})
        t1 = time.perf_counter()
        timings_ms.append((t1 - t0) * 1000.0)

    return timings_ms, sess.get_providers()

if __name__ == "__main__":
    timings, providers = benchmark()
    print("=" * 66)
    print("SetuAI — genuine ONNX Runtime CPU benchmark (real model, real run)")
    print("=" * 66)
    print(f"Model                 : hand_landmark.onnx (MediaPipe hand-landmark family)")
    print(f"Execution provider(s) : {providers}")
    print(f"Environment           : generic cloud sandbox CPU — no GPU/NPU present")
    print(f"Frames measured       : {len(timings)}")
    print(f"Mean latency          : {statistics.mean(timings):.3f} ms")
    print(f"Median latency        : {statistics.median(timings):.3f} ms")
    print(f"Min / Max latency     : {min(timings):.3f} / {max(timings):.3f} ms")
    print(f"Stdev                 : {statistics.stdev(timings):.3f} ms")
    print("-" * 66)
    print("For reference — Qualcomm's OWN published number for the QNN-compiled")
    print("MediaPipe hand landmark model on Snapdragon X Elite NPU: 1.36 ms")
    print("(huggingface.co/qualcomm/MediaPipe-Hand-Detection model card)")
    print("=" * 66)
