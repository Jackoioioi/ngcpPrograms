# NGCP Ground Control Infrastructure - Setup Guide

## Prerequisites
- Python 3.12+
- Git
- XBee module plugged in via USB
- Windows OS (instructions below are Windows-specific)

---

## Step 1 — Clone the Repository
> ⚠️ You MUST use `--recurse-submodules` or the `lib/` folder will be empty and all imports will fail.

```
git clone --recurse-submodules https://github.com/Jackoioioi/ngcpPrograms.git
```

If you already cloned without the flag, run this to fix it:
```
git submodule update --init --recursive
```

---

## Step 2 — Navigate into the Project
```
cd ngcpPrograms
```

---

## Step 3 — Create and Activate a Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear at the start of your terminal line.

---

## Step 4 — Install Dependencies
```
cd gcs-infrastructure
pip install -r requirements.txt
```

---

## Step 5 — Find Your COM Port
1. Plug in your XBee module via USB
2. Open **Device Manager** on Windows
3. Expand **Ports (COM & LPT)**
4. Note your COM port number (e.g. `COM6`, `COM8`)

---

## Step 6 — Configure Your Script
Open whichever script matches your role and update the `PORT` variable and MAC address to match your XBee module.

### If you are on the GCS Computer → `GCSTest.py`
```python
PORT = "COM6"  # change to your COM port
PacketLibrary.SetVehicleMACAddress(Vehicle.MRA, "YOUR_VEHICLE_MAC_HERE")
```

### If you are on the Vehicle Computer → `import sys.py`
```python
PORT = "COM8"  # change to your COM port
PacketLibrary.SetGCSMACAddress("YOUR_GCS_MAC_HERE")
```

> The MAC address is printed on the back of your XBee module (16 character hex, e.g. `0013A20040F8063C`)

---

## Step 7 — Run the Scripts

> ⚠️ Always start the **GCS computer first**, then the Vehicle computer.

### GCS Computer:
```
python ".\TestScripts\GCSTest.py"
```

### Vehicle Computer:
```
python ".\TestScripts\import sys.py"
```

---

## Troubleshooting

**`lib/` folder is empty / import errors**
```
git submodule update --init --recursive
```

**XBee not opening on COM port**
- Check Device Manager to confirm the correct COM port
- Make sure no other program (e.g. XCTU) is using the same port
- Try unplugging and replugging the XBee

**Telemetry timing out**
- Make sure both scripts are running at the same time
- Double check MAC addresses match the physical XBee modules
- Make sure GCS script was started first

**`pip install` failing**
- Make sure your virtual environment is activated (`(venv)` should appear in terminal)
- Make sure you are inside the `gcs-infrastructure/` folder when running `pip install`
