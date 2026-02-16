# Solution for Exercise 01: Polling vs Webhook Speed Test
# Week 5 Day 3

import time
import os
import threading
import requests
from flask import Flask, request
import logging

# Suppress Flask logs for cleaner output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def polling_demo():
    print("\n--- 1. POLLING DEMO ---")
    FILENAME = "alert.txt"
    
    # Trigger Thread (Writes file)
    def trigger():
        time.sleep(0.5)
        with open(FILENAME, "w") as f:
            f.write(str(time.time()))
        print(f"[TRIGGER] File Created at {time.time():.4f}")
        
    threading.Thread(target=trigger).start()
    
    # Poller Loop (Checks every 0.2s)
    # Even 0.2s is slow compared to webhook
    start_poll = time.time()
    while True:
        if os.path.exists(FILENAME):
            now = time.time()
            with open(FILENAME, "r") as f:
                content = f.read().strip()
                if content:
                    sent_time = float(content)
                    delay = (now - sent_time) * 1000
                    print(f"[POLLER] Detected file at {now:.4f}")
                    print(f"Latency: {delay:.2f} ms (Polling Interval: 200ms)")
            os.remove(FILENAME)
            break
        time.sleep(0.2)
        if time.time() - start_poll > 5:
            print("Timeout!")
            break

def webhook_demo():
    print("\n--- 2. WEBHOOK DEMO ---")
    app = Flask(__name__)
    
    @app.route('/alert', methods=['POST'])
    def alert():
        data = request.json
        sent_time = data['timestamp']
        now = time.time()
        delay = (now - sent_time) * 1000
        print(f"[WEBHOOK] Received POST at {now:.4f}")
        print(f"Latency: {delay:.2f} ms (Instant!)")
        # Kill server for demo purposes
        func = request.environ.get('werkzeug.server.shutdown')
        if func: func()
        return "OK"
        
    # Start Server in Thread
    server = threading.Thread(target=lambda: app.run(port=5001))
    server.start()
    time.sleep(1) # Wait for server boot
    
    # Trigger (Client)
    print(f"[TRIGGER] Sending POST at {time.time():.4f}")
    requests.post('http://localhost:5001/alert', json={'timestamp': time.time()})
    
    server.join()

if __name__ == "__main__":
    polling_demo()
    time.sleep(1)
    webhook_demo()
