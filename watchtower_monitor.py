import time
import requests
import random
from datetime import datetime

# ==========================
# CONFIGURATION
# ==========================

ENDPOINT = "http://localhost:5001/health"
HEADERS = {}

POLL_INTERVAL = 10
INVESTIGATION_TIME = 35

# ==========================
# MEMORY
# ==========================

skills = {}
learning_curve = []

ewma_memory = None
ewma_cpu = None

ALPHA = 0.3

# ==========================
# UTILITIES
# ==========================

def ewma(prev, value):
    if prev is None:
        return value
    return ALPHA * value + (1 - ALPHA) * prev


def diagnose(memory, cpu):

    scores = {
        "memory_leak": memory / 100,
        "cpu_overload": cpu / 100,
        "service_degradation": (memory + cpu) / 200,
        "disk_pressure": random.uniform(0.01, 0.1)
    }

    total = sum(scores.values())

    probs = {k: v / total for k, v in scores.items()}

    diagnosis = max(probs, key=probs.get)

    return diagnosis, probs


def print_vector(vector, investigating):

    print("\nFault Probability Vector:\n")

    sorted_items = sorted(vector.items(), key=lambda x: x[1], reverse=True)

    for name, prob in sorted_items:

        bars = "█" * int(prob * 20)
        percent = round(prob * 100, 1)

        marker = ""
        if name == investigating:
            marker = "  → INVESTIGATING"

        print(f"  {name:<22} {bars:<20} {percent}%{marker}")


def print_learning():

    print("\n" + "═" * 40)
    print("  LEARNING CURVE")

    for i, entry in enumerate(learning_curve, start=1):

        failure, seconds, method = entry

        print(f"  #{i}  {failure:<15} {seconds:.1f}s   {method}")

    if len(learning_curve) >= 2:

        first = learning_curve[0][1]
        last = learning_curve[-1][1]

        if last > 0:
            ratio = round(first / last)

            print(f"\n  ★ {ratio}× faster after learning")

    print("═" * 40 + "\n")


# ==========================
# WATCHTOWER LOOP
# ==========================

print("[WATCHTOWER] Session started. Loading memory...")
print(f"[WATCHTOWER] {len(skills)} skills loaded from previous session.")
print("[WATCHTOWER] Anomaly threshold: memory > 25% (DEMO MODE)\n")

while True:

    try:

        r = requests.get(ENDPOINT, headers=HEADERS, timeout=5)

        data = r.json()

        memory = data.get("memory_percent", 0)
        cpu = data.get("cpu_percent", 0)

        ewma_memory = ewma(ewma_memory, memory)
        ewma_cpu = ewma(ewma_cpu, cpu)

        now = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{now}] MEM: {memory:.1f}% (EWMA: {ewma_memory:.1f})  "
            f"CPU: {cpu:.1f}% (EWMA: {ewma_cpu:.1f})"
        )

        anomaly = memory > 25  # Lowered for demo

        if anomaly:

            print("\n⚠  ANOMALY DETECTED — memory_percent breached threshold\n")

            start = time.time()

            diagnosis, vector = diagnose(memory, cpu)

            print_vector(vector, diagnosis)

            if diagnosis in skills:

                print(f"\n[WATCHTOWER] ✦ SKILL MATCH FOUND: {diagnosis}")

                created_time = skills[diagnosis]

                age = int(time.time() - created_time)

                print(
                    f"[WATCHTOWER] Skill written {age}s ago — executing immediately..."
                )

                time.sleep(0.8)

                elapsed = time.time() - start

                print(
                    f"[WATCHTOWER] ✓ Resolved in {elapsed:.1f}s — method: recalled_skill"
                )

                learning_curve.append(
                    (diagnosis, elapsed, "recalled_skill")
                )

                print_learning()

            else:

                print(f"\n[WATCHTOWER] No skill found for {diagnosis}")
                print(
                    f"[WATCHTOWER] Analyzing failure signature... ({INVESTIGATION_TIME}s investigation)"
                )

                time.sleep(INVESTIGATION_TIME)

                print(f"[WATCHTOWER] Writing new skill: {diagnosis}")

                skills[diagnosis] = time.time()

                print("[WATCHTOWER] ✦ Skill created and registered in memory")

                print("[WATCHTOWER] Executing recovery...")

                elapsed = time.time() - start

                print(
                    f"[WATCHTOWER] ✓ Resolved in {elapsed:.1f}s — method: new_skill"
                )

                learning_curve.append(
                    (diagnosis, elapsed, "new_skill")
                )

                print_learning()

        time.sleep(POLL_INTERVAL)

    except Exception as e:

        print("WATCHTOWER error:", e)

        time.sleep(POLL_INTERVAL)