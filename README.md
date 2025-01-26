# Sh1dowQLI

A Python-based SQL Injection Scanner designed to detect SQL vulnerabilities in web applications. The tool supports **Error-Based SQL Injection** and **Blind SQL Injection** techniques.

---

## Features
- **All-In-One SQLi Module**
- **Error-Based SQL Injection Scan**
- **Time-Based SQL Injection Scan**
- **Bash script to find potential SQLi parameters**
- **User-friendly interface**

---

## Requirements

Before using the tool, ensure you have the following:

```bash
1. Python 3.6+ installed.
2. Required Python libraries:
   - `colorama`
   - `requests`
```
To install dependencies, run:

```bash
pip install colorama requests
```

---

## Installation

Clone this repository:

```bash
git clone https://github.com/HexShad0w/Sh1dowQLI.git
cd Sh1dowQLI
chmod +x *
```

## Run the tool:

```bash
python3 sh1dowqli.py
```
OR

Use command-line arguments for faster, automated scans:

-u: Specify your target URL <br>
-f: File containing multiple URLs <br>
-p: Load your custom payload file <br>
-o: Save results to a file


```bash
python3 time-based.py -u target url -p payloads/time_based.txt -o output.txt
```

```bash
python3 error-based.py -u target url -p payloads/error_based.txt -o output.txt
```

## Search for Potential SQLi Parameters

To begin, run the script to search for potential SQL injection (SQLi) parameters in the provided URLs.

```bash
./sqli.sh
```

Once executed, you'll be prompted to enter the target URL or domain. The script will use Katana to perform a passive and active scan to identify potential SQLi parameters.

### Install Katana

To install Katana, follow these steps:

```bash
go install github.com/projectdiscovery/katana/cmd/katana@latest
```

Ensure you have Go installed on your system to run the installation command.

---

# Contribution

Contributions are welcome! To contribute:

1. Fork the repository.
2. Make your changes.
3. Submit a pull request.



Feel free to reach out to me on X (formerly Twitter): <a href="https://x.com/hexsh1dow">Click Here</a>
