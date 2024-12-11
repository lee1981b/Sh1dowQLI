import os                                                                                       import subprocess
from colorama import Fore, init
                                                                                                init(autoreset=True)

def clear():                                                                                        os.system("clear" if os.name == "posix" else "cls")

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

def error_based_sqli():
    clear()
    print(Fore.YELLOW + "[*] Running Error-Based SQL Injection scan...")
    subprocess.run(["python3", "error-based.py"])
    input(Fore.CYAN + "[*] Press Enter to return to the main menu...")

def blind_sqli():
    clear()
    print(Fore.YELLOW + "[*] Running Error-Based SQL Injection scan...")
    subprocess.run(["python3", "time-based.py"])
    input(Fore.CYAN + "[*] Press Enter to return to the main menu...")

def menu():
    while True:

        clear()
        banner()
        print(Fore.CYAN + "╔═════════════════════════════════════════════════════╗")
        print(Fore.CYAN + "| " + Fore.YELLOW + "[1] Error-Based SQLi" + Fore.CYAN + "                                |")
        print(Fore.CYAN + "| " + Fore.YELLOW + "[2] Time-Based SQLi" + Fore.CYAN + "                                 |")
        print(Fore.CYAN + "| " + Fore.YELLOW + "[3] Credits" + Fore.CYAN + "                                         |")
        print(Fore.CYAN + "| " + Fore.RED + "[0] Exit" + Fore.CYAN + "                                            |")
        print(Fore.CYAN + "╚═════════════════════════════════════════════════════╝")

        choice = input(Fore.CYAN + "\n[?] Enter your choice: ").strip()

        if choice == "1":
            error_based_sqli()
        elif choice == "2":
            blind_sqli()
        elif choice == "3":

            clear()
            print(Fore.YELLOW + "╔════════════════════════════════════════════════════════╗")
            print(Fore.GREEN + """
[+] Tool: SQL Injection Scanner
[+] Author: @hexsh1dow
[+] Support : @GirlsWhoCodeBot
[+] Features: Error-Based SQLi, Blind SQLi
[+] Version: 1.0
    """)
            print(Fore.YELLOW + "╚════════════════════════════════════════════════════════╝")
        elif choice == "0":
            print(Fore.GREEN + "[+] Exiting. Thank you!")
            break
        else:
            print(Fore.RED + "[!] Invalid choice. Please try again.")
            input(Fore.CYAN + "[*] Press Enter to return to menu...")

if __name__ == "__main__":
    menu()
