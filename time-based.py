import os
import requests
import time
import argparse
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")


def banner():
    print(Fore.MAGENTA + "╔═══════════════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + r"""
████████╗██╗███╗   ███╗███████╗    ██████╗  █████╗ ███████╗███████╗██████╗
╚══██╔══╝██║████╗ ████║██╔════╝    ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
   ██║   ██║██╔████╔██║█████╗      ██████╔╝███████║███████╗█████╗  ██║  ██║
   ██║   ██║██║╚██╔╝██║██╔══╝      ██╔══██╗██╔══██║╚════██║██╔══╝  ██║  ██║
   ██║   ██║██║ ╚═╝ ██║███████╗    ██████╔╝██║  ██║███████║███████╗██████╔╝
   ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝
""")
    print(Fore.MAGENTA + "╚═══════════════════════════════════════════════════════════════════════════╝")


def detect_sqli(target_url, payload_file, output_file):
    print(Fore.BLUE +"[+] Starting SQLi detection on:"+Fore.GREEN+f" {target_url}")
    vulnerable_urls = []
    timeout_threshold = 10

    try:
        with open(payload_file, "r") as file:
            payloads = [line.strip() for line in file.readlines()]
        if not payloads:
            print(Fore.RED + "[!] No payloads found in the file. Exiting.")
            return

        print(Fore.BLUE + "[+] Loaded"+Fore.GREEN+f" {len(payloads)}"+Fore.BLUE+" payloads for testing.\n")

        for i, payload in enumerate(payloads, 1):
            print(Fore.YELLOW + f"[*] Testing payload {i}/{len(payloads)}: {payload}")

            injection_url = target_url.replace("*", payload)
            start_time = time.time()

            try:
                response = requests.get(injection_url, timeout=timeout_threshold + 2)
            except requests.exceptions.Timeout:
                print(Fore.GREEN + f"[!!!] Timeout detected with payload: {payload}")
                vulnerable_urls.append(f"{target_url} | Payload: {payload}")
                continue
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"[!] Error during request: {e}")
                continue

            elapsed_time = time.time() - start_time

            if elapsed_time > timeout_threshold:
                print(Fore.GREEN + f"[!!!] Potential vulnerability detected with payload: {payload}")
                vulnerable_urls.append(f"{target_url} | Payload: {payload}")
            else:
                print(Fore.RED + f"[-] No vulnerability detected for payload: {payload}")

        if vulnerable_urls:
            with open(output_file, "w") as file:
                file.write("\n".join(vulnerable_urls))
            print(Fore.GREEN + f"\n[+] Vulnerable URLs saved to '{output_file}'.")
        else:
            print(Fore.YELLOW + "\n[!] No vulnerabilities detected.")

    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting ...")
        exit()
    except FileNotFoundError:
        print(Fore.RED + f"[!] Error: Payload file '{payload_file}' not found.")
    except Exception as e:
        print(Fore.RED + f"[!] An unexpected error occurred: {e}")


def handle_multiple_urls(urls_file, payload_file, output_file):
    try:
        with open(urls_file, "r") as file:
            urls = [line.strip() for line in file.readlines()]
        if not urls:
            print(Fore.RED + "[!] No URLs found in the file. Exiting.")
            return

        vulnerable_urls = []
        for url in urls:
            if "*" not in url:
                print(Fore.RED + f"[!] Skipping invalid URL (missing '*'): {url}")
                continue

            print(Fore.BLUE + f"\n[+] Testing URL: {url}")
            results = detect_sqli(url, payload_file, output_file)
            vulnerable_urls.extend(results or [])

        if vulnerable_urls:
            with open(output_file, "w") as file:
                file.write("\n".join(vulnerable_urls))
            print(Fore.GREEN + f"\n[+] Vulnerable URLs saved to '{output_file}'.")
        else:
            print(Fore.YELLOW + "\n[!] No vulnerabilities detected across all URLs.")

    except FileNotFoundError:
        print(Fore.RED + f"[!] Error: URLs file '{urls_file}' not found.")
    except Exception as e:
        print(Fore.RED + f"[!] An unexpected error occurred: {e}")


def interactive_mode():
    while True:
        clear()
        banner()
        print(Fore.CYAN + "\n╔═══════════════════════════════════════════════════╗")
        print(Fore.CYAN + "| " + Fore.GREEN + "[1] Start SQLi Scan (Single URL)" + Fore.CYAN + "                  |")
        print(Fore.CYAN + "| " + Fore.GREEN + "[2] Start SQLi Scan (URLs File)" + Fore.CYAN + "                   |")
        print(Fore.CYAN + "| " + Fore.RED + "[0] Exit" + Fore.CYAN + "                                          |")
        print(Fore.CYAN + "╚═══════════════════════════════════════════════════╝")

        choice = input(Fore.CYAN + "\n[?] Enter your choice: ").strip()

        if choice == "1":
            clear()
            banner()
            print(Fore.MAGENTA + "[!] Ensure the URL includes '*' where payloads will be tested.")
            target = input(Fore.CYAN + "\nEnter the target URL: ").strip()
            payload_file = "payloads/time_based.txt"
            output_file = "vulnerable_results.txt"

            detect_sqli(target, payload_file, output_file)
            input(Fore.CYAN + "\n[*] Press Enter to return to the main menu...")

        elif choice == "2":
            clear()
            banner()
            print(Fore.MAGENTA + "[!] Provide the path to the file containing URLs.")
            urls_file = input(Fore.CYAN + "\nEnter the path to the URLs file: ").strip()
            payload_file = "payloads/time_based.txt"
            output_file = "vulnerable_results.txt"

            handle_multiple_urls(urls_file, payload_file, output_file)
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
    parser.add_argument("-f", "--file", help="File containing URLs for injection")
    parser.add_argument("-p", "--payloads", help="File containing payloads", default="payloads/time_based.txt")
    parser.add_argument("-o", "--output", help="File to save results", default="vulnerable_results.txt")

    args = parser.parse_args()

    if args.url:
        clear()
        banner()
        print(f"{Fore.GREEN}[+] Running in command-line mode...")
        if "*" not in args.url:
            print(f"{Fore.RED}[!] Invalid URL format. Ensure the URL contains '*' for injection.")
            return

        detect_sqli(args.url, args.payloads, args.output)

    elif args.file:
        clear()
        banner()
        print(f"{Fore.GREEN}[+] Running in command-line mode with URLs file...")
        handle_multiple_urls(args.file, args.payloads, args.output)

    else:
        interactive_mode()


if __name__ == "__main__":
    main()
