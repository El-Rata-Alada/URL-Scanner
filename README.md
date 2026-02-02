# The Eye 

**Deep URL Intelligence Scanner (CLI)**

**The Eye** is a lightweight, nmap-style command-line tool that extracts **maximum intelligence from a single URL**.
Designed for **cybersecurity students, SOC analysts, and blue/red team learners**.

Give it a URL → *The Eye sees everything*.

---

## ✨ Features

* URL structure analysis
* Domain WHOIS intelligence
* Domain age detection
* DNS & IP resolution
* SSL/TLS certificate inspection
* Suspicious keyword detection
* Clean CLI output (nmap-like feel)

> No browser needed. No GUI. Fast. Focused. Surgical.

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/the-eye.git
cd the-eye
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install the tool system-wide

```bash
chmod +x install.sh
sudo ./install.sh
```

---

## 🚀 Usage

```bash
theeye <url>
```

### Example

```bash
theeye https://login-example-secure.xyz/login
```

### Sample Output

```
[+] Domain   : login-example-secure.xyz
[+] IP       : 185.xxx.xxx.xxx
[+] Age      : 12 days
[!] Warning  : Suspicious keywords detected
```

---

## 🛠️ Requirements

* Python 3+
* Linux / macOS / Windows
* Internet connection for some options

---

## 📂 Project Structure(may change)

```
the-eye/
├── theeye
├── install.sh
├── requirements.txt
└── README.md
```

---

## 🎯 Use Cases

* Phishing analysis
* SOC alert triage
* Threat hunting (basic OSINT)
* Cybersecurity learning projects
* Resume / portfolio tool

---

## 🚧 Roadmap

* `-A` aggressive scan mode
* Redirect chain detection
* Phishing form analysis
* JSON / report output
* MITRE ATT&CK mapping
* Go-based compiled binary

---

## ⚠️ Disclaimer

This tool is intended for **educational and defensive security purposes only**.
Do not use it against systems you do not own or have permission to test.

---

## ⭐ Contribute

Pull requests, feature ideas, and improvements are welcome.
