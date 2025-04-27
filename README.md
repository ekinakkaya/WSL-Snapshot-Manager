# DISCLAIMER

This tool has not been tested properly and I am sure that it raises a lot of errors. So, if you encounter any bugs or errors, please feel free to open an issue, or fork and fix it yourself if you feel adventurous. Thanks for your feedback!

# 🐧 WSL Snapshot Manager

**WSL Snapshot Manager** is a simple, interactive CLI tool to **backup** and **restore** your WSL (Windows Subsystem for Linux) distros easily.

It supports:

- 📦 Exporting WSL distros into compressed `.tar.gz` snapshots
- 🛠 Importing snapshots back into WSL
- 📂 Default, customizable backup directory
- 🎨 Colored output for better UX
- 🔄 Progress spinner during operations
- ⚡ Auto-detects WSL1 or WSL2 versions

---

## 🚀 Features

- Simple interactive menu
- Automatic `.tar.gz` compression to save space
- Configuration for default backup folder
- Supports both WSL1 and WSL2 distros

---

## 🛠 Requirements

- **Python 3.7+**
- **Windows 10/11** with WSL installed
- Python packages listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/ekinakkaya/wsl-snapshot-manager.git
cd wsl-snapshot-manager
```

Install dependencies & run the tool

```bash
pip install -r requirements.txt
python wsl_snapshot.py
```

---

## 📋 Usage

You will see an interactive menu:

```
WSL Snapshot Manager
1. Export a WSL distro
2. Import a WSL distro
3. Set backup directory
4. Exit
```

- **Export a Distro**: Select an installed WSL distro to create a compressed backup.
- **Import a Distro**: Select a saved backup to restore it.
- **Set Backup Directory**: Change where your backups are saved.

---

## 📁 Default Locations

- **Backup storage**:  
  `~/wsl_backups/` _(can be changed in settings)_

- **Imported distros**:  
  Default install location: `~/wsl_installs/<distro_name>/`

---

## 🧹 Extra Notes

- Backups are compressed into `.tar.gz` automatically.
- Temporary files are cleaned up after importing.
- Compatible with both WSL1 and WSL2 distros.

---

## 🛡️ License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and contribute!
