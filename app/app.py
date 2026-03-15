from flask import Flask, jsonify
import psutil, time, threading

app = Flask(__name__)

_memory_leak_buffer = []
_leak_active = False

START_TIME = time.time()

def memory_leak_injector():
    global _leak_active, _memory_leak_buffer
    time.sleep(300)
    _leak_active = True
    print("[INJECTED] Memory leak started", flush=True)

    while _leak_active:
        _memory_leak_buffer.append("x" * 1024 * 50)
        time.sleep(1)

def cpu_spike_injector():
    time.sleep(600)
    print("[INJECTED] CPU spike started", flush=True)

    end_time = time.time() + 120
    while time.time() < end_time:
        _ = [i**2 for i in range(100000)]

def service_degradation_injector():
    time.sleep(900)
    print("[INJECTED] Service degradation started", flush=True)

@app.route('/health')
def health():
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.1)

    return jsonify({
        "status": "ok",
        "memory_percent": mem.percent,
        "memory_used_mb": mem.used // (1024 * 1024),
        "cpu_percent": cpu,
        "timestamp": time.time(),
        "uptime_seconds": time.time() - START_TIME
    })

@app.route('/status')
def status():
    return jsonify({
        "service": "vertex-app",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    threading.Thread(target=memory_leak_injector, daemon=True).start()
    threading.Thread(target=cpu_spike_injector, daemon=True).start()
    threading.Thread(target=service_degradation_injector, daemon=True).start()

    print("[VERTEX-APP] Started. Failures will inject automatically.", flush=True)

    app.run(host="0.0.0.0", port=5001)