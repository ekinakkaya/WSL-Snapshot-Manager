# WSL Snapshot Manager

import subprocess
import os
import json
import datetime
import time
import threading
import shutil
import gzip
import re

from termcolor import colored

CONFIG_FILE = os.path.expanduser("~/.wsl_snapshot_config.json")

DEFAULT_CONFIG = {
    "backup_dir": os.path.expanduser("~/wsl_backups")
}

spinner_running = False

def spinner():
    global spinner_running
    while spinner_running:
        for cursor in '|/-\\':
            print(cursor, end='\r', flush=True)
            time.sleep(0.1)

def start_spinner():
    global spinner_running
    spinner_running = True
    threading.Thread(target=spinner, daemon=True).start()

def stop_spinner():
    global spinner_running
    spinner_running = False
    print(' ', end='\r', flush=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)


def list_distros():
    result = subprocess.run(["wsl", "--list", "--verbose"], capture_output=True)
    output = result.stdout.decode('utf-16').strip()
    lines = output.splitlines()

    distros = []
    
    for line in lines[1:]:
        match = re.match(r'([* ]?)\s*([^\s]+)\s+([^\s]+)\s+(\d+)', line.strip())
        if match:
            is_default = match.group(1) == '*'
            name = match.group(2)
            state = match.group(3)
            version = int(match.group(4))
            
            distros.append([
                name,
                state,
                version,
                is_default
            ])

    return distros




def list_backups(backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.tar.gz')]
    return backups

def export_distro():
    config = load_config()
    backup_dir = config['backup_dir']

    distros = list_distros()
    if not distros:
        print(colored("No distros available to export.", "red"))
        return

    print("\nAvailable distros to export:")
    for idx, (distro, state, version, is_default) in enumerate(distros, 1):
        distro_colored = colored(f"{distro:20}", "yellow")
        state_colored = colored(f"{state:15}", "magenta")
        version_colored = colored(f"(WSL {version:5})", "blue")
        label = f"{distro_colored}{state_colored}{version_colored}"
        if is_default:
            label += colored(" [default]", "green")
        print(f"{colored(str(idx) + '.', 'cyan')} {label}")

    choice = int(input("Select a distro to export: ")) - 1
    selected_distro, state, version, is_default = distros[choice]

    # TODO: if the distro is not stopped, prompt the user to close it first.

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    backup_file = os.path.join(backup_dir, f"{selected_distro}-{timestamp}.tar")
    compressed_backup_file = backup_file + ".gz"

    print(colored(f"Exporting {selected_distro} to {compressed_backup_file}...", "cyan"))
    start_spinner()
    subprocess.run(["wsl", "--export", selected_distro, backup_file])
    stop_spinner()

    print(colored("Compressing backup...", "cyan"))
    with open(backup_file, 'rb') as f_in, gzip.open(compressed_backup_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(backup_file)

    print(colored("Export and compression complete! ✅", "green"))


def import_distro():
    config = load_config()
    backup_dir = config['backup_dir']

    backups = list_backups(backup_dir)
    if not backups:
        print(colored("No backups available to import.", "red"))
        return

    print("Available backups to import:")
    for idx, backup in enumerate(backups, 1):
        print(f"{idx}. {backup}")

    choice = int(input("Select a backup to import: ")) - 1
    selected_backup = backups[choice]

    new_distro_name = input("Enter a name for the new distro: ")
    default_install_location = os.path.expanduser(f"~/wsl_installs/{new_distro_name}")
    install_location = input(f"Enter the install location (default: {default_install_location}): ") or default_install_location

    compressed_backup_path = os.path.join(backup_dir, selected_backup)
    extracted_backup_path = compressed_backup_path[:-3]  # remove .gz

    print(colored("Decompressing backup...", "cyan"))
    start_spinner()
    with gzip.open(compressed_backup_path, 'rb') as f_in, open(extracted_backup_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    stop_spinner()

    print(colored(f"Importing {new_distro_name} from {extracted_backup_path} into {install_location}...", "cyan"))
    start_spinner()
    subprocess.run(["wsl", "--import", new_distro_name, install_location, extracted_backup_path])
    stop_spinner()

    os.remove(extracted_backup_path)

    print(colored("Import complete! ✅", "green"))

def set_backup_dir():
    new_dir = input("Enter new backup directory path: ")
    config = load_config()
    config['backup_dir'] = os.path.expanduser(new_dir)
    save_config(config)
    print(colored(f"Backup directory set to {new_dir}", "green"))

def main_menu():
    config = load_config()

    while True:
        print(colored("\nWSL Snapshot Manager", "yellow"))
        print("---\nThe default export(backup) directory is " + colored(config['backup_dir'], "green") + "\n---\n");
        print("1. Export a WSL distro")
        print("2. Import a WSL distro")
        print("3. Set backup directory")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            export_distro()
        elif choice == '2':
            import_distro()
        elif choice == '3':
            set_backup_dir()
        elif choice == '4':
            print(colored("Goodbye! 👋", "yellow"))
            break
        else:
            print(colored("Invalid choice. Please select again.", "red"))

if __name__ == "__main__":
    main_menu()
