"""
Self-measured CPU reference benchmark for the hand-landmark pipeline used in SetuAI.

WHAT THIS IS: an honest, reproducible measurement of how long the MediaPipe hand
detector + landmark model pipeline takes to process one frame, run locally on this
machine's CPU (no GPU, no NPU, no Qualcomm hardware available in this environment).

WHAT THIS IS NOT: this is NOT the Snapdragon Hexagon NPU number. That number
(1.36 ms on a Snapdragon X Elite CRD) is Qualcomm's own published benchmark for
their QNN-compiled export of the same model family, cited from their AI Hub model
card, not something we measured ourselves.

We report both, side by side, and label each one honestly, because conflating
"a number we measured on a generic cloud CPU" with "Qualcomm's own NPU benchmark"
would be a dishonest technical claim.
"""
import time
import statistics
import numpy as np
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

def make_synthetic_frame(width=640, height=480, seed=0):
    """Deterministic pseudo-camera frame (worst case for the palm detector:
    no real hand is present, so the model must run its full detection pass
    every single frame rather than the cheaper tracking-only path)."""
    rng = np.random.default_rng(seed)
    return rng.integers(0, 255, (height, width, 3), dtype=np.uint8)

def benchmark(num_frames=60, warmup=10):
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5,
    ) as hands:
        frame = make_synthetic_frame()

        # Warm-up: exclude one-time model load / graph construction cost
        for _ in range(warmup):
            hands.process(frame)

        timings_ms = []
        for i in range(num_frames):
            frame = make_synthetic_frame(seed=i)
            t0 = time.perf_counter()
            hands.process(frame)
            t1 = time.perf_counter()
            timings_ms.append((t1 - t0) * 1000.0)

        return timings_ms

if __name__ == "__main__":
    timings = benchmark()
    print("=" * 60)
    print("SetuAI — self-measured CPU reference benchmark")
    print("Environment: generic cloud sandbox CPU (no GPU/NPU present)")
    print("Model: MediaPipe Hands (palm detector + landmark model)")
    print("=" * 60)
    print(f"Frames measured        : {len(timings)}")
    print(f"Mean latency           : {statistics.mean(timings):.2f} ms")
    print(f"Median latency         : {statistics.median(timings):.2f} ms")
    print(f"Min / Max latency      : {min(timings):.2f} / {max(timings):.2f} ms")
    print(f"Stdev                  : {statistics.stdev(timings):.2f} ms")
    print("-" * 60)
    print("For reference — Qualcomm's OWN published number for the QNN-compiled")
    print("MediaPipe-Hand-Detection model on Snapdragon X Elite NPU: 1.36 ms")
    print("(source: huggingface.co/qualcomm/MediaPipe-Hand-Detection model card)")
    print("=" * 60)
