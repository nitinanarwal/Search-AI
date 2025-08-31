# Business Search App

A full-stack web application for searching and discovering businesses/nonprofits with semantic search capabilities.

## Features

- 🔍 **Semantic Search**: Advanced search using natural language processing
- 📍 **Geographic Filtering**: Search by location and radius
- 🏷️ **Category Filtering**: Filter by business categories and causes
- ⭐ **Smart Ranking**: Relevance-based result ranking
- 🎨 **Modern UI**: Responsive design with Tailwind CSS
- ⚡ **Fast Performance**: Vector search with FAISS

## Project Structure

```
business-search-app/
├── backend/                 # Python Flask API
│   ├── data/               # Sample data files
│   ├── server.py           # Main API server
│   ├── nlu.py              # Natural language processing
│   ├── vector_search.py    # Vector search implementation
│   ├── geo.py              # Geographic utilities
│   ├── ranking.py          # Result ranking logic
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/                # React source code
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
└── README.md               # This file
```

## Prerequisites

Before running this application, make sure you have the following installed:

### Required Software

#### Windows
1. **Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Node.js 16+**
   - Download from [nodejs.org](https://nodejs.org/)
   - This includes npm (Node Package Manager)

3. **Git** (optional, for version control)
   - Download from [git-scm.com](https://git-scm.com/)

#### macOS
1. **Install Homebrew** (package manager):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Python 3.8+**:
   ```bash
   brew install python@3.11
   # Add Python to PATH (if not already done)
   echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Node.js 16+**:
   ```bash
   brew install node
   ```

4. **Git**:
   ```bash
   brew install git
   ```

5. **Verify installations**:
   ```bash
   python3 --version
   node --version
   npm --version
   git --version
   ```

#### Linux (Ubuntu/Debian)
1. **Python 3.8+**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Node.js 16+**:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

3. **Git**:
   ```bash
   sudo apt install git
   ```

## Installation & Setup

### Step 1: Clone or Download the Project

If you have Git:
```bash
git clone <repository-url>
cd business-search-app
```

Or download and extract the ZIP file to a folder named `business-search-app`.

### Step 2: Set Up the Backend

1. **Navigate to the backend directory:**
```bash
cd backend
```

2. **Create a virtual environment (recommended):**
   ```bash
   # On Windows:
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend server:**
   ```bash
   # On Windows:
   python server.py
   
   # On macOS/Linux:
   python3 server.py
   ```

   The backend will start on `http://localhost:5000`

   **Note for macOS users**: If you encounter permission issues, run:
   ```bash
   chmod +x server.py
   ```

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
   Create a file named `.env` in the frontend directory with:
   ```bash
   # On Windows:
   echo VITE_API_URL=http://localhost:5000 > .env
   
   # On macOS/Linux:
   echo "VITE_API_URL=http://localhost:5000" > .env
   ```

   **Alternative for macOS**: You can also create the file manually:
   ```bash
   # Create and edit the .env file
   touch .env
   echo "VITE_API_URL=http://localhost:5000" >> .env
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will start on `http://localhost:5173`

## Usage

1. **Open your browser** and go to `http://localhost:5173`
2. **Type a search query** in the search bar (e.g., "pizza", "housing", "education")
3. **View results** - the app will display relevant businesses/nonprofits
4. **Use filters** - you can filter by location, category, or other criteria

## API Endpoints

The backend provides the following API endpoints:

- `GET /health` - Health check
- `GET /search?query=<search_term>` - Search for businesses
- `POST /api/search` - Advanced search with filters
- `GET /api/businesses` - Get all businesses
- `GET /api/businesses/<id>` - Get specific business details

## Troubleshooting

### Common Issues

1. **Port already in use:**
   - Backend: Change port in `server.py` line 245
   - Frontend: Vite will automatically use the next available port

2. **Python dependencies not found:**
   - Make sure you're in the virtual environment
   - Run `pip install -r requirements.txt` again

3. **Node modules not found:**
   - Run `npm install` in the frontend directory

4. **CORS errors:**
   - Make sure the backend is running on port 5000
   - Check that the frontend environment variable is set correctly

5. **Search returns no results:**
   - Check the browser console for errors
   - Verify the backend is running and accessible
   - Try different search terms

### Platform-Specific Issues

#### Windows
- **Python not found**: Make sure Python is added to PATH during installation
- **Permission errors**: Run Command Prompt as Administrator

#### macOS
- **Port 5000 in use**: Common on macOS, use `lsof -i :5000` to check and `sudo kill -9 <PID>` to kill the process
- **Permission denied**: Use `sudo chown -R $(whoami) /usr/local/lib/node_modules` or `sudo chown -R $(whoami) /opt/homebrew/lib/node_modules`
- **Python path issues**: Use `python3` explicitly instead of `python`
- **Homebrew path issues**: Add `/opt/homebrew/bin` to your PATH in `~/.zshrc`
- **Virtual environment not activating**: Make sure to use `source venv/bin/activate` (not `activate venv`)

#### Linux
- **Package not found**: Update package lists with `sudo apt update`
- **Permission issues**: Use `sudo` for system-wide installations

### Debug Mode

To run in debug mode:

**Backend:**
```bash
cd backend
python server.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Check the browser console (F12) for any JavaScript errors.

## Production Deployment

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

2. **Serve the dist folder** with any static file server (nginx, Apache, etc.)

## Data

The application uses sample nonprofit data stored in `backend/data/nonprofits.json`. You can replace this with your own data following the same JSON structure.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Cross-Platform Setup

For detailed setup instructions on different platforms:

- **macOS**: See [SETUP_MACOS.md](SETUP_MACOS.md) for comprehensive macOS setup guide with troubleshooting
- **Linux**: Follow the Linux installation commands in the Prerequisites section above
- **Windows**: Follow the Windows installation instructions in the Prerequisites section above

### Quick macOS Setup Checklist

If you're setting up on macOS, here's a quick checklist:

- [ ] Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- [ ] Install Python: `brew install python@3.11`
- [ ] Install Node.js: `brew install node`
- [ ] Install Git: `brew install git`
- [ ] Verify installations: `python3 --version && node --version && npm --version`
- [ ] Clone/extract the project
- [ ] Set up backend: `cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- [ ] Set up frontend: `cd frontend && npm install && echo "VITE_API_URL=http://localhost:5000" > .env`
- [ ] Start backend: `python3 server.py` (in backend directory with venv activated)
- [ ] Start frontend: `npm run dev` (in frontend directory)
- [ ] Open browser to `http://localhost:5173`

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Look at the browser console for error messages
3. Check the backend terminal for Python errors
4. Create an issue with detailed error information and your operating system version
