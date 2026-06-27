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

I built Polaris around what I believe is the most important principle in this space: transparency. Most competing applications do the same job — and do it worse — while keeping you in the dark about what you're actually running, and why it works the way it does. That's exactly why I created Polaris, and why it's open source.

## Setup

### Prerequisites

- Windows 10 or 11
- Python 3.8+ (if running source)
- Packages: `tqdm, rich, requests` (Automatically installed on run)
- Administrator privileges (required for network adapter and registry access)

### Installing and Running Polaris

### Recommended

1. Download the Executable file from [here](https://github.com/midinterlude/Polaris/releases/latest)
2. Run the Application
   (Scroll down for 3rd step)

### 'Advanced' Method

1.```bash
git clone https://github.com/midinterlude/Polaris.git
```

2.```bash
python polaris.py
```

### Configuration
3. Accept the UAC prompt. That's it for first launch — a setup wizard handles the rest.

### First-run configuration

The wizard walks you through:

- **Cleaning modules** — toggle process killing, DNS flushing, and token removal individually
- **Identity** — choose whether to spoof MAC addresses and which adapters to target
- **Compatibility** — pick your executor to lock in the correct Roblox version

Your choices are saved to `Polaris.config`. Future runs skip the wizard entirely.
