import sys
import time
import threading
from bypass import QuantumObliteration

def attack(target, threads, attack_type):
    print(f"[*] Starting attack on {target} with {threads} threads...\n")
    attack_instance = QuantumObliteration(target, attack_type)
    attack_instance.attack(threads)

def main():
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("python main.py <target> <threads>")
        print("python main.py -ip <IP Address> <threads>")
        print("python main.py -a <target> <threads>\n")
        sys.exit(1)

    if sys.argv[1] == "-ip":
        target = sys.argv[2]
        attack_type = "IP"
    elif sys.argv[1] == "-a":
        target = sys.argv[2]
        attack_type = "DOMAIN"
    else:
        target = sys.argv[1]
        attack_type = "DOMAIN"

    threads = int(sys.argv[3]) if sys.argv[1] in ["-ip", "-a"] else int(sys.argv[2])

    attack(target, threads, attack_type)

if __name__ == "__main__":
    main()
