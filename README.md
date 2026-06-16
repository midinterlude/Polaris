<div align="center">
<pre>
    ▄▄▄·      ▄▄▌   ▄▄▄· ▄▄▄  ▪  .▄▄ · 
   ▐█ ▄█▪     ██•  ▐█ ▀█ ▀▄ █·██ ▐█ ▀. 
    ██▀· ▄█▀▄ ██▪  ▄█▀▀█ ▐▀▀▄ ▐█·▄▀▀▀█▄
   ▐█▪·•▐█▌.▐▌▐█▌▐▌▐█ ▪▐▌▐█•█▌▐█▌▐█▄▪▐█
   .▀    ▀█▄▀▪.▀▀▀  ▀  ▀ .▀  ▀▀▀▀ ▀▀▀▀ 
               Information:              
     https://github.com/midinterlude/    
        Developed by: Midinterlude       
            Started 2026-04-14           
         Logs located in Workspace. 
</pre>

<p><strong>Identity Anonymization · Environment Sanitization · Automated Deployment</strong></p>

<p>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue?style=flat-square&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-yellow?style=flat-square" alt="License: MIT"></a>
  <a href="https://www.microsoft.com/windows"><img src="https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey?style=flat-square&logo=windows&logoColor=white" alt="Platform"></a>
  <img src="https://img.shields.io/badge/status-active-brightgreen?style=flat-square" alt="Status">
</p>

<p><em>Developed by <a href="https://github.com/midinterlude/">Midinterlude</a> · Started 2026-04-14</em></p>

</div>

---

## Why Polaris?

Most alt scripts do one thing. Polaris does everything — in the right order, automatically.

| | Standard Scripts | **Polaris** |
|:--|:--:|:--:|
| Identity | MAC spoofing | Full anonymization |
| Cookie cleaning | Roblox cookies only | Everything Roblox uses to track you |
| Reinstallation | ✗ | Fresh reinstall from scratch |
| Executor support | ✗ | Automated via WEAO API |
| Settings | Wiped | Backed up & restored |
| Control | Minimal | You decide what runs |

---

## Features

### 🛠 Environment Sanitization
- **Process termination** — force-kills conflicting background agents and Roblox instances before anything runs
- **DNS flush** — clears stale routing and tracking entries from the network cache
- **Identity purge** — targets and removes account-linked tokens and local storage artifacts

### 🕵️ Identity Protection
- **MAC randomization** — generates and applies randomized MAC addresses to your network adapters
- **Smart filtering** — skips virtual, loopback, and kernel-debug interfaces to keep things stable
- **No-reboot cycling** — disables and re-enables adapters automatically to apply changes

### 🍪 Browser Management
- **Direct SQLite access** — removes `roblox.com` cookies at the database level, leaving everything else untouched
- **Handle unlocking** — detects and releases database files locked by active browser processes

### 📦 Roblox Version Control
- **Manifest-based reinstall** — pulls components directly from Roblox's AWS mirrors with live progress tracking
- **Executor sync** — uses the WEAO API to match your chosen executor (Potassium, Severe, etc.) to the right Roblox build
- **Settings preservation** — backs up and restores your sensitivity, volume, and other in-game preferences

---

## Setup

### Prerequisites

- Windows 10 or 11
- Python 3.8+
- Administrator privileges (required for network adapter and registry access)

### Running Polaris

```bash
python polaris.py
```

Accept the UAC prompt. That's it for first launch — a setup wizard handles the rest.

### First-run configuration

The wizard walks you through:

- **Cleaning modules** — toggle process killing, DNS flushing, and token removal individually
- **Identity** — choose whether to spoof MAC addresses and which adapters to target
- **Compatibility** — pick your executor to lock in the correct Roblox version

Your choices are saved to `Polaris.config`. Future runs skip the wizard entirely.

### Execution sequence

```
Kill Processes → Clean Directories → Spoof Identity → Reinstall Roblox → Restore Settings → Launch
```

---

## Technical Details

| Component | Library |
|:--|:--|
| Terminal UI | `rich` |
| HTTP / downloads | `requests` |
| Progress tracking | `tqdm` |
| Browser DB access | `sqlite3` (stdlib) |
| Network adapters | Windows Registry / `netsh` |
