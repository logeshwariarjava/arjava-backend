# Arjava Backend Setup

## Quick Start

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Add to Windows hosts file (Run as Administrator):
   - Open `C:\Windows\System32\drivers\etc\hosts` in notepad as administrator
   - Add this line: `127.0.0.1 arjava.localhost`

3. Run the server:
   ```
   python main.py
   ```
   OR
   ```
   run.bat
   ```

4. Access your API:
   - API Docs: http://arjava.localhost:8000/docs
   - API: http://arjava.localhost:8000/
   - Health Check: http://arjava.localhost:8000/health

## Manual Hosts File Setup
1. Press Win+R, type `notepad` and press Ctrl+Shift+Enter (run as admin)
2. Open: C:\Windows\System32\drivers\etc\hosts
3. Add line: `127.0.0.1 arjava.localhost`
4. Save and close
