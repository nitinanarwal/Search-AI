# Git Ignore Reference

This document explains what files are being ignored in this project and why.

## Files/Folders Being Ignored

### Python Files
- `__pycache__/` - Python bytecode cache files
- `*.pyc`, `*.pyo` - Compiled Python files
- `.venv/`, `venv/` - Virtual environment directories
- `*.egg-info/` - Python package metadata
- `.pytest_cache/` - pytest cache directory

### Node.js Files
- `node_modules/` - npm/yarn dependencies (can be reinstalled)
- `npm-debug.log*` - npm debug logs
- `yarn-debug.log*` - yarn debug logs
- `dist/`, `build/` - Build output directories
- `.env.local`, `.env.development.local` - Local environment files

### IDE/Editor Files
- `.vscode/` - VS Code settings
- `.idea/` - PyCharm/IntelliJ settings
- `*.swp`, `*.swo` - Vim swap files
- `*~` - Backup files

### OS Files
- `.DS_Store` - macOS system files
- `Thumbs.db` - Windows thumbnail cache
- `ehthumbs.db` - Windows thumbnail cache
- `._*` - macOS resource fork files

### Project-Specific
- `export-project/` - Export directory (temporary)
- `.tools/` - Development tools directory
- `*.db`, `*.sqlite3` - Database files
- `*.log` - Log files

## Why These Files Are Ignored

1. **Dependencies** (`node_modules/`, `.venv/`) - Can be large and are platform-specific
2. **Build artifacts** (`dist/`, `build/`, `__pycache__/`) - Generated files that can be recreated
3. **Environment files** (`.env*`) - May contain sensitive information
4. **IDE files** - Personal preferences that shouldn't be shared
5. **OS files** - System-specific files that aren't needed
6. **Logs and caches** - Temporary files that change frequently

## What IS Included

- Source code (`.py`, `.jsx`, `.js`, `.css`, `.html`)
- Configuration files (`package.json`, `requirements.txt`, `vite.config.js`)
- Documentation (`README.md`, `SETUP_MACOS.md`)
- Data files (`backend/data/nonprofits.json`)
- Git configuration (`.gitignore`)

## Checking What Will Be Committed

Before committing, you can check what files will be included:

```bash
# See what files are staged
git status

# See what files are ignored
git status --ignored

# See what would be committed
git diff --cached --name-only
```

## Adding Files That Are Ignored

If you need to include a file that's being ignored:

1. **Temporarily**: Use `git add -f filename`
2. **Permanently**: Add an exception to `.gitignore`:
   ```
   # Ignore all .env files except
   .env
   !.env.example
   ```

## Best Practices

1. **Never commit sensitive data** (API keys, passwords, etc.)
2. **Keep dependencies in package files** (`requirements.txt`, `package.json`)
3. **Document setup steps** so others can recreate the environment
4. **Use environment variables** for configuration
5. **Test the setup** on a clean machine before committing
