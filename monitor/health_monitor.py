import requests
import math
from datetime import datetime


class EWMAHealthMonitor:
    """
    EWMA anomaly detection for WATCHTOWER.
    Polls the Flask patient on port 5001 and checks if metrics
    drift outside statistical control limits.
    """

    def __init__(self, lambda_param=0.3, sigma_multiplier=3.0):
        self.lam = lambda_param
        self.L = sigma_multiplier
        self.ewma = {}

        # Baselines calibrated to your system (~29% memory at rest)
        self.baselines = {
            "memory_percent": {"mean": 30.0, "std": 5.0},
            "cpu_percent": {"mean": 5.0, "std": 10.0},
        }

    def fetch_metrics(self):
        """
        Pull metrics from the patient server.
        NOTE: patient runs on port 5001.
        """
        try:
            response = requests.get("http://localhost:5001/health", timeout=5)
            return response.json()
        except Exception as e:
            return {
                "error": str(e),
                "memory_percent": 0,
                "cpu_percent": 0
            }

    def update_ewma(self, metric, value):
        if metric not in self.ewma:
            self.ewma[metric] = value
        else:
            self.ewma[metric] = (
                self.lam * value + (1 - self.lam) * self.ewma[metric]
            )
        return self.ewma[metric]

    def get_control_limits(self, metric):
        baseline = self.baselines.get(metric, {"mean": 50, "std": 10})

        mu = baseline["mean"]
        sigma = baseline["std"]

        factor = math.sqrt(self.lam / (2 - self.lam))

        ucl = mu + self.L * sigma * factor
        lcl = mu - self.L * sigma * factor

        return ucl, lcl

    def check(self, metric, value):
        ewma_val = self.update_ewma(metric, value)
        ucl, lcl = self.get_control_limits(metric)

        anomaly = ewma_val > ucl or ewma_val < lcl

        return {
            "metric": metric,
            "value": round(value, 2),
            "ewma": round(ewma_val, 2),
            "ucl": round(ucl, 2),
            "lcl": round(lcl, 2),
            "anomaly": anomaly,
            "timestamp": datetime.now().isoformat()
        }