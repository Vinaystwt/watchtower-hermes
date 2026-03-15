class BayesianFailureAnalyzer:

    def __init__(self):

        self.failure_patterns = {
            "memory_leak": {"memory_percent": 90, "cpu_percent": 20},
            "cpu_spike": {"memory_percent": 40, "cpu_percent": 90},
            "service_degradation": {"memory_percent": 60, "cpu_percent": 60},
            "disk_pressure": {"memory_percent": 75, "cpu_percent": 30}
        }

    def analyze(self, metrics):

        memory = metrics.get("memory_percent", 0)
        cpu = metrics.get("cpu_percent", 0)

        scores = {}

        for failure, pattern in self.failure_patterns.items():

            score = (
                abs(memory - pattern["memory_percent"]) +
                abs(cpu - pattern["cpu_percent"])
            )

            scores[failure] = score

        # convert scores to probabilities
        inverted = {k: 1/(v+1) for k,v in scores.items()}
        total = sum(inverted.values())

        probabilities = {
            k: round((v/total)*100,2) for k,v in inverted.items()
        }

        ranked = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

        diagnosis = ranked[0][0]

        return {
            "diagnosis": diagnosis,
            "probabilities": ranked
        }