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

# =======
# Imports
# =======

import ctypes
import datetime
import glob
import json as jsond
import msvcrt
import os
import re
import secrets
import shutil
import sqlite3
import subprocess
import sys
import time
import traceback
import uuid
import winreg
import zipfile
from datetime import timedelta, timezone


def install_requirements():
    requirements = {
        "requests": "requests",
        "tqdm": "tqdm",
        "rich": "rich",
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

import requests  # noqa: E402
import tqdm  # noqa: E402
from rich.align import Align  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.prompt import Confirm, Prompt  # noqa: E402
from rich.table import Table  # noqa: E402

# =====================
# Constants & Variables
# =====================

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

console = Console()

if getattr(sys, "frozen", False):
    Polarislocation = os.path.dirname(sys.executable)
else:
    Polarislocation = os.path.dirname(os.path.abspath(__file__))

workspace = os.path.join(Polarislocation, "workspace")
latestLogfile = os.path.join(workspace, "latest.log")
sessionTimestamp = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M")
sessionHash = uuid.uuid4().hex[:6]
sessionLogfile = os.path.join(workspace, f"Polaris_{sessionTimestamp}_{sessionHash}.log")

Config = {}

# =================
# Exception Classes
# =================


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


# =======
# Logging
# =======


def log(action, message, level="INFO"):
    try:
        os.makedirs(workspace, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logEntry = f"[{timestamp}] [{level.upper()}] [{action}] {message}\n"
        for target in [latestLogfile, sessionLogfile]:
            with open(target, "a", encoding="utf-8") as f:
                f.write(logEntry)
    except Exception as e:
        print(f"LogFailed: {e}")


def logException(action, error):
    try:
        errorMsg = f"{error}\n{traceback.format_exc()}"
        log(action, errorMsg, level="ERROR")
    except Exception as logE:
        print(f"LogFailed: {logE}")


# =================
# Console Utilities
# =================


def clear():
    os.system("cls")


def title():
    clear()
    console.print(Align.center(polaris))


# ==============
# File Utilities
# ==============


def delete(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
            log("FileSystem", f"Successfully deleted target file: {filename}")
            return os.path.basename(filename)
        except PermissionError:
            log("FileSystem", f"Skipped locked file: {filename}", level="DEBUG")
            return None
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
        except Exception:
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


# =================
# Process Utilities
# =================


def run_cmd(cmd, captureOutput=True, shell=False):
    try:
        if captureOutput:
            return subprocess.run(cmd, capture_output=True, text=True, shell=shell)
        return subprocess.run(cmd, shell=shell)
    except Exception as e:
        logException("Process", e)
        return None


def killprocess(processList=None):
    targets = processList or Config.get("Removals", {}).get("processes", [])
    if not targets:
        log("Process", "No processes specified to kill.", level="DEBUG")
        return []
    killed = []
    for ptk in targets:
        try:
            result = run_cmd(["taskkill", "/f", "/im", ptk])
            if result and result.returncode == 0:
                log("Process", f"Successfully killed: {ptk}")
                killed.append(ptk)
            else:
                log("Process", f"Failed to kill {ptk}: {result.stderr if result and result.stderr else 'Process not found'}", level="WARNING")
        except Exception as e:
            logException("Process", e)
    return killed


# ==============
# HTTP Utilities
# ==============


def requests_retry(url, method="GET", headers=None, retries=3, delay=2, timeout=10, stream=False, raiseOnError=True):
    lastErr = None
    response = None
    for i in range(retries):
        try:
            if method.upper() == "HEAD":
                response = requests.head(url, headers=headers, timeout=timeout, verify=True)
            else:
                response = requests.get(url, headers=headers, timeout=timeout, verify=True, stream=stream)
            if raiseOnError:
                response.raise_for_status()
            return response
        except Exception as e:
            lastErr = e
            if i < retries - 1:
                time.sleep(delay)
    if raiseOnError and lastErr:
        raise lastErr
    return response


def wait_for_connection(timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            requests.get("https://www.google.com", timeout=2)
            return True
        except Exception:
            time.sleep(1)
    return False


# ================
# System Utilities
# ================


def checkAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def get_wtPath():
    if os.name != "nt":
        return None
    wtPath = shutil.which("wt.exe") or shutil.which("wt")
    if wtPath:
        return wtPath
    defaultPath = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe")
    if os.path.exists(defaultPath):
        return defaultPath
    return None


def prefer_terminal():
    if os.name != "nt":
        return
    if "WT_SESSION" in os.environ or "--no-wt-relaunch" in sys.argv:
        return
    wtPath = get_wtPath()
    if not wtPath:
        return

    newArgs = sys.argv.copy()
    if "--no-wt-relaunch" not in newArgs:
        newArgs.append("--no-wt-relaunch")

    formattedArgs = []
    for arg in newArgs:
        if " " in arg:
            formattedArgs.append(f'"{arg}"')
        else:
            formattedArgs.append(arg)

    wtArgs = f'"{sys.executable}" {" ".join(formattedArgs)}'
    verb = "runas" if not checkAdmin() else None

    try:
        ctypes.windll.shell32.ShellExecuteW(None, verb, wtPath, wtArgs, None, 1)
        sys.exit(0)
    except Exception as e:
        log("System", f"Failed to relaunch in Windows Terminal: {e}", level="WARNING")


# ====================
# Configuration System
# ====================


def validate_config(config):
    requiredSections = [
        "Base",
        "onExit",
        "MAC",
        "Browsers",
        "Removals",
        "Roblox",
        "Install Config",
    ]
    if not isinstance(config, dict):
        return False, "Configuration is not a JSON object."
    for section in requiredSections:
        if section not in config or not isinstance(config[section], dict):
            return False, f"Missing or invalid section: '{section}'"

    boolKeys = {
        "Base": ["killProcs", "removeRobloxToken", "flushDNS"],
        "onExit": ["launchRoblox", "openLog", "restartWindows"],
        "MAC": ["spoofMAC", "allAdapters"],
        "Browsers": ["removeCookies", "removeAll"],
        "Roblox": ["removeFolders", "reinstallRoblox", "preserveSettings"],
        "Install Config": ["latestVersion", "useExecutor"],
    }
    for section, keys in boolKeys.items():
        for key in keys:
            val = config[section].get(key)
            if val is not None and not isinstance(val, bool):
                return False, f"Invalid value for '{section}.{key}': expected boolean, got {type(val).__name__}"

    return True, None


def loadconfig(configPath):
    global Config
    try:
        with open(configPath, "r", encoding="utf-8") as f:
            data = jsond.load(f)

        isValid, errorMsg = validate_config(data)
        if not isValid:
            log("Config", f"Integrity check failed: {errorMsg}", level="ERROR")
            Config = {}
            return {}

        Config = data
        return Config
    except Exception as e:
        logException("Config", e)
        return {}


def find_configFiles():
    found = []
    seen = set()
    for searchDir in [Polarislocation, workspace]:
        if not os.path.isdir(searchDir):
            continue
        for fname in os.listdir(searchDir):
            if fname.lower().endswith(".config") and fname not in seen:
                seen.add(fname)
                found.append((fname, os.path.join(searchDir, fname)))
    return found


def choose_config_file(configFiles):
    if len(configFiles) == 0:
        return None
    if len(configFiles) == 1:
        return configFiles[0][1]

    table = Table(title="Multiple config files found")
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Location", style="dim")
    for i, (fname, fpath) in enumerate(configFiles, 1):
        loc = "root" if os.path.dirname(fpath) == Polarislocation else "workspace"
        table.add_row(str(i), fname, loc)
    console.print(table)

    choice = Prompt.ask(
        f"Which config to use? [orange3](1-{len(configFiles)})[/]",
        default="1",
        show_default=False,
    )
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(configFiles):
            selected = configFiles[idx][1]
            log("Config", f"User selected config: {configFiles[idx][0]}")
            return selected
    except ValueError:
        pass
    console.print("[red]Invalid choice, using first config.[/]")
    return configFiles[0][1]


# ============
# MAC Spoofing
# ============


def gen_mac():
    macBytes = [0x02] + [secrets.randbelow(256) for _ in range(5)]
    return "".join(f"{byte:02X}" for byte in macBytes)


def list_adapters():
    try:
        adapters = []
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}",
        ) as classKey:
            for i in range(10000):
                try:
                    subkeyName = f"{i:04d}"
                    with winreg.OpenKey(classKey, subkeyName) as adapterKey:
                        try:
                            driverDesc = winreg.QueryValueEx(adapterKey, "DriverDesc")[0]
                            netCfgInstanceId = winreg.QueryValueEx(adapterKey, "NetCfgInstanceId")[0]

                            try:
                                connectionPath = f"SYSTEM\\CurrentControlSet\\Control\\Network\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{netCfgInstanceId}\\Connection"
                                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, connectionPath) as connKey:
                                    connectionName = winreg.QueryValueEx(connKey, "Name")[0]
                            except Exception:
                                connectionName = driverDesc

                            descLower = driverDesc.lower()
                            if not any(
                                word in descLower
                                for word in [
                                    "virtual",
                                    "loopback",
                                    "bluetooth",
                                    "wan miniport",
                                    "tap-windows",
                                    "pseudo",
                                    "kernel debug",
                                ]
                            ):
                                adapters.append({
                                    "id": subkeyName,
                                    "description": driverDesc,
                                    "connectionName": connectionName,
                                })
                        except (FileNotFoundError, OSError):
                            continue
                except FileNotFoundError:
                    break
        return adapters
    except Exception as e:
        logException("MAC", e)
        return []


def change_mac(adapterId, macAddress):
    try:
        path = f"SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e972-e325-11ce-bfc1-08002be10318}}\\{adapterId}"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE) as adapterKey:
            winreg.SetValueEx(adapterKey, "NetworkAddress", 0, winreg.REG_SZ, macAddress)
    except Exception as e:
        raise ProcessError(f"Registry error: {e}")


def restart_adapter(connectionName):
    actions = []

    disableResult = run_cmd(
        f'netsh interface set interface name="{connectionName}" admin=disable',
        shell=True,
    )
    if disableResult and disableResult.returncode == 0:
        actions.append(f"Interface disabled: {connectionName}")
    else:
        err = disableResult.stderr.strip() if disableResult and disableResult.stderr else "unknown error"
        log("MAC", f"Failed to disable interface '{connectionName}': {err}", level="WARN")
        actions.append(f"Failed to disable {connectionName}")

    time.sleep(2)

    enableResult = run_cmd(
        f'netsh interface set interface name="{connectionName}" admin=enable',
        shell=True,
    )
    if enableResult and enableResult.returncode == 0:
        actions.append(f"Interface enabled: {connectionName}")
    else:
        err = enableResult.stderr.strip() if enableResult and enableResult.stderr else "unknown error"
        log("MAC", f"Failed to enable interface '{connectionName}': {err}", level="WARN")
        actions.append(f"Failed to re-enable {connectionName}")
    return actions


def SpoofMAC(config=None, detailsCallback=None):
    config = config or Config
    macConfig = config.get("MAC", {})
    if not macConfig.get("spoofMAC"):
        return []

    def addAction(text):
        actions.append(text)
        if detailsCallback:
            detailsCallback(actions)

    log("MAC", "Starting verbose MAC spoofing operation")
    actions = []

    adapters = list_adapters()
    if not adapters:
        log("MAC", "No adapters found.")
        return ["No compatible hardware adapters found."]

    addAction(f"Found {len(adapters)} potential network adapters.")

    allAdapters = macConfig.get("allAdapters", True)
    targetNames = macConfig.get("adapters", [])

    for adapter in adapters:
        isTarget = (
            allAdapters
            or adapter["connectionName"] in targetNames
            or adapter["description"] in targetNames
        )

        if isTarget:
            addAction(f"Targeting adapter: {adapter['connectionName']}")
            newMac = gen_mac()
            addAction(f"  - Generating random MAC: {newMac}")
            try:
                change_mac(adapter["id"], newMac)
                log("MAC", f"Changed MAC for {adapter['connectionName']} to {newMac}")
                addAction(f"  - Registry key updated for ID {adapter['id']}")

                resetActions = restart_adapter(adapter["connectionName"])
                for ra in resetActions:
                    addAction(f"  - {ra}")

            except Exception as e:
                logException("MAC", e)
                addAction(f"  - [red]Failed to spoof {adapter['connectionName']}: {e}[/]")
        else:
            addAction(f"Skipping adapter: {adapter['connectionName']} (Not in target list)")

    return actions


# ======================
# Browser Cookie Removal
# ======================


def remove_cookies_for_host(cookieFile: str, host: str) -> int:
    if not os.path.exists(cookieFile):
        return 0
    conn = None
    try:
        conn = sqlite3.connect(cookieFile)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        tableName = (
            "cookies"
            if "cookies" in tables
            else ("moz_cookies" if "moz_cookies" in tables else None)
        )
        if not tableName:
            return 0

        cursor.execute(f"PRAGMA table_info({tableName})")
        columns = [c[1] for c in cursor.fetchall()]
        hostCol = (
            "host_key"
            if "host_key" in columns
            else ("host" if "host" in columns else None)
        )
        if not hostCol:
            return 0

        try:
            cursor.execute("VACUUM")
        except Exception as ve:
            log("Browsers", f"VACUUM failed (proceeding anyway): {ve}", level="DEBUG")

        cursor.execute(f"DELETE FROM {tableName} WHERE {hostCol} LIKE ?", (f"%{host}%",))
        conn.commit()

        deleted = cursor.rowcount
        if deleted > 0:
            log("Browsers", f"Cleaned {host} from {os.path.basename(cookieFile)} ({deleted} records)")
        return deleted
    except Exception as e:
        log("Browsers", f"Error cleaning {cookieFile}: {e}", level="WARN")
        return 0
    finally:
        if conn:
            conn.close()


def clean_browser_cookies(sites=None, removeAll=False):
    log("Browsers", "Cleaning cookies")
    cleanedBrowsers = []

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

    killedProcesses = set()

    for name, path, exe in browsers:
        for filePath in glob.glob(os.path.expandvars(path)):
            if os.path.exists(filePath):
                if exe not in killedProcesses:
                    log("Browsers", f"Terminating {name} ({exe}) to unlock cookie files...")
                    try:
                        subprocess.run(["taskkill", "/f", "/im", exe], capture_output=True)
                        killedProcesses.add(exe)
                        time.sleep(2.0)
                    except Exception as e:
                        log("Browsers", f"Failed to terminate {exe}: {e}", level="WARNING")

                for ext in ["-wal", "-shm"]:
                    sidecar = filePath + ext
                    if os.path.exists(sidecar):
                        try:
                            os.remove(sidecar)
                        except OSError:
                            pass

                if removeAll:
                    try:
                        os.remove(filePath)
                        log("Browsers", f"Deleted {filePath}")
                        if name not in cleanedBrowsers:
                            cleanedBrowsers.append(name)
                    except Exception as e:
                        log("Browsers", f"Failed to delete {filePath}: {e}", level="WARN")
                else:
                    totalDeleted = 0
                    for site in sites or ["roblox.com"]:
                        totalDeleted += remove_cookies_for_host(filePath, site)
                    if totalDeleted > 0 and name not in cleanedBrowsers:
                        cleanedBrowsers.append(name)
    return cleanedBrowsers


# ======
# Roblox
# ======


def CreateStartMenuShortcut(versionPath):
    try:
        log("Roblox", f"Attempting to create Start Menu shortcut for: {versionPath}")
        startMenuPath = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Roblox")
        os.makedirs(startMenuPath, exist_ok=True)

        shortcutPath = os.path.join(startMenuPath, "Roblox Player.lnk")
        targetExe = os.path.join(versionPath, "RobloxPlayerBeta.exe")

        if not os.path.exists(targetExe):
            log("Roblox", f"Shortcut target not found: {targetExe}", level="WARN")
            return False

        safePath = shortcutPath.replace("'", "''")
        safeTarget = targetExe.replace("'", "''")
        safeWorkdir = versionPath.replace("'", "''")
        psCommand = f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{safePath}');$s.TargetPath='{safeTarget}';$s.WorkingDirectory='{safeWorkdir}';$s.Save()"

        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-Command", psCommand],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            log("Roblox", f"Start Menu shortcut created/updated at {shortcutPath}")
            return True
        else:
            log("Roblox", f"Failed to create shortcut using PowerShell: {result.stderr}", level="ERROR")
            return False
    except Exception as e:
        logException("Roblox", e)
        return False


def RobloxSettings(config=None, statusHandler=None):
    log("Roblox", "Processing Roblox reinstallation")
    config = config or Config
    try:
        installCfg = config.get("Install Config", {})
        robloxCfg = config.get("Roblox", {})

        executor = installCfg.get("executor", "").strip()
        versionHash = ""

        if statusHandler:
            statusHandler("Resolving Roblox installation version...")

        if executor:
            log("Roblox", f"Using executor: {executor}")
            try:
                resp = requests_retry("https://weao.xyz/api/status/exploits")
                if not resp:
                    raise Exception("No response from WEAO API")
                for ex in resp.json():
                    if ex.get("title", "").lower() == executor.lower():
                        versionHash = ex.get("rbxversion", "")
                        break
            except Exception as e:
                log("Roblox", f"WEAO API failed: {e}", level="WARN")

        if not versionHash and not installCfg.get("latestVersion", False):
            versionHash = installCfg.get("versionHash", "")

        if not versionHash:
            try:
                resp = requests_retry("https://weao.xyz/api/versions/current")
                if resp:
                    versionHash = resp.json().get("Windows", {}).get("version", "")
            except Exception:
                pass

        if not versionHash:
            try:
                channel = robloxCfg.get("channel", "LIVE")
                resp = requests_retry(
                    f"https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer/channel/{channel}",
                    timeout=15,
                )
                if resp:
                    versionHash = resp.json().get("clientVersionUpload", "")
            except Exception:
                pass

        if not versionHash:
            log("Roblox", "Could not resolve version hash.", level="ERROR")
            return False

        if versionHash.lower().startswith("version-"):
            versionHash = versionHash.split("-", 1)[1]

        if not re.fullmatch(r"[0-9a-fA-F]+", versionHash):
            log("Roblox", f"Invalid version hash format: {versionHash}", level="ERROR")
            return False

        log("Roblox", f"Version hash: {versionHash}")
        targetDir = os.path.expandvars(
            r"%LOCALAPPDATA%\Roblox\Versions" + "\\" + versionHash
        )
        os.makedirs(targetDir, exist_ok=True)

        if statusHandler:
            statusHandler(
                "Calculating Roblox package sizes...",
                details=[f"Version: {versionHash}"],
            )

        channel = robloxCfg.get("channel", "LIVE")
        cdnVersion = f"version-{versionHash}"
        if channel == "LIVE":
            baseUrl = f"https://setup-aws.rbxcdn.com/{cdnVersion}"
        else:
            baseUrl = f"https://setup-aws.rbxcdn.com/channel/{channel}/{cdnVersion}"

        manifestUrl = f"{baseUrl}-rbxPkgManifest.txt"
        resp = requests_retry(manifestUrl, timeout=15, raiseOnError=False)
        if not resp or not resp.ok:
            manifestUrl = f"https://setup-aws.rbxcdn.com/channel/common/{cdnVersion}-rbxPkgManifest.txt"
            resp = requests_retry(manifestUrl, timeout=15)

        if not resp:
            log("Roblox", "Failed to fetch package manifest.", level="ERROR")
            return False

        resp.raise_for_status()
        packages = [
            line.strip()
            for line in resp.text.split("\n")
            if line.strip().endswith(".zip")
        ]

        totalSize = 0
        pkgData = []
        for pkg in packages:
            pkgUrl = f"{baseUrl}-{pkg}"
            h = requests_retry(pkgUrl, method="HEAD", timeout=15)
            size = int(h.headers.get("content-length", 0)) if h else 0
            totalSize += size
            pkgData.append((pkg, pkgUrl, size))

        if statusHandler:
            log("Roblox", f"Total size verified: {totalSize / 1024 / 1024:.2f} MB")

        extractMap = {
            "RobloxApp.zip": "",
            "redist.zip": "",
            "shaders.zip": "shaders/",
            "ssl.zip": "ssl/",
            "content-avatar.zip": "content/avatar/",
            "content-configs.zip": "content/configs/",
            "content-fonts.zip": "content/fonts/",
            "content-sky.zip": "content/sky/",
            "content-sounds.zip": "content/sounds/",
            "content-textures2.zip": "content/textures/",
            "content-models.zip": "content/models/",
            "content-platform-fonts.zip": "PlatformContent/pc/fonts/",
            "content-platform-dictionaries.zip": "PlatformContent/pc/shared_compression_dictionaries/",
            "content-terrain.zip": "PlatformContent/pc/terrain/",
            "content-textures3.zip": "PlatformContent/pc/textures/",
            "extracontent-luapackages.zip": "ExtraContent/LuaPackages/",
            "extracontent-translations.zip": "ExtraContent/translations/",
            "extracontent-models.zip": "ExtraContent/models/",
            "extracontent-textures.zip": "ExtraContent/textures/",
            "extracontent-places.zip": "ExtraContent/places/",
        }

        tempDir = os.path.expandvars(r"%temp%\robloxDownloadPolaris")
        os.makedirs(tempDir, exist_ok=True)

        title()
        console.print(
            Align.center(
                f"[bold cyan]Downloading Roblox Components ({totalSize / 1024 / 1024:.2f} MB total)[/]"
            )
        )
        print("\n")

        overallPbar = tqdm.tqdm(
            total=totalSize,
            unit="B",
            unit_scale=True,
            desc="Overall Progress",
            dynamic_ncols=True,
            colour="green",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            leave=True,
        )

        for pkg, url, size in pkgData:
            tempFile = os.path.join(tempDir, pkg)
            downloaded = False
            pkgBytes = 0
            pbar = None
            for attempt in range(3):
                try:
                    resp = requests_retry(url, stream=True, timeout=30, retries=1)
                    if not resp:
                        raise Exception("No response from server")
                    resp.raise_for_status()

                    pbar = tqdm.tqdm(
                        total=size,
                        unit="B",
                        unit_scale=True,
                        desc=f"Downloading {pkg}",
                        leave=False,
                        dynamic_ncols=True,
                        colour="cyan",
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]",
                    )

                    written = 0
                    pkgBytes = 0
                    with open(tempFile, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                written += len(chunk)
                                pkgBytes += len(chunk)
                                pbar.update(len(chunk))
                                overallPbar.update(len(chunk))
                    pbar.close()

                    if size > 0 and written != size:
                        raise DownloadError(f"Size mismatch for {pkg}: expected {size}, got {written}")

                    with zipfile.ZipFile(tempFile, "r") as z:
                        bad = z.testzip()
                        if bad is not None:
                            raise DownloadError(f"CRC failed for {pkg}: {bad}")

                    downloaded = True
                    break

                except Exception as e:
                    if pbar is not None:
                        pbar.close()
                        pbar = None
                    log("Roblox", f"Download attempt {attempt + 1}/3 failed for {pkg}: {e}", level="WARNING")
                    if os.path.exists(tempFile):
                        os.remove(tempFile)
                    if attempt < 2:
                        time.sleep(2)

            if not downloaded:
                log("Roblox", f"Failed to download {pkg} after 3 attempts", level="ERROR")
                tqdm.tqdm.write(f" \033[31mX\033[0m Failed: {pkg}")
                overallPbar.update(size - pkgBytes)
                continue

            try:
                with zipfile.ZipFile(tempFile, "r") as z:
                    root = extractMap.get(pkg, "")
                    for member in z.namelist():
                        if member.endswith("/") or member.endswith("\\"):
                            continue
                        target = os.path.join(targetDir, root, member.replace("\\", "/"))
                        if not os.path.abspath(target).startswith(os.path.abspath(targetDir)):
                            log("Roblox", f"Skipped suspicious zip member: {member}", level="WARN")
                            continue
                        os.makedirs(os.path.dirname(target), exist_ok=True)
                        with z.open(member) as s, open(target, "wb") as t:
                            shutil.copyfileobj(s, t)

                logText = f" √ Installed {pkg}"
                padding = " " * ((console.width - len(logText)) // 2)
                overallPbar.write(f"{padding}\033[32m√\033[0m Installed {pkg}")
            except Exception as e:
                log("Roblox", f"Failed to extract {pkg}: {e}", level="ERROR")
                tqdm.tqdm.write(f" \033[31mX\033[0m Failed to extract: {pkg}")
            finally:
                if os.path.exists(tempFile):
                    os.remove(tempFile)

        overallPbar.close()

        with open(os.path.join(targetDir, "AppSettings.xml"), "w") as f:
            f.write(
                '<?xml version="1.0" encoding="UTF-8"?>\n<Settings>\n    <ContentFolder>content</ContentFolder>\n    <BaseUrl>http://www.roblox.com</BaseUrl>\n</Settings>'
            )

        if statusHandler:
            statusHandler("Updating Start Menu shortcuts...")
        CreateStartMenuShortcut(targetDir)

        log("Roblox", "Installation complete.")
        return True
    except Exception as e:
        logException("Roblox", e)
        return False


# ====================
# Configuration Wizard
# ====================


def display_config_title():
    clear()
    panel = Panel(
        Align.center(polaris),
        title="[bold green]Polaris Configuration Menu[/]",
        border_style="cyan",
        padding=(0, 2, 0, 2),
        expand=False,
    )
    console.print(Align.center(panel))


def run_configurator(location=None, existingConfig=None):
    display_config_title()
    console.print("\n[bold yellow]Welcome to the Polaris Configuration Menu![/]")
    if existingConfig:
        console.print(
            "This wizard will guide you through updating your [cyan]Polaris.config[/] file.\n[dim]Existing values are shown as defaults — press Enter to keep them.[/]\n"
        )
    else:
        console.print(
            "This wizard will guide you through creating an optimal [cyan]Polaris.config[/] file.\n"
        )

    ec = existingConfig or {}
    config = {
        "Base": {},
        "onExit": {},
        "MAC": {},
        "Browsers": {},
        "Removals": {},
        "Roblox": {},
        "Install Config": {},
    }

    # 1. Base settings
    console.print(
        Panel(
            "[bold cyan]Base Environment[/]\n[dim]Core settings for cleaning the execution environment.[/]\n\n• [green]killProcs[/]: Terminate conflicting background processes.\n• [green]removeRobloxToken[/]: Purge account tracking tokens.\n• [green]flushDNS[/]: Clear network routing cache.",
            border_style="blue",
            expand=False,
        )
    )
    d = ec.get("Base", {}).get("killProcs", True)
    config["Base"]["killProcs"] = Confirm.ask(
        f"Enable killProcs? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ec.get("Base", {}).get("removeRobloxToken", True)
    config["Base"]["removeRobloxToken"] = Confirm.ask(
        f"Enable removeRobloxToken? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ec.get("Base", {}).get("flushDNS", True)
    config["Base"]["flushDNS"] = Confirm.ask(
        f"Enable flushDNS? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )

    # 2. onExit settings
    console.print(
        Panel(
            "\n[bold cyan]Automation & Exit[/]\n[dim]Define what happens after the cleanup completes.[/]\n\n• [green]launchRoblox[/]: Reopen Roblox immediately.\n• [green]openLog[/]: Show the detailed execution log.\n• [red]restartWindows[/]: Force a system reboot (Use with caution).",
            border_style="blue",
            expand=False,
        )
    )
    d = ec.get("onExit", {}).get("launchRoblox", True)
    config["onExit"]["launchRoblox"] = Confirm.ask(
        f"Launch Roblox on exit? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ec.get("onExit", {}).get("openLog", True)
    config["onExit"]["openLog"] = Confirm.ask(
        f"Open log on exit? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ec.get("onExit", {}).get("restartWindows", False)
    config["onExit"]["restartWindows"] = Confirm.ask(
        f"Restart Windows on exit? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )

    # 3. MAC settings
    console.print(
        Panel(
            "\n[bold cyan]Identity Protection[/]\n[dim]Hardware identification spoofing.[/]\n\n• [bold red]spoofMAC[/]: Highly recommended to avoid hardware-linked bans.\n• [green]allAdapters[/]: Apply spoofing to every available network interface.",
            border_style="blue",
            expand=False,
        )
    )
    d = ec.get("MAC", {}).get("spoofMAC", True)
    config["MAC"]["spoofMAC"] = Confirm.ask(
        f"Enable MAC spoofing? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ec.get("MAC", {}).get("allAdapters", True)
    config["MAC"]["allAdapters"] = Confirm.ask(
        f"Apply to all adapters? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    config["MAC"]["adapters"] = ec.get("MAC", {}).get("adapters", [])
    if not config["MAC"]["allAdapters"] and config["MAC"]["spoofMAC"]:
        current = ", ".join(config["MAC"]["adapters"]) if config["MAC"]["adapters"] else ""
        adaptersStr = Prompt.ask(
            f"Enter comma-separated list of adapters to spoof [orange3](Default: '{current}')[/]",
            default=current,
            show_default=False,
        )
        if adaptersStr.strip():
            config["MAC"]["adapters"] = [a.strip() for a in adaptersStr.split(",")]

    # 4. Browsers settings
    console.print(
        Panel(
            "\n[bold cyan]Browser Cleanup[/]\n[dim]Manage web-based tracking data.[/]\n\n• [yellow]removeCookies[/]: Target specific domains.\n• [red]removeAll[/]: Complete cookie wipeout.\n• [green]removedSites[/]: Targeted domains (Default: roblox.com).",
            border_style="blue",
            expand=False,
        )
    )
    d = ec.get("Browsers", {}).get("removeCookies", True)
    config["Browsers"]["removeCookies"] = Confirm.ask(
        f"Remove cookies? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ec.get("Browsers", {}).get("removeAll", False)
    config["Browsers"]["removeAll"] = Confirm.ask(
        f"Remove ALL browser cookies? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ", ".join(ec.get("Browsers", {}).get("removedSites", ["roblox.com"]))
    sitesStr = Prompt.ask(
        f"Sites to remove cookies for (comma-separated) [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    config["Browsers"]["removedSites"] = [
        s.strip() for s in sitesStr.split(",") if s.strip()
    ]

    # 5. Removals settings
    console.print(
        Panel(
            "\n[bold cyan]System Paths[/]\n[dim]Configures default targets for file and folder deletion.[/]",
            border_style="blue",
            expand=False,
        )
    )
    config["Removals"] = {
        "files": ["%appdata%\\local\\Roblox\\Localstorage\\RobloxCookies.dat"],
        "folders": ["%temp%", "%localappdata%\\Roblox", "%appdata%\\Roblox"],
        "processes": ["RobloxPlayerBeta.exe", "RobloxPlayerLauncher.exe"],
    }
    console.print("[dim]→ Initialized default removal targets.[/]")

    # 6. Roblox settings
    console.print(
        Panel(
            "\n[bold cyan]Roblox Integrity[/]\n[dim]Deep cleanup and reinstallation settings.[/]\n\n• [green]removeFolders[/]: Purge local application data.\n• [green]reinstallRoblox[/]: Clean re-download of components.\n• [green]preserveSettings[/]: Keep [white]GlobalBasicSettings_13.xml[/].\n\n[bold red]⚠  Reinstalling uses up to ~150MB+ of disk space.[/]",
            border_style="red",
            expand=False,
        )
    )
    d = ec.get("Roblox", {}).get("removeFolders", True)
    config["Roblox"]["removeFolders"] = Confirm.ask(
        f"Remove Roblox folders? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ec.get("Roblox", {}).get("reinstallRoblox", True)
    config["Roblox"]["reinstallRoblox"] = Confirm.ask(
        f"Reinstall Roblox after cleanup? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ec.get("Roblox", {}).get("preserveSettings", True)
    config["Roblox"]["preserveSettings"] = Confirm.ask(
        f"Preserve Roblox settings? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )

    # 7. Install Config
    console.print(
        Panel(
            "\n[bold cyan]Version & Compatibility[/]\n[dim]Select the specific build of Roblox to install.[/]\n\n• [yellow]latestVersion[/]: Always pull newest build.\n• [green]useExecutor[/]: Auto-resolve build based on your software.",
            border_style="blue",
            expand=False,
        )
    )
    d = ec.get("Install Config", {}).get("latestVersion", False)
    config["Install Config"]["latestVersion"] = Confirm.ask(
        f"Force latest Roblox version? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ec.get("Install Config", {}).get("versionHash", "")
    config["Install Config"]["versionHash"] = Prompt.ask(
        f"Enter specific version hash to install (leave blank if none) [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    d = ec.get("Install Config", {}).get("useExecutor", True)
    config["Install Config"]["useExecutor"] = Confirm.ask(
        f"Use a specific executor? [orange3](Default: '{d}')[/]",
        default=d,
        show_default=False,
    )
    if config["Install Config"]["useExecutor"]:
        d = ec.get("Install Config", {}).get("executor", "Potassium")
        while True:
            executorName = Prompt.ask(
                f"Enter executor name (type 'list' to see options) [orange3](Default: '{d}')[/]",
                default=d,
                show_default=False,
            )
            if executorName.strip().lower() == "list":
                try:
                    with console.status("[bold green]Fetching executors from WEAO API..."):
                        response = requests_retry(
                            "https://weao.xyz/api/status/exploits",
                            headers={"User-Agent": "WEAO-3PService"},
                        )
                        data = response.json() if response else []

                    table = Table(title="Supported Executors from WEAO")
                    table.add_column("Name", style="cyan", no_wrap=True)
                    table.add_column("Version", style="magenta")
                    table.add_column("Updated Date")

                    now = datetime.datetime.now(timezone.utc)
                    for exploit in data:
                        exType = str(exploit.get("extype", "")).lower()
                        if exType != "wexecutor":
                            continue

                        dateStr = exploit.get("updatedDate", "Unknown")
                        dateDisplay = dateStr.split(" at")[0]

                        color = "green"
                        try:
                            dt = datetime.datetime.strptime(
                                dateStr, "%m/%d/%Y at %I:%M %p UTC"
                            ).replace(tzinfo=timezone.utc)
                            diff = now - dt
                            if diff > timedelta(days=30):
                                color = "red"
                            elif diff > timedelta(days=14):
                                color = "orange3"
                        except Exception as e:
                            logException("Config", e)

                        table.add_row(
                            exploit.get("title", "Unknown"),
                            exploit.get("version", "N/A"),
                            f"[{color}]{dateDisplay}[/]",
                        )

                    console.print(table)
                    console.print(
                        "[dim italic]Note: Green dates indicate recent updates and do not guarantee the executor is currently working.[/]"
                    )
                except Exception as e:
                    console.print(f"[bold red]Failed to fetch from WEAO API:[/] {e}")
            else:
                config["Install Config"]["executor"] = executorName.strip()
                break
    else:
        config["Install Config"]["executor"] = ""

    saveDir = location if location else Polarislocation
    configPath = os.path.join(saveDir, "Polaris.config")
    try:
        with open(configPath, "w", encoding="utf-8") as f:
            jsond.dump(config, f, indent=4)
        console.print(f"[bold green]Success![/] Saved configuration to [bold white]{configPath}[/]")
    except Exception as e:
        console.print(f"[bold red]Failed to save configuration:[/] {e}")


# ==============
# Initialization
# ==============


def Initialize():
    log("System", f"Admin: {checkAdmin()} | Executable: {sys.executable} | Args: {sys.argv}")
    try:
        with open(latestLogfile, "w", encoding="utf-8") as _:
            pass
    except Exception as e:
        logException("System", e)

    if not checkAdmin():
        log("System", "Requesting UAC")
        newArgs = (
            sys.argv + ["--direct-run"] if "--direct-run" not in sys.argv else sys.argv
        )

        wtPath = get_wtPath()
        if wtPath and "--no-wt-relaunch" not in newArgs:
            newArgs.append("--no-wt-relaunch")
            formattedArgs = []
            for arg in newArgs:
                if " " in arg:
                    formattedArgs.append(f'"{arg}"')
                else:
                    formattedArgs.append(arg)
            wtArgs = f'"{sys.executable}" {" ".join(formattedArgs)}'
            ctypes.windll.shell32.ShellExecuteW(None, "runas", wtPath, wtArgs, None, 1)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(newArgs), None, 1)
        sys.exit(0)

    if not os.path.exists(workspace):
        try:
            os.makedirs(workspace)
            log("System", f"Created workspace at {workspace}")
        except Exception as e:
            logException("System", e)

    configFiles = find_configFiles()
    final_configPath = choose_config_file(configFiles)

    if not final_configPath or not loadconfig(final_configPath):
        log("Config", "Config missing or invalid, launching configurator", level="INFO")
        run_configurator(Polarislocation)
        final_configPath = os.path.join(Polarislocation, "Polaris.config")
        loadconfig(final_configPath)

    return final_configPath


# =========
# Run Logic
# =========


def autoClose():
    log("Close", "Automatically Closing")
    title()
    timer = 15
    starttime = time.time()

    print("\n")

    while time.time() - starttime < timer:
        timeLeft = int(timer - (time.time() - starttime))
        maxLen = len(f" Exiting in {timer}s... (Press Any Key to Exit.)")
        padding = " " * ((console.width - maxLen) // 2)
        output = f"{padding}[cyan]Exiting in[/] [bold]{timeLeft}s[/]... [dim](Press [bold]Any Key[/] to Exit.)[/]"
        console.print(output.ljust(console.width), end="\r")
        if msvcrt.kbhit():
            msvcrt.getch()
            break
        time.sleep(0.1)
    print("\n")

    if Config.get("onExit", {}).get("launchRoblox"):
        try:
            robloxPath = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions")
            if os.path.exists(robloxPath):
                versions = [
                    d
                    for d in os.listdir(robloxPath)
                    if os.path.isdir(os.path.join(robloxPath, d))
                ]
                for v in versions:
                    exePath = os.path.join(robloxPath, v, "RobloxPlayerBeta.exe")
                    if os.path.exists(exePath):
                        subprocess.Popen([exePath])
                        log("Exit", f"Launched Roblox from {exePath}")
                        break
        except Exception as e:
            logException("Exit", e)

    if Config.get("onExit", {}).get("openLog"):
        try:
            os.startfile(latestLogfile)
        except Exception as e:
            logException("Exit", e)

    if Config.get("onExit", {}).get("restartWindows"):
        try:
            log("Exit", "System restart initiated by user config")
            os.system("shutdown /r /t 5")
        except Exception as e:
            logException("Exit", e)

    sys.exit()


def run():
    statusHistory = []

    def render_status():
        title()
        for item in statusHistory:
            color = "green" if item["level"] == "info" else "red"
            bullet = "√" if item["level"] == "info" else "X"
            console.print(f" [[{color}]{bullet}[/]] {item['msg']}")
            for detail in item["details"]:
                console.print(f"    [dim]- {detail}[/]")

    def update_status(msg, level="info", details=None):
        if details is None:
            details = []
        statusHistory.append({"msg": msg, "level": level, "details": details})
        render_status()

    try:
        log("System", f"Admin: {checkAdmin()} | Executable: {sys.executable} | Args: {sys.argv}")
        configPath = Initialize()
        if not loadconfig(configPath):
            autoClose()
            return
    except Exception as e:
        logException("Run", e)
        update_status(f"Startup failed: {e}", level="error")
        autoClose()
        return
    log("System", "Run sequence started.")

    base = Config.get("Base", {})
    roblox = Config.get("Roblox", {})
    removals = Config.get("Removals", {})
    mac = Config.get("MAC", {})
    browsers = Config.get("Browsers", {})

    # Settings Preservation Backup
    settingsFile = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\GlobalBasicSettings_13.xml")
    settingsBackup = None

    if roblox.get("preserveSettings") and os.path.exists(settingsFile):
        try:
            with open(settingsFile, "rb") as f:
                settingsBackup = f.read()
            log("Roblox", "Backed up GlobalBasicSettings_13.xml for preservation.")
        except Exception as e:
            logException("Roblox", e)

    if base.get("killProcs"):
        update_status("Killing background processes...")
        killed = killprocess()
        if killed:
            statusHistory[-1]["details"] = [f"Terminated: {p}" for p in killed]
            render_status()

    if roblox.get("removeFolders"):
        update_status("Cleaning selected directories...")
        removed = []
        for folder in removals.get("folders", []):
            res = removeFolder(os.path.expandvars(folder))
            if res:
                removed.append(res)
        if removed:
            statusHistory[-1]["details"] = [f"Removed: {f}" for f in removed]
            render_status()

    if base.get("removeRobloxToken"):
        update_status("Removing account tokens...")
        deleted = []
        for file in removals.get("files", []):
            res = delete(os.path.expandvars(file))
            if res:
                deleted.append(res)
        if deleted:
            statusHistory[-1]["details"] = [f"Deleted: {f}" for f in deleted]
            render_status()

    # Restore preserved settings after folder/file removals
    if settingsBackup:
        try:
            os.makedirs(os.path.dirname(settingsFile), exist_ok=True)
            with open(settingsFile, "wb") as f:
                f.write(settingsBackup)
            log("Roblox", "Restored GlobalBasicSettings_13.xml")
            update_status("Restored preserved Roblox settings.")
        except Exception as e:
            logException("Roblox", e)

    if browsers.get("removeCookies") or browsers.get("removeAll"):
        update_status("Cleaning browser cookies...")
        cleaned = clean_browser_cookies(
            browsers.get("removedSites"), browsers.get("removeAll")
        )
        if cleaned:
            statusHistory[-1]["details"] = [f"Cleaned: {b}" for b in cleaned]
            render_status()

    if base.get("flushDNS"):
        update_status("Flushing DNS cache...")
        res = subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
        if res.returncode == 0:
            statusHistory[-1]["details"] = ["DNS cache purged successfully."]
            render_status()

    if mac.get("spoofMAC"):
        update_status("Spoofing network MAC address...")

        def sync_details(actions):
            statusHistory[-1]["details"] = actions
            render_status()

        SpoofMAC(detailsCallback=sync_details)

        with console.status("[bold cyan]Waiting for network connection...", spinner="dots"):
            if wait_for_connection(timeout=45):
                update_status("Network connection restored.")
                statusHistory[-1]["details"] = ["Ping successful!"]
            else:
                update_status("Network connection timeout.", level="error")
                statusHistory[-1]["details"] = ["System might be offline."]
            render_status()

    if roblox.get("reinstallRoblox"):
        update_status("Reinstalling Roblox...")
        res = RobloxSettings(statusHandler=update_status)
        if not res:
            if statusHistory:
                statusHistory[-1]["level"] = "error"

    update_status("Sequence completed.")
    autoClose()


# ===========
# Entry Point
# ===========

if __name__ == "__main__":
    try:
        prefer_terminal()

        if "--direct-run" in sys.argv:
            run()
            sys.exit(0)

        configFiles = find_configFiles()
        if not configFiles:
            run_configurator()
            if Confirm.ask("Run now?"):
                run()
        else:
            cfgPath = choose_config_file(configFiles)
            choice = "run"
            if not cfgPath or not loadconfig(cfgPath):
                run_configurator()
                if Confirm.ask("Run now?"):
                    run()
            else:
                display_config_title()

                timer = 10
                start = time.time()

                console.print(
                    Align.center(
                        r"[bold]Action?[/] [cyan]\[Press 'R' to Run or 'C' to Configure.][/]"
                    )
                )

                while time.time() - start < timer:
                    timeLeft = int(timer - (time.time() - start))
                    maxLen = len(f" -- Auto-starting in {timer}s... (Press Esc to Cancel) --")
                    padding = " " * ((console.width - maxLen) // 2)
                    output = f"{padding}[cyan]-- Auto-starting in[/] [bold]{timeLeft}s[/]... [dim](Press [bold yellow]Esc[/] to Cancel)[/] [cyan]--[/]"
                    console.print(output.ljust(console.width), end="\r")

                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        if key == b"\x1b":
                            console.print("\n\n [bold red]Operation cancelled by user.[/]\n")
                            sys.exit(0)

                        keyLower = key.lower()
                        if keyLower == b"c":
                            choice = "configure"
                        else:
                            choice = "run"
                        break
                    time.sleep(0.1)

            print("\n")

            if choice == "configure":
                run_configurator(existingConfig=Config)
                if Confirm.ask(
                    "Run now? [orange3](Default: 'True')[/]",
                    default=True,
                    show_default=False,
                ):
                    run()
            else:
                run()
    except KeyboardInterrupt:
        sys.exit(0)
