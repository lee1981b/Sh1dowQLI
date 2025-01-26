import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def animation():
    text = "Welcome to Sh1dowQLI"
    clear()
    for i in range(len(text) + 1):
        clear()
        print(Fore.YELLOW + text[:i] + Style.BRIGHT)
        time.sleep(0.1)
    time.sleep(0.2)

def banner():
    print(Fore.MAGENTA + "╔═══════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + r"""
 ███████╗██╗  ██╗ ██╗██████╗  ██████╗ ██╗    ██╗ ██████╗ ██╗     ██╗
 ██╔════╝██║  ██║███║██╔══██╗██╔═══██╗██║    ██║██╔═══██╗██║     ██║
 ███████╗███████║╚██║██║  ██║██║   ██║██║ █╗ ██║██║   ██║██║     ██║
 ╚════██║██╔══██║ ██║██║  ██║██║   ██║██║███╗██║██║▄▄ ██║██║     ██║
 ███████║██║  ██║ ██║██████╔╝╚██████╔╝╚███╔███╔╝╚██████╔╝███████╗██║
 ╚══════╝╚═╝  ╚═╝ ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝  ╚══▀▀═╝ ╚══════╝╚═╝
    """)
    print(Fore.MAGENTA + "╚═══════════════════════════════════════════════════════════════════╝")
    print(Fore.GREEN + "╔══════════════════════════════════════════════════════════╗")
    print(Fore.GREEN + "|                    Made by hexsh1dow                     |")
    print(Fore.GREEN + "╚══════════════════════════════════════════════════════════╝")

def credits():
    clear()
    print(Fore.YELLOW + "╔════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + """
[+] Tool: Sh1dowQLI
[+] Author: @hexsh1dow
[+] Features: Error-Based SQLi, Time-Based SQLi
[+] Version: 2.1
    """)
    print(Fore.YELLOW + "╚════════════════════════════════════════════════════════╝")
    input(Fore.CYAN + "[*] Press Enter to return to the main menu...")

def all_in_one():
    clear()
    banner()
    print(Fore.YELLOW + "[*] Running All-in-One SQL Injection Tests...\n")
    print(Fore.MAGENTA + "[!] Ensure the URL includes '*' where payloads will be tested.\n")
    target = input(Fore.CYAN + "[?] Enter the target URL (e.g., https://example.com): ").strip()

    if not target:
        print(Fore.RED + "[!] Invalid input. URL cannot be empty.")
        input(Fore.CYAN + "[*] Press Enter to return to the menu...")
        return

    print(Fore.GREEN + f"[*] Target set to: {target}\n")

    print(Fore.YELLOW + "[*] Running Error-Based SQL Injection...")
    os.system(f"python3 error-based.py -u {target}")

    print(Fore.YELLOW + "[*] Running Time-Based SQL Injection...")
    os.system(f"python3 time-based.py -u {target}")

    print(Fore.GREEN + "[+] All tests completed successfully!")
    input(Fore.CYAN + "[*] Press Enter to return to the menu...")

def error_based_sqli():
    clear()
    print(Fore.YELLOW + "[*] Running Error-Based SQL Injection scan...\n")
    os.system("python3 error-based.py")
    input(Fore.CYAN + "[*] Press Enter to return to the menu...")

def blind_sqli():
    clear()
    print(Fore.YELLOW + "[*] Running Time-Based SQL Injection scan...\n")
    os.system("python3 time-based.py")
    input(Fore.CYAN + "[*] Press Enter to return to the menu...")

def menu():
    while True:
        clear()
        banner()
        print(Fore.CYAN + "╔═════════════════════════════════════════════════════╗")
        print(Fore.CYAN + "| " + Fore.YELLOW + "[1] All In One" + Fore.CYAN + "                                      |")
        print(Fore.CYAN + "| " + Fore.YELLOW + "[2] Error-Based SQLi" + Fore.CYAN + "                                |")
        print(Fore.CYAN + "| " + Fore.YELLOW + "[3] Time-Based SQLi" + Fore.CYAN + "                                 |")
        print(Fore.CYAN + "| " + Fore.YELLOW + "[4] Credits" + Fore.CYAN + "                                         |")
        print(Fore.CYAN + "| " + Fore.RED + "[0] Exit" + Fore.CYAN + "                                            |")
        print(Fore.CYAN + "╚═════════════════════════════════════════════════════╝")

        choice = input(Fore.CYAN + "\n[?] Enter your choice: ").strip()

        if choice == "1":
            all_in_one()
        elif choice == "2":
            error_based_sqli()
        elif choice == "3":
            blind_sqli()
        elif choice == "4":
            credits()
        elif choice == "0":
            print(Fore.GREEN + "[+] Exiting. Thank you!")
            break
        else:
            print(Fore.RED + "[!] Invalid choice. Please try again.")
            input(Fore.CYAN + "[*] Press Enter to return to menu...")


if __name__ == "__main__":
    animation()
    menu()
