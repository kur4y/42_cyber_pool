# Stockholm

## Description:
This project is an educational ransomware simulator. It encrypts and decrypts specific file extensions in the `~/infection` directory using symmetric encryption (Fernet/AES). 

**⚠️ WARNING: This project is for educational purposes only. Never use this type of program for malicious purposes.**

## PrerequisitesL
* Python 3
* `cryptography` library

## To install the required dependencies:
pip install -r requirements.txt

## Setup:
To set up the executable, simply run:
make

## Compilation:
Usage:
- ./stockholm [-h] [-v] [-r REVERSE] [-s]

    -h, --help : Show the help message and exit.

    -v, --version : Show the version of the program.

    -r KEY, --reverse KEY : Decrypt the files using the provided key.

    -s, --silent : Enable silent mode (no output during encryption/decryption).
