import os
import requests
import argparse
from colorama import Fore, init

init(autoreset=True)


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def banner():
    print(Fore.MAGENTA + "╔═══════════════════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + r"""

███████╗██████╗ ██████╗  ██████╗ ██████╗ ██████╗  █████╗ ███████╗███████╗██████╗
██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
█████╗  ██████╔╝██████╔╝██║   ██║██████╔╝██████╔╝███████║███████╗█████╗  ██║  ██║
██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔══██║╚════██║██╔══╝  ██║  ██║
███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║██████╔╝██║  ██║███████║███████╗██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝

""")
    print(Fore.MAGENTA + "╚═══════════════════════════════════════════════════════════════════════════════╝")


def detect_database_type(response_text):
    db_errors = {
        "MySQL": "you have an error in your sql syntax",
        "MSSQL": "unclosed quotation mark",
        "Oracle": "ora-01756",
        "PostgreSQL": "syntax error at or near",
    }
    for db, error in db_errors.items():
        if error.lower() in response_text.lower():
            return db
    return None


def load_payloads(file_path):
    try:
        with open(file_path, "r") as file:
            payloads = [line.strip() for line in file.readlines() if line.strip()]
        return payloads
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Payload file not found: {file_path}")
        return []


def inject_payload(url, payload):
    if "?" in url and "=" in url:
        base, params = url.split("?", 1)
        param_pairs = params.split("&")
        injected_params = [
            f"{key}={payload}" if i == 0 else f"{key}={value}"
            for i, pair in enumerate(param_pairs)
            for key, value in [pair.split("=", 1)]
        ]
        return f"{base}?{'&'.join(injected_params)}"
    return None


def sqli_scanner(url, payloads, output_file):
    results = []
    for payload in payloads:
        injected_url = inject_payload(url, payload)
        if not injected_url:
            print(f"{Fore.RED}[!] Could not construct an injected URL for payload: {payload}")
            continue

        print(f"{Fore.CYAN}[*] Testing payload: {Fore.YELLOW}{payload}")
        try:
            response = requests.get(injected_url, timeout=5)
            db_type = detect_database_type(response.text)
            if db_type:
                print(f"{Fore.GREEN}[!] Vulnerable! Database Type: {Fore.YELLOW}{db_type}")
                print(f"    {Fore.GREEN}Payload: {Fore.YELLOW}{payload}")
                print(f"    {Fore.GREEN}URL: {Fore.YELLOW}{injected_url}")
                results.append({"payload": payload, "db_type": db_type, "url": injected_url})
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Request failed for payload {payload}: {e}")

    if results:
        with open(output_file, "w") as file:
            for result in results:
                file.write(f"Payload: {result['payload']} | DB: {result['db_type']} | URL: {result['url']}\n")
        print(f"{Fore.GREEN}\n[+] Results saved to '{output_file}'.")
    else:
        print(f"{Fore.YELLOW}[!] No vulnerabilities found with the tested payloads.")

    return results


def interactive_mode():
    while True:
        clear()
        banner()
        print(Fore.CYAN + "\n╔═════════════════════════════════════════════════════╗")
        print(Fore.CYAN + "| " + Fore.GREEN + "[1] Start Error-Based SQL Injection Scan" + Fore.CYAN + "            |")
        print(Fore.CYAN + "| " + Fore.RED + "[0] Exit" + Fore.CYAN + "                                            |")
        print(Fore.CYAN + "╚═════════════════════════════════════════════════════╝")

        choice = input(Fore.CYAN + "\n[?] Enter your choice: ").strip()

        if choice == "1":
            clear()
            banner()
            url = input(f"{Fore.YELLOW}[?] Enter the target URL (with a parameter, e.g., http://example.com/page.php?id=): ").strip()
            if "?" not in url:
                print(f"{Fore.RED}[!] Invalid URL format. Make sure to include a parameter.")
                input(Fore.CYAN + "[*] Press Enter to return to the main menu...")
                continue

            payload_file = "payloads/error_based.txt"
            output_file = "error_based_results.txt"

            print(f"{Fore.GREEN}[+] Starting SQLi scan on: {Fore.CYAN}{url}")
            payloads = load_payloads(payload_file)
            if not payloads:
                print(f"{Fore.RED}[!] No payloads loaded. Ensure {payload_file} exists and is not empty.")
                input(Fore.CYAN + "[*] Press Enter to return to the main menu...")
                continue

            results = sqli_scanner(url, payloads, output_file)

            input(Fore.CYAN + "[*] Press Enter to return to the main menu...")

        elif choice == "0":
            print(Fore.GREEN + "[+] Exiting. Thank you!")
            break

        else:
            print(Fore.RED + "[!] Invalid choice. Please try again.")
            input(Fore.CYAN + "[*] Press Enter to return to the main menu...")


def main():
    parser = argparse.ArgumentParser(description="Error-Based SQL Injection Scanner")
    parser.add_argument("-u", "--url", help="Target URL with a parameter")
    parser.add_argument("-p", "--payloads", help="File containing payloads", default="payloads/error_based.txt")
    parser.add_argument("-o", "--output", help="File to save results", default="error_based_results.txt")

    args = parser.parse_args()

    if args.url:
        clear()
        banner()
        print(f"{Fore.GREEN}[+] Running in command-line mode...")
        payloads = load_payloads(args.payloads)
        if not payloads:
            print(f"{Fore.RED}[!] No payloads loaded. Ensure {args.payloads} exists and is not empty.")
            return
        sqli_scanner(args.url, payloads, args.output)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
