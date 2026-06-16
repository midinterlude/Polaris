#                                    ▄▄▄·      ▄▄▌   ▄▄▄· ▄▄▄  ▪  .▄▄ · 
#                                   ▐█ ▄█▪     ██•  ▐█ ▀█ ▀▄ █·██ ▐█ ▀. 
#                                    ██▀· ▄█▀▄ ██▪  ▄█▀▀█ ▐▀▀▄ ▐█·▄▀▀▀█▄
#                                   ▐█▪·•▐█▌.▐▌▐█▌▐▌▐█ ▪▐▌▐█•█▌▐█▌▐█▄▪▐█
#                                   .▀    ▀█▄▀▪.▀▀▀  ▀  ▀ .▀  ▀▀▀▀ ▀▀▀▀ 
#
#                                                Information:              
#                                      https://github.com/midinterlude/    
#                                         Developed by: Midinterlude       
#                                             Started 2026-04-14           
#                                          Logs located in Workspace.      





# (imports)         

import os
import sys
import subprocess

def install_requirements():
    # Map package names to their import names
    requirements = {
        "requests": "requests",
        "tqdm": "tqdm",
        "rich": "rich",
        "pywin32": "win32security",
        "qrcode": "qrcode",
        "pillow": "PIL"
    }
    
    missing = []
    for pkg, imp in requirements.items():
        try:
            __import__(imp)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"Missing requirements: {', '.join(missing)}. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("Requirements installed. Please restart the script if you see import errors.")
        except Exception as e:
            print(f"Failed to install requirements: {e}. Please install them manually: pip install {' '.join(missing)}")
            sys.exit(1)

install_requirements()

import ctypes
import json as jsond
import sqlite3
import time
import msvcrt
import shutil
import datetime
import traceback
import uuid
import random
import winreg
import requests
import glob
import tqdm
import zipfile
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Confirm, Prompt
from rich.table import Table
from datetime import timezone, timedelta
from uuid import uuid4


# (variables)

polaris = """
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
"""

def display_config_title():
    clear()
    panel = Panel(
        Align.center(polaris), 
        title="[bold green]Polaris Configuration Menu[/]", 
        border_style="cyan", 
        padding=(0,2,0,2),
        expand=False
    )
    console.print(Align.center(panel))

def run_configurator(location=None):
    display_config_title()
    console.print("\n[bold yellow]Welcome to the Polaris Configuration Menu![/]")
    console.print("This wizard will guide you through creating an optimal [cyan]Polaris.config[/] file.\n")
    
    config = {
        "Base": {},
        "onExit": {},
        "MAC": {},
        "Browsers": {},
        "Removals": {},
        "Roblox": {},
        "Install Config": {}# ,
#        "Monitor": {}
    }

    # 1. Base settings
    console.print(Panel("[bold cyan]Base Environment[/]\n[dim]Core settings for cleaning the execution environment.[/]\n\n• [green]killProcs[/]: Terminate conflicting background processes.\n• [green]removeRobloxToken[/]: Purge account tracking tokens.\n• [green]flushDNS[/]: Clear network routing cache.", border_style="blue", expand=False))
    config["Base"]["killProcs"] = Confirm.ask("Enable killProcs? [orange3](Default: 'True')[/]", default=True, show_default=False)
    config["Base"]["removeRobloxToken"] = Confirm.ask("Enable removeRobloxToken? [orange3](Default: 'True')[/]", default=True, show_default=False)
    config["Base"]["flushDNS"] = Confirm.ask("Enable flushDNS? [orange3](Default: 'True')[/]", default=True, show_default=False)

    # 2. onExit settings
    console.print(Panel("\n[bold cyan]Automation & Exit[/]\n[dim]Define what happens after the cleanup completes.[/]\n\n• [green]launchRoblox[/]: Reopen Roblox immediately.\n• [green]openLog[/]: Show the detailed execution log.\n• [red]restartWindows[/]: Force a system reboot (Use with caution).", border_style="blue", expand=False))
    config["onExit"]["launchRoblox"] = Confirm.ask("Launch Roblox on exit? [orange3](Default: 'True')[/]", default=True, show_default=False)
    config["onExit"]["openLog"] = Confirm.ask("Open log on exit? [orange3](Default: 'True')[/]", default=True, show_default=False)
    config["onExit"]["restartWindows"] = Confirm.ask("Restart Windows on exit? [orange3](Default: 'False')[/]", default=False, show_default=False)

    # 3. MAC settings
    console.print(Panel("\n[bold cyan]Identity Protection[/]\n[dim]Hardware identification spoofing.[/]\n\n• [bold red]spoofMAC[/]: Highly recommended to avoid hardware-linked bans.\n• [green]allAdapters[/]: Apply spoofing to every available network interface.", border_style="blue", expand=False))
    config["MAC"]["spoofMAC"] = Confirm.ask("Enable MAC spoofing? [orange3](Default: 'True')[/]", default=True, show_default=False)
    config["MAC"]["allAdapters"] = Confirm.ask("Apply to all adapters? [orange3](Default: 'True')[/]", default=True, show_default=False)
    config["MAC"]["adapters"] = []
    if not config["MAC"]["allAdapters"] and config["MAC"]["spoofMAC"]:
        adapters_str = Prompt.ask("Enter comma-separated list of adapters to spoof")
        if adapters_str.strip():
            config["MAC"]["adapters"] = [a.strip() for a in adapters_str.split(",")]

    # 4. Browsers settings
    console.print(Panel("\n[bold cyan]Browser Cleanup[/]\n[dim]Manage web-based tracking data.[/]\n\n• [yellow]removeCookies[/]: Target specific domains.\n• [red]removeAll[/]: Complete cookie wipeout.\n• [green]removedSites[/]: Targeted domains (Default: roblox.com).", border_style="blue", expand=False))
    config["Browsers"]["removeCookies"] = Confirm.ask("Remove cookies? [orange3](Default: 'True')[/]", default=True, show_default=False)
    config["Browsers"]["removeAll"] = Confirm.ask("Remove ALL browser cookies? [orange3](Default: 'False')[/]", default=False, show_default=False)
    sites_str = Prompt.ask("Sites to remove cookies for (comma-separated) [orange3](Default: 'roblox.com')[/]", default="roblox.com", show_default=False)
    config["Browsers"]["removedSites"] = [s.strip() for s in sites_str.split(",") if s.strip()]

    # 5. Removals settings
    console.print(Panel("\n[bold cyan]System Paths[/]\n[dim]Configures default targets for file and folder deletion.[/]", border_style="blue", expand=False))
    config["Removals"] = {
        "files": ["%appdata%\\local\\Roblox\\Localstorage\\RobloxCookies.dat"],
        "folders": ["%temp%", "%localappdata%\\Roblox", "%appdata%\\Roblox"],
        "processes": ["RobloxPlayerBeta.exe","RobloxPlayerLauncher.exe"]
    }
    console.print("[dim]→ Initialized default removal targets.[/]")

    # 6. Roblox settings
    console.print(Panel("\n[bold cyan]Roblox Integrity[/]\n[dim]Deep cleanup and reinstallation settings.[/]\n\n• [green]removeFolders[/]: Purge local application data.\n• [green]reinstallRoblox[/]: Clean re-download of components.\n• [green]preserveSettings[/]: Keep [white]GlobalBasicSettings_13.xml[/].\n\n[bold red]⚠  Reinstalling uses up to ~150MB+ of disk space.[/]", border_style="red", expand=False))
    config["Roblox"]["removeFolders"] = Confirm.ask("Remove Roblox folders? [orange3](Default: 'True')[/]", default=True, show_default=False)
    config["Roblox"]["reinstallRoblox"] = Confirm.ask("Reinstall Roblox after cleanup? [orange3](Default: 'True')[/]", default=True, show_default=False)
    config["Roblox"]["preserveSettings"] = Confirm.ask("Preserve Roblox settings? [orange3](Default: 'True')[/]", default=True, show_default=False)

    # 7. Install Config
    console.print(Panel("\n[bold cyan]Version & Compatibility[/]\n[dim]Select the specific build of Roblox to install.[/]\n\n• [yellow]latestVersion[/]: Always pull newest build.\n• [green]useExecutor[/]: Auto-resolve build based on your software.", border_style="blue", expand=False))
    config["Install Config"]["latestVersion"] = Confirm.ask("Force latest Roblox version? [orange3](Default: 'False')[/]", default=False, show_default=False)
    config["Install Config"]["versionHash"] = Prompt.ask("Enter specific version hash to install (leave blank if none) [orange3](Default: '')[/]", default="", show_default=False)
    config["Install Config"]["useExecutor"] = Confirm.ask("Use a specific executor? [orange3](Default: 'True')[/]", default=True, show_default=False)
    if config["Install Config"]["useExecutor"]:
        while True:
            executor_name = Prompt.ask("Enter executor name (type 'list' to see options) [orange3](Default: 'Potassium')[/]", default="Potassium", show_default=False)
            if executor_name.strip().lower() == "list":
                try:
                    with console.status("[bold green]Fetching executors from WEAO API..."):
                        response = requests_get_retry(
                            'https://weao.xyz/api/status/exploits', 
                            headers={'User-Agent': 'WEAO-3PService'}
                        )
                        data = response.json()
                            
                    table = Table(title="Supported Executors from WEAO")
                    table.add_column("Name", style="cyan", no_wrap=True)
                    table.add_column("Version", style="magenta")
                    table.add_column("Updated Date")
                    
                    now = datetime.datetime.now(timezone.utc)
                    for exploit in data:
                        ex_type = str(exploit.get("extype", "")).lower()
                        
                        # Only show Windows executors
                        if ex_type != "wexecutor":
                            continue

                        # Extract and parse date
                        date_str = exploit.get("updatedDate", "Unknown")
                        date_display = date_str.split(" at")[0]
                        
                        color = "green"
                        try:
                            # Format: 04/06/2026 at 2:05 AM UTC
                            dt = datetime.datetime.strptime(date_str, "%m/%d/%Y at %I:%M %p UTC").replace(tzinfo=timezone.utc)
                            diff = now - dt
                            if diff > timedelta(days=30):
                                color = "red"
                            elif diff > timedelta(days=14):
                                color = "orange3"
                        except:
                            pass # Keep green/unknown if parsing fails
                        
                        table.add_row(
                            exploit.get("title", "Unknown"), 
                            exploit.get("version", "N/A"), 
                            f"[{color}]{date_display}[/]"
                        )
                        
                    console.print(table)
                    console.print("[dim italic]Note: Green dates indicate recent updates and do not guarantee the executor is currently working.[/]")
                except Exception as e:
                    console.print(f"[bold red]Failed to fetch from WEAO API:[/] {e}")
            else:
                config["Install Config"]["executor"] = executor_name.strip()
                break
    else:
        config["Install Config"]["executor"] = ""

    # # 8. Monitor Settings
    # console.print(Panel("\n[bold cyan]Background Monitor[/]\n[dim]Configure background automation behavior.[/]", border_style="blue", expand=False))
    # config["Monitor"]["triggerMode"] = Prompt.ask("Monitor Trigger Mode (Prompt/Auto) [orange3](Default: 'Prompt')[/]", choices=["Prompt", "Auto"], default="Prompt", show_default=False)
    # config["Monitor"]["targetPath"] = Prompt.ask(f"Path to Polaris executable or python script [orange3](Default: '{Polarislocation}')[/]", default=Polarislocation, show_default=False)
    # console.print()

    # Output
    save_dir = location if location else Polarislocation
    config_path = os.path.join(save_dir, "Polaris.config")
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            jsond.dump(config, f, indent=4)
        console.print(f"[bold green]Success![/] Saved configuration to [bold white]{config_path}[/]")
    except Exception as e:
        console.print(f"[bold red]Failed to save configuration:[/] {e}")



# (paths)

console = Console()

## Polaris Location
if getattr(sys, 'frozen', False):
    Polarislocation = os.path.dirname(sys.executable)
else:
    Polarislocation = os.path.dirname(os.path.abspath(__file__))

## Misc Folder and internals

workspace = os.path.join(Polarislocation, "workspace")
latest_logfile = os.path.join(workspace, "latest.log")
session_timestamp = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M")
session_hash = uuid.uuid4().hex[:6]
session_logfile = os.path.join(workspace, f"Polaris_{session_timestamp}_{session_hash}.log")

# (config variables)
Config = {} # Main configuration object

class ProcessError(Exception):
    def __init__(self, message, operation=None, details=None):
        super().__init__(message)
        self.operation = operation
        self.details = details or {}

class DownloadError(Exception):
    def __init__(self, message, operation=None, details=None):
        super().__init__(message)
        self.operation = operation
        self.details = details or {}

class NetworkError(Exception):
    def __init__(self, message, operation=None, details=None):
        super().__init__(message)
        self.operation = operation
        self.details = details or {}

# (definitions)

def log(action, message, level="INFO"):
    try:
        os.makedirs(workspace, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level.upper()}] [{action}] {message}\n"
        
        for target in [latest_logfile, session_logfile]:
            with open(target, "a", encoding="utf-8") as f:
                f.write(log_entry)
    except Exception as e:
        print(f"LogFailed: {e}")

def logException(action, error):
    try:
        error_msg = f"{error}\n{traceback.format_exc()}"
        log(action, error_msg, level="ERROR")
    except Exception as log_e:
        print(f"LogFailed: {log_e}")

## console
def clear():
    os.system('cls')

def title():
    clear()
    console.print(Align.center(polaris))

def autoClose():
    log("Close","Automatically Closing")
    title()
    timer = 15
    starttime = time.time()

    # Move down a bit to separate from the history log
    print("\n")
    
    while time.time() - starttime < timer:
        time_left = int(timer - (time.time() - starttime))
        timer_text = f" Exiting in {time_left}s... (Press Any Key to Exit.)"
        padding = " " * ((console.width - len(timer_text)) // 2)
        console.print(f"{padding}[cyan]Exiting in[/] [bold]{time_left}s[/]... [dim](Press [bold]Any Key[/] to Exit.)[/]", end="\r")
        if msvcrt.kbhit():
            msvcrt.getch() # consume key
            break
        time.sleep(0.1)
    print("\n") # Final newline after countdown
    
    if Config.get("onExit", {}).get("launchRoblox"):
        try:
            roblox_path = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions")
            if os.path.exists(roblox_path):
                versions = [d for d in os.listdir(roblox_path) if os.path.isdir(os.path.join(roblox_path, d))]
                for v in versions:
                    exe_path = os.path.join(roblox_path, v, "RobloxPlayerBeta.exe")
                    if os.path.exists(exe_path):
                        subprocess.Popen([exe_path])
                        log("Exit", f"Launched Roblox from {exe_path}")
                        break
        except Exception as e:
            logException("Exit", e)

    if Config.get("onExit", {}).get("openLog"):
        try:
            os.startfile(latest_logfile)
        except Exception as e:
            logException("Exit", e)

    if Config.get("onExit", {}).get("restartWindows"):
        try:
            log("Exit", "System restart initiated by user config")
            os.system("shutdown /r /t 5")
        except Exception as e:
            logException("Exit", e)
    
    sys.exit()
    

## deletion
def delete(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
            log("FileSystem", f"Successfully deleted target file: {filename}")
            return os.path.basename(filename)
        except Exception as e:
            logException("FileSystem", e)
            return None
    else:
        log("FileSystem", f"Skipped deletion: File not found ({filename})", level="DEBUG")
        return None
        

def removeFolder(foldername):
    if os.path.exists(foldername):
        try:
            shutil.rmtree(foldername)
            log("FileSystem", f"Removed directory: {foldername}")
            return os.path.basename(foldername)
        except Exception as e:
            log("FileSystem", f"shutil.rmtree failed for {foldername}, attempting manual clear.", level="WARN")
            folderfiles = os.listdir(foldername)
            for file in folderfiles:
                filepath = os.path.join(foldername, file)
                delete(filepath)
            try:
                os.rmdir(foldername)
                log("FileSystem", f"Manually removed directory: {foldername}")
                return os.path.basename(foldername)
            except Exception as e2:
                logException("FileSystem", e2)
                return None
    return None

## Initialization

def checkAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_wt_path():
    if os.name != 'nt':
        return None
    wt_path = shutil.which("wt.exe") or shutil.which("wt")
    if wt_path:
        return wt_path
    default_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe")
    if os.path.exists(default_path):
        return default_path
    return None

def prefer_terminal():
    if os.name != 'nt':
        return
    
    # Check if already running in Windows Terminal or if we should skip relaunch
    if "WT_SESSION" in os.environ or "--no-wt-relaunch" in sys.argv:
        return

    wt_path = get_wt_path()
    if not wt_path:
        return

    # Prepare command arguments
    new_args = sys.argv.copy()
    if "--no-wt-relaunch" not in new_args:
        new_args.append("--no-wt-relaunch")
    
    # Escape quotes in arguments if needed
    formatted_args = []
    for arg in new_args:
        if " " in arg:
            formatted_args.append(f'"{arg}"')
        else:
            formatted_args.append(arg)

    wt_args = f'"{sys.executable}" {" ".join(formatted_args)}'
    
    # If not admin, we can elevate directly using WT
    verb = "runas" if not checkAdmin() else None
    
    try:
        ctypes.windll.shell32.ShellExecuteW(None, verb, wt_path, wt_args, None, 1)
        sys.exit(0)
    except Exception as e:
        # Fallback to current execution if relaunch fails
        log("System", f"Failed to relaunch in Windows Terminal: {e}", level="WARNING")

def Initialize():
    # Ensure Administrator Privileges
    log("System", f"Admin: {checkAdmin()} | Executable: {sys.executable} | Args: {sys.argv}")
    try:
        with open(latest_logfile, "w", encoding="utf-8") as f:
            pass
    except Exception as e:
        logException("System", e)
    
    if not checkAdmin():
        log("System", "Requesting UAC")
        new_args = sys.argv + ["--direct-run"] if "--direct-run" not in sys.argv else sys.argv
        
        wt_path = get_wt_path()
        if wt_path and "--no-wt-relaunch" not in new_args:
            new_args.append("--no-wt-relaunch")
            formatted_args = []
            for arg in new_args:
                if " " in arg:
                    formatted_args.append(f'"{arg}"')
                else:
                    formatted_args.append(arg)
            wt_args = f'"{sys.executable}" {" ".join(formatted_args)}'
            ctypes.windll.shell32.ShellExecuteW(None, "runas", wt_path, wt_args, None, 1)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(new_args), None, 1)
        sys.exit(0)
    if not os.path.exists(workspace):
        try:
            os.makedirs(workspace)
            log("System", f"Created workspace at {workspace}")
        except Exception as e:
            logException("System", e)

    # Resolve config path
    config_in_Polaris = os.path.join(Polarislocation, "Polaris.config")
    config_in_workspace = os.path.join(workspace, "Polaris.config")

    final_config_path = ""
    if os.path.exists(config_in_Polaris):
        final_config_path = config_in_Polaris
    elif os.path.exists(config_in_workspace):
        final_config_path = config_in_workspace

    if not final_config_path or not loadconfig(final_config_path):
        log("Config", "Config missing or invalid, launching configurator", level="INFO")
        run_configurator(Polarislocation)
        final_config_path = config_in_Polaris
        loadconfig(final_config_path)
    
    return final_config_path

def run_cmd(cmd, capture_output=True, shell=False):
    try:
        if capture_output:
            return subprocess.run(cmd, capture_output=True, text=True, shell=shell)
        return subprocess.run(cmd, shell=shell)
    except Exception as e:
        logException("Process", e)
        return None

## Kill Processes
def killprocess(process_list=None):
    targets = process_list or Config.get("Removals", {}).get("processes", [])
    if not targets:
        log("Process", "No processes specified to kill.", level="DEBUG")
        return []
    killed = []
    for ptk in targets:
        try:
            result = subprocess.run(["taskkill", "/f", "/im", ptk], capture_output=True)
            if result.returncode == 0:
                log("Process", f"Successfully killed: {ptk}")
                killed.append(ptk)
            else:
                log("Process", f"Failed to kill {ptk}: {result.stderr.decode() if result.stderr else 'Process not found'}", level="WARNING")
        except Exception as e:
            logException("Process", e)
    return killed

## Configuration system
def validate_config(config):
    required_sections = ["Base", "onExit", "MAC", "Browsers", "Removals", "Roblox", "Install Config"] # "Monitor"
    if not isinstance(config, dict):
        return False, "Configuration is not a JSON object."
    for section in required_sections:
        if section not in config or not isinstance(config[section], dict):
            return False, f"Missing or invalid section: '{section}'"
    return True, None

def loadconfig(config_path):
    global Config
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = jsond.load(f)
        
        is_valid, error_msg = validate_config(data)
        if not is_valid:
            log("Config", f"Integrity check failed: {error_msg}", level="ERROR")
            return {}

        Config = data
        return Config
    except Exception as e:
        logException("Config", e)
        return {}

## MAC Spoofing

def gen_mac():
    mac_bytes = [0x02] + [random.randint(0, 255) for _ in range(5)]
    return "".join(f"{byte:02X}" for byte in mac_bytes)

def list_adapters():
    try:
        adapters = []
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}",
        ) as class_key:
            for i in range(10000):
                try:
                    subkey_name = f"{i:04d}"
                    with winreg.OpenKey(class_key, subkey_name) as adapter_key:
                        try:
                            driver_desc = winreg.QueryValueEx(adapter_key, "DriverDesc")[0]
                            net_cfg_instance_id = winreg.QueryValueEx(adapter_key, "NetCfgInstanceId")[0]

                            try:
                                connection_path = f"SYSTEM\\CurrentControlSet\\Control\\Network\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{net_cfg_instance_id}\\Connection"
                                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, connection_path) as conn_key:
                                    connection_name = winreg.QueryValueEx(conn_key, "Name")[0]
                            except:
                                connection_name = driver_desc

                            desc_lower = driver_desc.lower()
                            if not any(keyword in desc_lower for    word in ["virtual", "loopback", "bluetooth", "wan miniport", "tap-windows", "pseudo", "kernel debug"]):
                                adapters.append({"id": subkey_name, "description": driver_desc, "connection_name": connection_name})
                        except (FileNotFoundError, OSError):
                            continue
                except FileNotFoundError:
                    break
        return adapters
    except Exception as e:
        logException("MAC", e)
        return []

def change_mac(adapter_id, mac_address):
    try:
        path = f"SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e972-e325-11ce-bfc1-08002be10318}}\\{adapter_id}"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE) as adapter_key:
            winreg.SetValueEx(adapter_key, "NetworkAddress", 0, winreg.REG_SZ, mac_address)
    except Exception as e:
        raise ProcessError(f"Registry error: {e}")

def restart_adapter(connection_name):
    actions = []
    
    disable_cmd = f'netsh interface set interface name="{connection_name}" admin=disable'
    disable_result = run_cmd(disable_cmd, shell=True)
    if disable_result and disable_result.returncode == 0:
        actions.append(f"Interface disabled: {connection_name}")
    else:
        log("MAC", f"Failed to disable interface '{connection_name}'.", level="WARN")
        actions.append(f"Failed to disable {connection_name}")
    
    time.sleep(2)
    
    enable_cmd = f'netsh interface set interface name="{connection_name}" admin=enable'
    enable_result = run_cmd(enable_cmd, shell=True)
    if enable_result and enable_result.returncode == 0:
        actions.append(f"Interface enabled: {connection_name}")
    else:
        log("MAC", f"Failed to enable interface '{connection_name}'.", level="WARN")
        actions.append(f"Failed to re-enable {connection_name}")
    return actions

def wait_for_connection(timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            requests.get("http://www.google.com", timeout=2)
            return True
        except:
            time.sleep(1)
    return False

def requests_get_retry(url, headers=None, retries=3, delay=2, timeout=10):
    last_err = None
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout, verify=True)
            response.raise_for_status()
            return response
        except Exception as e:
            last_err = e
            if i < retries - 1:
                time.sleep(delay)
    raise last_err

def SpoofMAC(config=None, details_callback=None):
    config = config or Config
    mac_config = config.get("MAC", {})
    if not mac_config.get("spoofMAC"):
        return []

    def add_action(text):
        actions.append(text)
        if details_callback:
            details_callback(actions)

    log("MAC", "Starting verbose MAC spoofing operation")
    actions = []
    
    adapters = list_adapters()
    if not adapters:
        log("MAC", "No adapters found.")
        return ["No compatible hardware adapters found."]

    add_action(f"Found {len(adapters)} potential network adapters.")

    all_adapters = mac_config.get("allAdapters", True)
    target_names = mac_config.get("adapters", [])

    for adapter in adapters:
        is_target = all_adapters or adapter["connection_name"] in target_names or adapter["description"] in target_names
        
        if is_target:
            add_action(f"Targeting adapter: {adapter['connection_name']}")
            new_mac = gen_mac()
            add_action(f"  - Generating random MAC: {new_mac}")
            try:
                change_mac(adapter["id"], new_mac)
                log("MAC", f"Changed MAC for {adapter['connection_name']} to {new_mac}")
                add_action(f"  - Registry key updated for ID {adapter['id']}")
                
                # Cycle interface
                reset_actions = restart_adapter(adapter["connection_name"])
                for ra in reset_actions:
                    add_action(f"  - {ra}")
                
            except Exception as e:
                logException("MAC", e)
                add_action(f"  - [red]Failed to spoof {adapter['connection_name']}: {e}[/]")
        else:
            add_action(f"Skipping adapter: {adapter['connection_name']} (Not in target list)")

    return actions

## Browser Cookie Removal

def remove_cookies_for_host(cookie_file: str, host: str):
    if not os.path.exists(cookie_file): return
    conn = None
    try:
        conn = sqlite3.connect(cookie_file)
        cursor = conn.cursor()
        
        # Determine table and column
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        table_name = 'cookies' if 'cookies' in tables else ('moz_cookies' if 'moz_cookies' in tables else None)
        if not table_name: return
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [c[1] for c in cursor.fetchall()]
        host_col = 'host_key' if 'host_key' in columns else ('host' if 'host' in columns else None)
        if not host_col: return

        # VACUUM to fix potential corruption/indices (Common in Zen/Firefox)
        try:
            cursor.execute("VACUUM")
        except Exception as ve:
            log("Browsers", f"VACUUM failed (proceeding anyway): {ve}", level="DEBUG")
        
        # Targeted deletion
        cursor.execute(f"DELETE FROM {table_name} WHERE {host_col} LIKE ?", (f"%{host}%",))
        conn.commit()
        
        if cursor.rowcount > 0:
            log("Browsers", f"Cleaned {host} from {os.path.basename(cookie_file)} ({cursor.rowcount} records)")
    except Exception as e:
        log("Browsers", f"Error cleaning {cookie_file}: {e}", level="WARN")
    finally:
        if conn: conn.close()

def clean_browser_cookies(sites=None, remove_all=False):
    log("Browsers", "Cleaning cookies")
    cleaned_browsers = []
    
    browsers = [
        ("Chrome", r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Network\Cookies", "chrome.exe"),
        ("Chrome (Legacy)", r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cookies", "chrome.exe"),
        ("Edge", r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Network\Cookies", "msedge.exe"),
        ("Opera GX", r"%APPDATA%\Opera Software\Opera GX Stable\Network\Cookies", "opera.exe"),
        ("Brave", r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies", "brave.exe"),
        ("Firefox", r"%APPDATA%\Mozilla\Firefox\Profiles\*.default-release\cookies.sqlite", "firefox.exe"),
        ("Firefox (All)", r"%APPDATA%\Mozilla\Firefox\Profiles\*.default*\cookies.sqlite", "firefox.exe"),
        ("Zen", r"%APPDATA%\Zen\Profiles\*\cookies.sqlite", "zen.exe"),
        ("Zen (Alt)", r"%APPDATA%\zen-browser\Profiles\*\cookies.sqlite", "zen.exe"),
        ("Vivaldi", r"%LOCALAPPDATA%\Vivaldi\User Data\Default\Network\Cookies", "vivaldi.exe"),
    ]
    
    # Track which browser processes we've already tried to kill this session
    killed_processes = set()

    for name, path, exe in browsers:
        for file_path in glob.glob(os.path.expandvars(path)):
            if os.path.exists(file_path):
                # If we're about to touch this browser's files, ensure it's closed
                if exe not in killed_processes:
                    log("Browsers", f"Terminating {name} ({exe}) to unlock cookie files...")
                    try:
                        subprocess.run(["taskkill", "/f", "/im", exe], capture_output=True)
                        killed_processes.add(exe)
                        time.sleep(2.0) # Grace period for OS file handles to release
                    except Exception as e:
                        log("Browsers", f"Failed to terminate {exe}: {e}", level="WARNING")

                # Clear WAL/SHM sidecar files to prevent malformed errors
                for ext in ["-wal", "-shm"]:
                    sidecar = file_path + ext
                    if os.path.exists(sidecar): 
                        try: os.remove(sidecar)
                        except: pass

                if remove_all:
                    try:
                        os.remove(file_path)
                        log("Browsers", f"Deleted {file_path}")
                        if name not in cleaned_browsers: cleaned_browsers.append(name)
                    except Exception as e: log("Browsers", f"Failed to delete {file_path}: {e}", level="WARN")
                else:
                    for site in (sites or ["roblox.com"]):
                        remove_cookies_for_host(file_path, site)
                    if name not in cleaned_browsers: cleaned_browsers.append(name)
    return cleaned_browsers

def CreateStartMenuShortcut(version_path):
    try:
        log("Roblox", f"Attempting to create Start Menu shortcut for: {version_path}")
        start_menu_path = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Roblox")
        os.makedirs(start_menu_path, exist_ok=True)
        
        shortcut_path = os.path.join(start_menu_path, "Roblox Player.lnk")
        target_exe = os.path.join(version_path, "RobloxPlayerBeta.exe")
        
        if not os.path.exists(target_exe):
            log("Roblox", f"Shortcut target not found: {target_exe}", level="WARN")
            return False

        # PowerShell script to create shortcut
        ps_command = f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_path}');$s.TargetPath='{target_exe}';$s.WorkingDirectory='{version_path}';$s.Save()"
        
        result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_command], capture_output=True, text=True)
        if result.returncode == 0:
            log("Roblox", f"Start Menu shortcut created/updated at {shortcut_path}")
            return True
        else:
            log("Roblox", f"Failed to create shortcut using PowerShell: {result.stderr}", level="ERROR")
            return False
    except Exception as e:
        logException("Roblox", e)
        return False

## Roblox Settings & Download

def RobloxSettings(config=None, status_handler=None):
    log("Roblox", "Processing Roblox reinstallation")
    config = config or Config
    try:
        install_cfg = config.get("Install Config", {})
        roblox_cfg = config.get("Roblox", {})
        
        executor = install_cfg.get("executor", "").strip()
        version_hash = ""

        if status_handler:
            status_handler("Resolving Roblox installation version...")

        if executor:
            log("Roblox", f"Using executor: {executor}")
            try:
                resp = requests_get_retry("https://weao.xyz/api/status/exploits")
                for ex in resp.json():
                    if ex.get("title", "").lower() == executor.lower():
                        version_hash = ex.get("rbxversion", "")
                        break
            except Exception as e: log("Roblox", f"WEAO API failed: {e}", level="WARN")

        if not version_hash and not install_cfg.get("latestVersion", True):
            version_hash = install_cfg.get("versionHash", "")

        if not version_hash:
            try:
                resp = requests_get_retry("https://weao.xyz/api/versions/current")
                version_hash = resp.json().get("Windows", {}).get("version", "")
            except: pass
        
        if not version_hash:
            try:
                channel = roblox_cfg.get("channel", "LIVE")
                resp = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer/channel/{channel}")
                version_hash = resp.json().get("clientVersionUpload", "")
            except: pass

        if not version_hash:
            log("Roblox", "Could not resolve version hash.", level="ERROR")
            return False

        log("Roblox", f"Version hash: {version_hash}")
        target_dir = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions\\" + version_hash)
        os.makedirs(target_dir, exist_ok=True)
        
        # Download Manifest
        if status_handler:
            status_handler("Calculating Roblox package sizes...", details=[f"Version: {version_hash}"])

        channel = roblox_cfg.get("channel", "LIVE").lower()
        manifest_url = f"https://setup-aws.rbxcdn.com/channel/{channel}/{version_hash}-rbxPkgManifest.txt"
        resp = requests.get(manifest_url)
        if not resp.ok:
            manifest_url = f"https://setup-aws.rbxcdn.com/channel/common/{version_hash}-rbxPkgManifest.txt"
            resp = requests.get(manifest_url)
        
        resp.raise_for_status()
        packages = [line.strip() for line in resp.text.split("\n") if line.strip().endswith(".zip")]
        
        total_size = 0
        pkg_data = []
        for pkg in packages:
            pkg_url = f"https://setup-aws.rbxcdn.com/{version_hash}-{pkg}"
            h = requests.head(pkg_url)
            size = int(h.headers.get("content-length", 0))
            total_size += size
            pkg_data.append((pkg, pkg_url, size))

        if status_handler:
            # Update the last status line with the final size
            # We can't easily reach back, so we just set a new status or we use a more complex global state
            # For simplicity, we just add a new detail line in the next status
            log("Roblox", f"Total size verified: {total_size/1024/1024:.2f} MB")

        extract_map = {
            "RobloxApp.zip": "", "redist.zip": "", "shaders.zip": "shaders/", "ssl.zip": "ssl/",
            "content-avatar.zip": "content/avatar/", "content-configs.zip": "content/configs/",
            "content-fonts.zip": "content/fonts/", "content-sky.zip": "content/sky/",
            "content-sounds.zip": "content/sounds/", "content-textures2.zip": "content/textures/",
            "content-models.zip": "content/models/", "content-platform-fonts.zip": "PlatformContent/pc/fonts/",
            "content-platform-dictionaries.zip": "PlatformContent/pc/shared_compression_dictionaries/",
            "content-terrain.zip": "PlatformContent/pc/terrain/", "content-textures3.zip": "PlatformContent/pc/textures/",
            "extracontent-luapackages.zip": "ExtraContent/LuaPackages/", "extracontent-translations.zip": "ExtraContent/translations/",
            "extracontent-models.zip": "ExtraContent/models/", "extracontent-textures.zip": "ExtraContent/textures/",
            "extracontent-places.zip": "ExtraContent/places/",
        }

        temp_dir = os.path.expandvars(r"%temp%\robloxDownloadPolaris")
        os.makedirs(temp_dir, exist_ok=True)

        title()
        console.print(Align.center(f"[bold cyan]Downloading Roblox Components ({total_size/1024/1024:.2f} MB total)[/]"))
        print("\n")

        # Simplified Stacked Progress Bars
        overall_pbar = tqdm.tqdm(
            total=total_size, 
            unit="B", 
            unit_scale=True, 
            desc="Overall Progress", 
            dynamic_ncols=True,
            colour="green",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            leave=True
        )
        
        # Stylized divider between bars
        divider = tqdm.tqdm(total=0, bar_format="{bar}", ascii="=", dynamic_ncols=True, leave=True)

        for pkg, url, size in pkg_data:
            temp_file = os.path.join(temp_dir, pkg)
            try:
                resp = requests.get(url, stream=True, timeout=30)
                resp.raise_for_status()
                
                # Per-file progress bar (nested)
                pbar = tqdm.tqdm(
                    total=size,
                    unit="B",
                    unit_scale=True,
                    desc=f"Downloading {pkg}",
                    leave=False,
                    dynamic_ncols=True,
                    colour="cyan",
                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]"
                )
                
                with open(temp_file, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
                            overall_pbar.update(len(chunk))
                pbar.close()

                # Extraction
                with zipfile.ZipFile(temp_file, "r") as z:
                    root = extract_map.get(pkg, "")
                    for member in z.namelist():
                        if member.endswith("/") or member.endswith("\\"): continue
                        target = os.path.join(target_dir, root, member.replace("\\", "/"))
                        os.makedirs(os.path.dirname(target), exist_ok=True)
                        with z.open(member) as s, open(target, "wb") as t:
                            shutil.copyfileobj(s, t)
                
                # Centered install log
                log_text = f" √ Installed {pkg}"
                padding = " " * ((console.width - len(log_text)) // 2)
                overall_pbar.write(f"{padding}\033[32m√\033[0m Installed {pkg}")
                os.remove(temp_file)
                
            except Exception as e:
                log("Roblox", f"Failed to process {pkg}: {e}", level="ERROR")
                tqdm.tqdm.write(f" \033[31mX\033[0m Failed: {pkg}")

        overall_pbar.close()
        divider.close()

        # AppSettings.xml
        with open(os.path.join(target_dir, "AppSettings.xml"), "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<Settings>\n    <ContentFolder>content</ContentFolder>\n    <BaseUrl>http://www.roblox.com</BaseUrl>\n</Settings>')
        
        # Update Start Menu
        if status_handler:
            status_handler("Updating Start Menu shortcuts...")
        CreateStartMenuShortcut(target_dir)

        log("Roblox", "Installation complete.")
        return True
    except Exception as e:
        logException("Roblox", e)
        return False

def run():
    try:
        log("System", f"Admin: {checkAdmin()} | Executable: {sys.executable} | Args: {sys.argv}")
        config_path = Initialize()
        if not loadconfig(config_path):
            autoClose()
            return
    except Exception as e:
        logException("Run", e)
        update_status(f"Startup failed: {e}", level="error")
        autoClose()
        return
    log("System", "Run sequence started.")

    status_history = []
    def render_status():
        title()
        for item in status_history:
            color = "green" if item["level"] == "info" else "red"
            bullet = "√" if item["level"] == "info" else "X"
            console.print(f" [[{color}]{bullet}[/]] {item['msg']}")
            for detail in item["details"]:
                console.print(f"    [dim]- {detail}[/]")

    def update_status(msg, level="info", details=None):
        if details is None: details = []
        status_history.append({"msg": msg, "level": level, "details": details})
        render_status()

    base = Config.get("Base", {})
    roblox = Config.get("Roblox", {})
    removals = Config.get("Removals", {})
    mac = Config.get("MAC", {})
    browsers = Config.get("Browsers", {})

    # Settings Preservation Backup
    settings_file = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\GlobalBasicSettings_13.xml")
    settings_backup = None

    if roblox.get("preserveSettings") and os.path.exists(settings_file):
        try:
            with open(settings_file, "rb") as f:
                settings_backup = f.read()
            log("Roblox", "Backed up GlobalBasicSettings_13.xml for preservation.")
        except Exception as e:
            logException("Roblox", e)

    if base.get("killProcs"):
        update_status("Killing background processes...")
        killed = killprocess()
        if killed:
            status_history[-1]["details"] = [f"Terminated: {p}" for p in killed]
            render_status()

    if roblox.get("removeFolders"):
        update_status("Cleaning selected directories...")
        removed = []
        for folder in removals.get("folders", []):
            res = removeFolder(os.path.expandvars(folder))
            if res: removed.append(res)
        if removed:
            status_history[-1]["details"] = [f"Removed: {f}" for f in removed]
            render_status()

    if base.get("removeRobloxToken"):
        update_status("Removing account tokens...")
        deleted = []
        for file in removals.get("files", []):
            res = delete(os.path.expandvars(file))
            if res: deleted.append(res)
        if deleted:
            status_history[-1]["details"] = [f"Deleted: {f}" for f in deleted]
            render_status()

    # Restore preserved settings after folder/file removals
    if settings_backup:
        try:
            os.makedirs(os.path.dirname(settings_file), exist_ok=True)
            with open(settings_file, "wb") as f:
                f.write(settings_backup)
            log("Roblox", "Restored GlobalBasicSettings_13.xml")
            update_status("Restored preserved Roblox settings.")
        except Exception as e:
            logException("Roblox", e)

    if browsers.get("removeCookies") or browsers.get("removeAll"):
        update_status("Cleaning browser cookies...")
        cleaned = clean_browser_cookies(browsers.get("removedSites"), browsers.get("removeAll"))
        if cleaned:
            status_history[-1]["details"] = [f"Cleaned: {b}" for b in cleaned]
            render_status()

    if base.get("flushDNS"):
        update_status("Flushing DNS cache...")
        res = subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
        if res.returncode == 0:
            status_history[-1]["details"] = ["DNS cache purged successfully."]
            render_status()

    if mac.get("spoofMAC"):
        update_status("Spoofing network MAC address...")
        
        # Pass callback for live updates
        def sync_details(actions):
            status_history[-1]["details"] = actions
            render_status()
            
        SpoofMAC(details_callback=sync_details)
        
        # Dynamic loading bar for connection
        with console.status("[bold cyan]Waiting for network connection...", spinner="dots"):
            if wait_for_connection(timeout=45):
                update_status("Network connection restored.")
                status_history[-1]["details"] = ["Ping successful!"]
            else:
                update_status("Network connection timeout.", level="error")
                status_history[-1]["details"] = ["System might be offline."]
            render_status()

    if roblox.get("reinstallRoblox"):
        res = RobloxSettings(status_handler=update_status)
        if not res:
            status_history[-1]["level"] = "error"
            title()

    update_status("Sequence completed.")
    autoClose()

if __name__ == "__main__":
    try:
        # Prefer Windows Terminal over Command Prompt if available
        prefer_terminal()

        if "--direct-run" in sys.argv:
            run()
            sys.exit(0)

        cfg_path = os.path.join(Polarislocation, "Polaris.config")
        if not os.path.exists(cfg_path):
            run_configurator()
            if Confirm.ask("Run now?"): run()
        else:
            display_config_title()
            
            choice = "run"
            timer = 10
            start = time.time()
            
            console.print(Align.center(r"[bold]Action?[/] [cyan]\[Press 'R' to Run or 'C' to Configure.][/]"))
            
            while time.time() - start < timer:
                time_left = int(timer - (time.time() - start))
                timer_text = f" -- Auto-starting in {time_left}s... (Press Esc to Cancel) --"
                padding = " " * ((console.width - len(timer_text)) // 2)
                console.print(f"{padding}[cyan]-- Auto-starting in[/] [bold]{time_left}s[/]... [dim](Press [bold yellow]Esc[/] to Cancel)[/] [cyan]--[/]", end="\r")
                
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'\x1b':
                        console.print("\n\n [bold red]Operation cancelled by user.[/]\n")
                        sys.exit(0)
                        
                    key_lower = key.lower()
                    if key_lower == b'c':
                        choice = "configure"
                    else:
                        choice = "run"
                    break
                time.sleep(0.1)
            
            print("\n") # New line after choice
            
            if choice == "configure":
                run_configurator()
                if Confirm.ask("Run now? [orange3](Default: 'True')[/]", default=True, show_default=False): run()
            else:
                run()
    except KeyboardInterrupt:
        sys.exit(0)