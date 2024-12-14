import os
import requests
import time
import argparse
from colorama import Fore, init

init(autoreset=True)


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def banner():
    print(Fore.MAGENTA + "╔══════════════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + r"""
████████╗██╗███╗   ███╗███████╗    ██████╗  █████╗ ███████╗███████╗██████╗
╚══██╔══╝██║████╗ ████║██╔════╝    ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
   ██║   ██║██╔████╔██║█████╗      ██████╔╝███████║███████╗█████╗  ██║  ██║
   ██║   ██║██║╚██╔╝██║██╔══╝      ██╔══██╗██╔══██║╚════██║██╔══╝  ██║  ██║
   ██║   ██║██║ ╚═╝ ██║███████╗    ██████╔╝██║  ██║███████║███████╗██████╔╝
   ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝
""")
    print(Fore.MAGENTA + "╚══════════════════════════════════════════════════════════════════════════╝")


def detect_sqli(target_url, payload_file, output_file):
    print(Fore.BLUE + f"[+] Starting SQLi detection on: {target_url}")
    results = []
    timeout_threshold = 10

    try:
        with open(payload_file, "r") as file:
            payloads = [line.strip() for line in file.readlines()]
        if not payloads:
            print(Fore.RED + "[!] No payloads found in the file. Exiting.")
            return

        print(Fore.BLUE + f"[+] Loaded {len(payloads)} payloads for testing.\n")

        for i, payload in enumerate(payloads, 1):
            print(Fore.YELLOW + f"[*] Testing payload {i}/{len(payloads)}: {payload}")

            injection_url = target_url.replace("*", payload)
            start_time = time.time()

            try:
                response = requests.get(injection_url, timeout=timeout_threshold + 2)
            except requests.exceptions.Timeout:
                print(Fore.RED + f"[!!!] Timeout detected for payload: {payload}")
                print(Fore.GREEN + f"      [!] This is likely a vulnerability as it exceeds {timeout_threshold} seconds.")
                results.append(f"[!!!] Timeout detected with payload: {payload}")
                continue
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"[!] Error during request: {e}")
                results.append(f"[!] Error with payload: {payload}. Details: {e}")
                continue

            end_time = time.time()
            elapsed_time = end_time - start_time

            if elapsed_time > timeout_threshold:
                print(Fore.GREEN + f"[!!!] Potential SQLi vulnerability detected with payload: {payload}")
                print(Fore.GREEN + f"      Response time: {elapsed_time:.2f} seconds")
                results.append(f"[!!!] Vulnerable payload: {payload} | Response time: {elapsed_time:.2f} seconds")
            else:
                print(Fore.RED + f"[-] No vulnerability detected for payload: {payload}")
                results.append(f"[-] No vulnerability detected with payload: {payload}")

        if results:
            with open(output_file, "w") as file:
                file.write("\n".join(results))
            print(Fore.GREEN + f"\n[+] Results saved to '{output_file}'.")
        else:
            print(Fore.YELLOW + "\n[!] No results to save.")

    except FileNotFoundError:
        print(Fore.RED + f"[!] Error: Payload file '{payload_file}' not found.")
    except Exception as e:
        print(Fore.RED + f"[!] An unexpected error occurred: {e}")
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Exiting...")


def interactive_mode():
    while True:
        clear()
        banner()
        print(Fore.CYAN + "\n╔═════════════════════════════════════════════════════╗")
        print(Fore.CYAN + "| " + Fore.GREEN + "[1] Start Time-Based SQL Injection Scan" + Fore.CYAN + "             |")
        print(Fore.CYAN + "| " + Fore.RED + "[0] Exit" + Fore.CYAN + "                                            |")
        print(Fore.CYAN + "╚═════════════════════════════════════════════════════╝")

        choice = input(Fore.CYAN + "\n[?] Enter your choice: ").strip()

        if choice == "1":
            clear()
            banner()
            print(Fore.MAGENTA + "[!] Ensure the URL includes '*' where payloads will be tested")
            target = input(Fore.CYAN + "\nEnter the target URL: ").strip()
            payload_file = "payloads/time_based.txt"
            output_file = "time_based_results.txt"

            detect_sqli(target, payload_file, output_file)
            input(Fore.CYAN + "\n[*] Press Enter to return to the main menu...")

        elif choice == "0":
            print(Fore.GREEN + "[+] Exiting. Thank you!")
            break
        else:
            print(Fore.RED + "[!] Invalid choice. Please try again.")
            input(Fore.CYAN + "[*] Press Enter to return to the main menu...")


def main():
    parser = argparse.ArgumentParser(description="Time-Based SQL Injection Scanner")
    parser.add_argument("-u", "--url", help="Target URL with '*' for injection")
    parser.add_argument("-p", "--payloads", help="File containing payloads", default="payloads/time_based.txt")
    parser.add_argument("-o", "--output", help="File to save results", default="time_based_results.txt")

    args = parser.parse_args()

    if args.url:
        clear()
        banner()
        print(f"{Fore.GREEN}[+] Running in command-line mode...")
        if "*" not in args.url:
            print(f"{Fore.RED}[!] Invalid URL format. Ensure the URL contains '*' for injection.")
            return

        payloads_file = args.payloads
        output_file = args.output
        detect_sqli(args.url, payloads_file, output_file)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
