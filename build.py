from datetime import datetime
import json
import requests

repos = list()

def main():
    token = get_token()
    print(token)

def get_token():
    with open('github_token.txt', 'r') as f:
        return f.read().strip()

if __name__ == '__main__':
    main()