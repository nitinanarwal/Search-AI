# Business Search App - macOS Setup Guide

This guide will help you set up the Business Search App on macOS from a Windows backup.

## Prerequisites

### 1. Install Homebrew (Package Manager)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python 3.8+
```bash
brew install python@3.11
```

### 3. Install Node.js 16+
```bash
brew install node
```

### 4. Install Git
```bash
brew install git
```

### 5. Verify Installations
```bash
python3 --version
node --version
npm --version
git --version
```

## Project Setup

### Step 1: Clone or Extract the Project
If you have the project on GitHub:
```bash
git clone <your-repository-url>
cd business-search-app
```

If you have a ZIP file:
```bash
# Extract the ZIP file
unzip business-search-app.zip
cd business-search-app
```

### Step 2: Set Up the Backend

1. **Navigate to the backend directory:**
```bash
cd backend
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the backend server:**
```bash
python server.py
```

The backend will start on `http://localhost:5000`

### Step 3: Set Up the Frontend

1. **Open a new terminal and navigate to the frontend directory:**
```bash
cd frontend
```

2. **Install Node.js dependencies:**
```bash
npm install
```

3. **Create environment file:**
```bash
echo "VITE_API_URL=http://localhost:5000" > .env
```

4. **Start the development server:**
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

## macOS-Specific Notes

### File Permissions
If you encounter permission issues:
```bash
chmod +x backend/server.py
```

### Port Issues
If port 5000 is already in use (common on macOS):
```bash
# Check what's using port 5000
lsof -i :5000

# Kill the process if needed
sudo kill -9 <PID>
```

### Python Path Issues
If you have multiple Python versions:
```bash
# Use python3 explicitly
python3 -m venv venv
python3 server.py
```

### Node.js Issues
If npm install fails:
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install
```

## Troubleshooting

### Common macOS Issues

1. **"Permission denied" errors:**
   ```bash
   sudo chown -R $(whoami) /usr/local/lib/node_modules
   ```

2. **Python virtual environment not activating:**
   ```bash
   source venv/bin/activate
   ```

3. **Port already in use:**
   - Backend: Change port in `server.py` line 245
   - Frontend: Vite will automatically use the next available port

4. **CORS errors:**
   - Make sure the backend is running on port 5000
   - Check that the frontend environment variable is set correctly

5. **Search returns no results:**
   - Check the browser console for errors
   - Verify the backend is running and accessible
   - Try different search terms

### Debug Mode

To run in debug mode:

**Backend:**
```bash
cd backend
source venv/bin/activate
python server.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Check the browser console (Cmd+Option+I) for any JavaScript errors.

## Production Deployment on macOS

### Backend Deployment

1. **Install production dependencies:**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 server:app
   ```

### Frontend Deployment

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Serve the dist folder:**
   ```bash
   # Install a simple HTTP server
   npm install -g serve
   
   # Serve the built files
   serve -s dist -l 3000
   ```

## Useful macOS Commands

### Check System Information
```bash
# Check macOS version
sw_vers

# Check available disk space
df -h

# Check memory usage
top -l 1 | head -n 10
```

### Network Commands
```bash
# Check if ports are open
netstat -an | grep LISTEN

# Test connectivity
ping localhost
```

### Process Management
```bash
# Find processes by name
ps aux | grep python
ps aux | grep node

# Kill processes
kill -9 <PID>
```

## Next Steps

1. **Open your browser** and go to `http://localhost:5173`
2. **Test the application** with various search queries
3. **Customize the data** in `backend/data/nonprofits.json`
4. **Deploy to production** when ready

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Look at the browser console for error messages
3. Check the backend terminal for Python errors
4. Create an issue with detailed error information and macOS version
