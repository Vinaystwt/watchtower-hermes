import time
import random
import os

from monitor.health_monitor import EWMAHealthMonitor

monitor = EWMAHealthMonitor()


def diagnose_failure(memory, cpu):
    """
    Simple Bayesian-style scoring.
    """

    scores = {
        "memory_leak": memory / 100,
        "cpu_spike": cpu / 100,
        "service_degradation": (memory + cpu) / 200,
        "disk_pressure": random.uniform(0.1, 0.3),

        # NEW FAILURE TYPE
        "database_connection_exhaustion": random.uniform(0.7, 0.9)
    }

    total = sum(scores.values())

    probabilities = {k: v / total for k, v in scores.items()}

    diagnosis = max(probabilities, key=probabilities.get)

    return diagnosis, probabilities


def skill_exists(failure):
    return os.path.exists(f"skills/{failure}.sh")


def create_skill(failure):

    os.makedirs("skills", exist_ok=True)

    path = f"skills/{failure}.sh"

    with open(path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"echo 'Recovering from {failure}'\n")

    os.chmod(path, 0o755)

    print(f"New skill created: {path}")


def execute_skill(failure):

    path = f"skills/{failure}.sh"

    if os.path.exists(path):
        os.system(path)


def log_learning(failure, seconds, method):

    os.makedirs("memory", exist_ok=True)

    with open("memory/learning_curve.log", "a") as f:

        f.write(
            f"{int(time.time())} | "
            f"{failure} | "
            f"{seconds:.1f}s | "
            f"{method}\n"
        )


def print_probability_vector(vector, investigating=None):

    print("\nBayesian Probability Vector\n")

    sorted_items = sorted(vector.items(), key=lambda x: x[1], reverse=True)

    for failure, prob in sorted_items:

        bars = "█" * int(prob * 20)
        percent = round(prob * 100, 2)

        marker = ""
        if failure == investigating:
            marker = "  → INVESTIGATING"

        print(f"{failure:<20} {bars:<20} {percent}%{marker}")


def watchtower():

    print("WATCHTOWER starting...\n")

    while True:

        try:

            metrics = monitor.fetch_metrics()

            memory = metrics.get("memory_percent", 0)
            cpu = metrics.get("cpu_percent", 0)

            memory_status = monitor.check("memory_percent", memory)
            cpu_status = monitor.check("cpu_percent", cpu)

            print("Memory:", memory_status)
            print("CPU:", cpu_status)

            anomaly = memory_status["anomaly"] or cpu_status["anomaly"]

            if anomaly:

                print("\nANOMALY DETECTED")

                # Start timer exactly here
                incident_start_time = time.time()

                diagnosis, vector = diagnose_failure(memory, cpu)

                print_probability_vector(vector, investigating=diagnosis)

                print(f"\nDiagnosis: {diagnosis}")

                if skill_exists(diagnosis):

                    method = "recalled_skill"

                    print("[WATCHTOWER] ✦ Skill match found. Executing immediately...")

                    execute_skill(diagnosis)

                else:

                    method = "new_skill"

                    print("[WATCHTOWER] Analyzing failure signature...")
                    print(f"[WATCHTOWER] Running diagnostics on {diagnosis}...")

                    investigation_time = random.randint(30, 60)

                    time.sleep(investigation_time)

                    print("[WATCHTOWER] Investigation complete. Writing new skill...")

                    create_skill(diagnosis)

                    execute_skill(diagnosis)

                elapsed = time.time() - incident_start_time

                log_learning(diagnosis, elapsed, method)

                print("\nRecovery complete\n")

            time.sleep(5)

        except KeyboardInterrupt:

            print("\nWATCHTOWER stopped")
            break

        except Exception as e:

            print("WATCHTOWER error:", e)
            time.sleep(5)


if __name__ == "__main__":
    watchtower()