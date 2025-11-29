# Python Installation Guide for Windows

## Quick Installation Steps

### Method 1: Official Python Installer (Recommended)

1. **Download Python**
   - Go to https://www.python.org/downloads/
   - Click "Download Python 3.x.x" (latest version, 3.8 or higher)
   - The installer will download automatically

2. **Run the Installer**
   - Double-click the downloaded `.exe` file
   - **IMPORTANT**: Check the box "Add Python to PATH" at the bottom
   - Click "Install Now" (or "Customize installation" for advanced options)
   - Wait for installation to complete

3. **Verify Installation**
   - Open Command Prompt (Win + R, type `cmd`, press Enter)
   - Type: `python --version`
   - You should see: `Python 3.x.x`
   - Type: `pip --version`
   - You should see: `pip x.x.x from ...`

### Method 2: Microsoft Store (Alternative)

1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Install"
4. Wait for installation
5. Verify: Open Command Prompt and type `python --version`

### Method 3: Using Chocolatey (For Advanced Users)

If you have Chocolatey package manager:

```powershell
choco install python
```

---

## Post-Installation Setup

### 1. Verify Python is in PATH

Open Command Prompt and run:
```cmd
python --version
pip --version
```

If you get "Python is not recognized", you need to add Python to PATH:
1. Search for "Environment Variables" in Windows
2. Click "Edit the system environment variables"
3. Click "Environment Variables"
4. Under "System variables", find "Path" and click "Edit"
5. Click "New" and add:
   - `C:\Python3x` (or wherever Python is installed)
   - `C:\Python3x\Scripts`
6. Click OK on all dialogs
7. Restart Command Prompt

### 2. Install Project Dependencies

Navigate to the Bharat project directory:
```cmd
cd C:\Users\scar\Downloads\Bharat
```

Install dependencies:
```cmd
pip install -r requirements.txt
```

### 3. Verify Installation

Test that everything works:
```cmd
python -c "import fastapi; print('FastAPI installed successfully')"
python -c "import pydantic; print('Pydantic installed successfully')"
python -c "import yaml; print('PyYAML installed successfully')"
```

---

## Troubleshooting

### Python Not Found

**Problem**: `python` command not recognized

**Solutions**:
1. Reinstall Python and check "Add Python to PATH"
2. Manually add Python to PATH (see above)
3. Use `py` command instead: `py --version`
4. Find Python location: Usually `C:\Users\YourName\AppData\Local\Programs\Python\`

### pip Not Found

**Problem**: `pip` command not recognized

**Solutions**:
1. Use `python -m pip` instead of `pip`
2. Reinstall Python with pip included
3. Install pip manually: `python -m ensurepip --upgrade`

### Permission Errors

**Problem**: Permission denied when installing packages

**Solutions**:
1. Run Command Prompt as Administrator
2. Use user installation: `pip install --user -r requirements.txt`
3. Check antivirus isn't blocking

### Multiple Python Versions

**Problem**: Multiple Python versions installed

**Solutions**:
1. Use `py -3.11` for specific version
2. Use `python3` if available
3. Check which Python: `where python`

---

## Quick Test

After installation, test the project:

```cmd
cd C:\Users\scar\Downloads\Bharat
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Then open: http://localhost:8000/docs

---

## Python Version Requirements

- **Minimum**: Python 3.8
- **Recommended**: Python 3.10 or 3.11
- **Latest**: Python 3.12

Check your version:
```cmd
python --version
```

---

## Alternative: Using Python Virtual Environment (Recommended for Development)

### Create Virtual Environment

```cmd
cd C:\Users\scar\Downloads\Bharat
python -m venv venv
```

### Activate Virtual Environment

```cmd
venv\Scripts\activate
```

You'll see `(venv)` in your prompt.

### Install Dependencies

```cmd
pip install -r requirements.txt
```

### Deactivate (when done)

```cmd
deactivate
```

---

## Next Steps

After Python is installed:

1. ✅ Verify installation: `python --version`
2. ✅ Install dependencies: `pip install -r requirements.txt`
3. ✅ Test the server: `python main.py`
4. ✅ Run tests: `pytest`
5. ✅ Read QUICKSTART.md for usage

---

## Need Help?

- Python Official Docs: https://docs.python.org/3/
- Python Windows FAQ: https://docs.python.org/3/using/windows.html
- Stack Overflow: Search for Python installation issues

