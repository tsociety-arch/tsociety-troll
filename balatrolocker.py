#we need the psutil module in order this works, so go use pip install psutil
#with the pi ducky payload, go ahead and do that
import os
import subprocess
import time
import sys
import ensurepip
import pathlib
from pathlib import Path
import ctypes #used to get admin rights along with the sys module, used for windows stuff
import tkinter as tk #some GUI stuff
from tkinter import messagebox
from tkinter import simpledialog #we will ask for a password if the tries are exceeded
import getpass #will allow us to ask for a password
import threading #this will help us continue the killer in the background while password dialog is open, basically it lets us run multiple things at once



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Relaunch script with admin rights and visible terminal
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, params, None, 0
    )
    sys.exit()
#this is a little hard to understand but it checks if this script is run as administrator
#and runs it as an administrator if its not










 
 
warning_closed = False 

def show_warning():
    global kill_count,warning_closed
    
    
    messagebox.showwarning("system", "balatro is currently not available sir")
    warning_closed = True








try: #ensures pip is installed
    import pip
except ImportError:
    ensurepip.bootstrap() #adds pip to current python




subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

#

possible_target_processes = ["Balatro.exe",  "balatro.exe"]


subprocess.call([sys.executable, "-m", "pip", "install", "psutil"])


script_path = Path(__file__).resolve()
task_name_base = "BalatroTerminator"



# Paths
script_path = Path(__file__).resolve()
task_name_base = "BalatroTerminator"

# First-run marker file (saved next to the script)
marker_file = script_path.with_name(".balatro_scheduled")

# Only run scheduling once
if not marker_file.exists():
    print("[+] First run detected. Scheduling tasks...")

    run_times = ["08:41", "09:30", "10:21", "11:11", "12:11", "13:41", "14:31"]

    for i, run_time in enumerate(run_times):
        task_name = f"{task_name_base}_Time_{i}"
        subprocess.run([
            "schtasks", "/Create", "/F",
            "/SC", "DAILY",
            "/TN", task_name,
            "/TR", f'"{Path(sys.executable)}" "{script_path}"',
            "/ST", run_time
        ])

    # Logon trigger
    task_name_logon = f"{task_name_base}_Logon"
    subprocess.run([
        "schtasks", "/Create", "/F",
        "/SC", "ONLOGON",
        "/TN", task_name_logon,
        "/TR", f'"{Path(sys.executable)}" "{script_path}"'
    ])

    # Create the marker file
    marker_file.write_text("scheduled")

    print("[+] Tasks scheduled. This will not run again.")
    messagebox.showinfo("system", "balatro is FUCKED")
else:
    print("[=] Tasks already scheduled. Skipping setup.")
    




import psutil

kill_count = 0

def kill_balatro():
    global kill_count, warning_closed
    for proc in psutil.process_iter(['name']):
        for exe in possible_target_processes:
             if proc.info['name'] == exe:
                 try:
                     proc.kill()
                     print(f"balatro terminated.")
                     print(f"this was the {kill_count}'th time sir.")
                     kill_count += 1
                    
                     warning_thread = threading.Thread(target=show_warning)   
                     warning_thread.start()
                
                     while not warning_closed:
                         proc.kill()
                         time.sleep(2)                     
                     
                                         
                 except Exception as e:
                     pass
        
try:
    kill_balatro()
    print("[+]running balatro terminator")
except Exception as j:
    print("the script is not working properly")    

password = "duhantosun123"
unlocked = False           
           
           
 #now lets ask for a password using the tkinter module.

#the show argument           
           
terminate = True
kill_count = 0
         
           
if __name__ == "__main__":  # checks if the script is being run directly
    print("[+] Welcome to the balatro terminator.")
    print("checking and killing balatro...")



    #  Define this function to run password dialog in a separate thread
    def ask_password():
        global terminate, unlocked ,kill_count#the global here means These variables exist outside the function, in the global script scope — I want to modify them.
        while not unlocked:
            entered_password = simpledialog.askstring("sir balatro is locked sir", "sir please enter the password to keep playing balatro sir", show="*")
            if entered_password == password:
                messagebox.showinfo("system", "sir thank you sir!")
                terminate = False
                kill_count = 0
                unlocked = True
                
            else:
                messagebox.showwarning("system", "sir i am sorry sir you can't play this game sir")
                time.sleep(1)
                kill_count = 0

    while terminate and not unlocked:
        if kill_count >= 3:
            print("too many attempts detected. Locking Balatro's ass.")
            kill_balatro()

            #  Start the password dialog in a new thread
            password_thread = threading.Thread(target=ask_password)
            password_thread.start()

            #  Wait here while the password thread handles input
            while not unlocked:
                kill_balatro()
                time.sleep(1)

        else:
            
            kill_balatro()
            time.sleep(1)

messagebox.showinfo("system", "if you are seeing this message, balatro is unlocked.")
    
    

# psutil.process_iter() returns an iterator over all running processes.
# 'name' saves us time by only returning the name of the process
