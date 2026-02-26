# Iron Dome

> **Note:** This project is currently a Proof of Concept (PoC) focusing on Shannon entropy calculation and monitoring logic to detect anomalous cryptographic activity.

## Description
Iron Dome is a background daemon designed to monitor specific directories for ransomware-like activity. It calculates the Shannon entropy of modified files in real-time to detect potential encryption processes (such as those executed by the `stockholm` malware).

## Prerequisites
* Python 3
* Required libraries listed in `requirements.txt` (`watchdog`, `python-daemon`, etc.)

## Installation
pip install -r requirements.txt

## Usage
The program must be executed as root to allow background daemonization and system-level monitoring.

sudo ./irondome [path1] [path2] ...

If no arguments are provided, the daemon defaults to monitoring /home and /var/www.
All alerts and system events are logged in /var/log/irondome/irondome.log.