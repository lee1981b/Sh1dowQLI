# Sh1dowQLI

A Python-based SQL Injection Scanner designed to detect SQL vulnerabilities in web applications. The tool supports **Error-Based SQL Injection** and **Blind SQL Injection** techniques.

---

## Features

- **Error-Based SQL Injection Scan**
- **Time-Based SQL Injection Scan**
- User-friendly interface

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

1. Clone this repository:

```bash
git clone https://github.com/HexShad0w/Sh1dowQLI.git

cd Sh1dowQLI
```

## Run the tool:

```bash
python3 sh1dowqli.py
```
OR

Use command-line arguments for faster, automated scans:

-u: Specify your target URL <br>
-p: Load your custom payload file <br>
-o: Save results to a file


```bash
python3 time-based.py -u target url -p payloads/time_based.txt -o output.txt
```

```bash
python3 error-based.py -u target url -p payloads/error_based.txt -o output.txt
```


