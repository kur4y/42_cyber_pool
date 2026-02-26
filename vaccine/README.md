# Vaccine

## Description
Vaccine is an automated SQL injection vulnerability scanner. It detects error-based SQL injections and automatically dumps the SQLite database structure and data using dynamically injected UNION-based payloads. It supports both GET and POST HTTP methods.

## Prerequisites
Ensure Python 3 is installed. Install the required dependencies from requirements.txt

## Usage
python vaccine.py [-h] [-o OUTPUT] [-X {GET,POST}] url
