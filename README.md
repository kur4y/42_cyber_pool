# 42 Cybersecurity Piscine

An intensive curriculum focused on understanding offensive security, network vulnerabilities, and secure infrastructure. This repository contains the core projects developed during the piscine, showcasing a transition from theoretical vulnerabilities to automated detection and containerized network simulations.

## 🛠️ Technical Stack
* **Languages:** Python, C, Bash
* **Infrastructure & Automation:** Docker, Docker Compose, Nginx, Tor
* **Networking & Protocols:** TCP/IP, ARP, HTTP/HTTPS, FTP, Scapy
* **Security Concepts:** Cryptography (AES, HOTP), SQL Injection, ARP Poisoning, Reverse Engineering

---

## 🏗️ Infrastructure & Network Security

### [Inquisitor](./inquisitor)
A containerized network laboratory demonstrating Man-in-the-Middle (MitM) attacks.
* **Core Concepts:** Full-duplex ARP Spoofing, Packet Sniffing, PCAP.
* **Stack:** Python (Scapy), Docker, Docker Compose.
* **Highlights:** Automatically builds an isolated virtual network with an attacker node, an FTP server, and a client to intercept credentials in real-time.

### [ft_onion](./ft_onion)
Deployment of a secure Tor Hidden Service.
* **Core Concepts:** Network isolation, Proxying, SSH tunneling.
* **Stack:** Docker, Nginx, Tor, Debian.
* **Highlights:** A strictly configured Docker container serving a static website exclusively over the Tor network while routing SSH traffic securely, without exposing any local ports.

---

## 🕸️ Web Security & Automation

### [Vaccine](./vaccine)
An automated SQL injection vulnerability scanner and data extractor.
* **Core Concepts:** Error-based & Union-based SQLi, Data Dumping, HTTP manipulation.
* **Stack:** Python (Requests, BeautifulSoup), Flask (for the test target).
* **Highlights:** Dynamically adapts payloads to extract SQLite database structures and data, packaged with a vulnerable Flask application for local testing.

### [Arachnida](./arachnida)
A recursive web scraper and metadata analyzer.
* **Core Concepts:** DOM Parsing, EXIF data extraction, recursive algorithms.
* **Stack:** Python (BeautifulSoup, ExifRead).
* **Highlights:** Built entirely without automated frameworks (no Scrapy), strictly managing HTTP protocols, URL sanitization, and binary file handling.

---

## 🛡️ Defensive Security & Monitoring (Blue Team)

### [Iron Dome](./iron_dome)
A file system monitoring tool designed to detect ransomware activity in real-time.
* **Core Concepts:** Daemonization, System integrity monitoring, Shannon Entropy calculation, Anomaly detection.
* **Stack:** Python.
* **Highlights:** Acts as a countermeasure to malware like *Stockholm*. It continuously monitors critical directories and calculates the entropy of modified files to detect cryptographic transformations (encryption) typical of ransomware attacks.

---

## 🔐 Cryptography & Systems

### [ft_otp](./ft_otp)
Implementation of a Time-based One-Time Password (TOTP) generator based on RFC 4226.
* **Core Concepts:** HOTP algorithm, HMAC-SHA1, Bitwise operations, Hexadecimal encryption.
* **Stack:** Python (Native libraries only).
* **Highlights:** Manually computes cryptographic hashes and dynamic truncation without relying on external OTP libraries. 

### [Stockholm](./stockholm)
An educational ransomware simulator mimicking the behavior of WannaCry.
* **Core Concepts:** Symmetric encryption, File system traversal, Malware signatures.
* **Stack:** Python (Cryptography/Fernet).
* **Highlights:** Recursively targets specific file extensions for encryption and decryption within a sandboxed environment.

### [Reverse Me](./reverse_me)
Introduction to Reverse Engineering and binary analysis.
* **Core Concepts:** Assembly (x86), Stack inspection, Memory management.
* **Stack:** C, GDB.
* **Highlights:** Algorithmic reconstruction of compiled binaries to understand hardcoded logic and bypass authentication mechanisms.

---
*Disclaimer: All projects in this repository were developed in a strictly controlled academic environment for educational purposes.*
