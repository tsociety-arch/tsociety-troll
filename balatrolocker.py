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


#now i will prevent them from renaming balatro using watchdog



try: #ensures pip is installed
    import pip
except ImportError:
    ensurepip.bootstrap() #adds pip to current python

 
 
warning_closed = False 

def show_warning():
    global kill_count,warning_closed
    
    
    messagebox.showwarning("system", "balatro is currently not available sir")
    warning_closed = True


subprocess.call([sys.executable, "-m", "pip", "install", "watchdog"])

subprocess.call([sys.executable, "-m", "pip", "install", "pywin32"])

from watchdog.observers import Observer         # Watches for changes in the file system
from watchdog.events import FileSystemEventHandler  # Lets us define what to do when something happens

#configuration part

userhome = Path().home()
download_path = userhome / 'Downloads'
balatro_path = userhome / 'Downloads' / 'baltro' / 'Balatro.v1.0.1o' / 'Balatro.v1.0.1o' / 'balatro.exe'
balatro_dir = balatro_path.parent
balatro_name = "balatro.exe"


def make_directory_read_only(path: Path):
    for file in path.rglob("*"):
        if file.is_file():
            try:
                os.chmod(file, 0o444)  # read-only for all
            except Exception as e:
                print(f"Failed to set read-only: {file} - {e}")

make_directory_read_only(balatro_dir)
subprocess.call(["icacls", str(balatro_dir), "/deny", f"{os.getlogin()}:W"])


#step one : lets make the file read only


def make_read_only(path: Path):
    if path.exists():
        os.chmod(path, 0o444) #we changed its property. # 0o444 = read-only for everyone
    else:
        messagebox.showinfo("system", "balatro is not in its normal path")    
        
        
def warn_user(message): #warns user with the desired message
    ctypes.windll.user32.MessageBoxW(0, message, "System Warning", 0x10)  # 0x10 = MB_ICONHAND (red X)

#define the event handler

class BalatroWatcher(FileSystemEventHandler): #this is the windows module that handles events, we'll use it
    
    """
    This class inherits from FileSystemEventHandler and defines how we react when files change.
    `on_moved` and `on_deleted` are special methods that get called automatically when a file moves or is deleted.
    """
    
    def on_moved(self, event):
        self.check_for_rename()

    def on_deleted(self, event):
        self.check_for_rename()

    def check_for_rename(self):
        """
        This method checks if Balatro.exe is missing. If so, it searches the folder
        for a suspicious renamed .exe and tries to fix it.
        """
        if not balatro_path.exists():
            print("[!] Balatro.exe is missing!")
           

            # Scan the folder for other suspicious .exe files
            for file in balatro_dir.glob("*.exe"):
                if file.name != balatro_name:
                    try:
                        print(f"[!] Found renamed version: {file.name}")
                        file.rename(balatro_path)
                        make_read_only(balatro_path) #used the func we defined
                        def threaded_warning():
                            warn_user("Sir, PLEASE don't rename the file. It's forbidden.")
                            warn_user(f"{file.name} has been renamed back to Balatro.exe. Please don't touch it again.")
                            messagebox.askyesno("system", "Are you sure you want to proceed with this behavior?")

                        threading.Thread(target=threaded_warning).start()
    
                        break
                    except Exception as e:
                        print(f"[!] Failed to rename: {e}")
                        warn_user("Failed to fix the rename. You'll be edged.")
                        break
                for file in balatro_dir.rglob("*"):
                    if file.is_file() and not file.name.startswith("balatro") and ".exe" in file.suffix:
                        warn_user(f"Suspicious file found: {file.name}. Do not rename Balatro files.")
            


# === 4. START WATCHING ===
def start_monitoring():
    """
    This sets up the folder monitoring using watchdog.
    We create an Observer, attach our custom handler to it, and start watching.
    """
    observer = Observer()
    handler = BalatroWatcher()  # Instance of our custom class
    observer.schedule(handler, path=str(balatro_dir), recursive=True)
    observer.start()
    print("[+] Started watching Balatro folder...")

    try:
        while True:
            time.sleep(1)  # Keeps the script alive
    except KeyboardInterrupt:
        observer.stop()   # Let user stop with Ctrl+C

    observer.join()       # Wait for the observer to finish
    




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
                         warning_closed = False  # reset after some time
                  
                     
                                         
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
         
           
if __name__ == "__main__":
    print("[+] Welcome to the balatro terminator.")
    print("checking and killing balatro...")

    # Start the BalatroWatcher in a separate thread
    monitor_thread = threading.Thread(target=start_monitoring, daemon=True)
    monitor_thread.start()



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
