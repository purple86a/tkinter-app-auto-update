# Auto-Updater Setup Guide

Complete guide for adding auto-update functionality to your Tkinter application with GitHub releases.

## Overview

This auto-updater provides:
- ✅ Automatic update checking on app startup
- ✅ Beautiful splash screen with update UI
- ✅ Download progress tracking
- ✅ Automatic installation and restart
- ✅ Works directly with GitHub releases (no complex setup)
- ✅ Main app stays hidden during updates

## Prerequisites

- Python 3.7+
- GitHub repository with Actions enabled
- PyInstaller for building executables

## Step 1: Install Required Dependencies

Add these to your `requirements.txt`:
```txt
requests
packaging
pyinstaller
```

Install them:
```bash
pip install requests packaging pyinstaller
```

## Step 2: Test with Example Application

Before integrating into your main app, test with the provided example:

1. **Download the complete example** from the "Complete Example Application with Updater" artifact

2. **Update configuration** at the bottom of the file:
```python
APP_VERSION = "1.0.0"  # Your current version
GITHUB_OWNER = "your-github-username"  # Your GitHub username
GITHUB_REPO = "your-repo-name"  # Your repo name
```

3. **Run it** to see how it works:
```bash
python main.py
```

You should see:
- Update splash screen appears first
- "Checking for Updates..." message
- Then either update dialog or main app opens

## Step 3: Set Up GitHub Actions Workflow

1. **Create the workflow file** in your repository:
```
.github/workflows/release.yml
```

2. **Copy the workflow** from the "GitHub Release Workflow" artifact

3. **Customize these values** in the workflow:
```yaml
pyinstaller --onefile --windowed --name "MyApp" main.py
```
Change:
- `"MyApp"` → Your desired executable name
- `main.py` → Your main Python file
- Add `--icon=icon.ico` if you have an icon

4. **Update the asset paths**:
```yaml
asset_path: ./dist/MyApp.exe  # Match your exe name
asset_name: MyApp.exe  # Match your exe name
```

## Step 4: Integrate into Your Application

### Option A: Copy the Classes

Copy these classes from the example into your main application:
- `AutoUpdater`
- `UpdateSplashScreen`

### Option B: Create a Separate Module

Create `updater.py` with the classes and import them:
```python
from updater import UpdateSplashScreen
```

### Update Your Main Code

Modify your main application entry point:

**Before (typical Tkinter app):**
```python
if __name__ == "__main__":
    root = tk.Tk()
    MyApp(root)
    root.mainloop()
```

**After (with updater):**
```python
def main():
    APP_VERSION = "1.0.0"
    GITHUB_OWNER = "your-username"
    GITHUB_REPO = "your-repo"
    
    root = tk.Tk()
    root.withdraw()  # Hide main window initially
    
    def show_main_app():
        root.deiconify()  # Show main window
        MyApp(root)  # Your application class
    
    # Show update splash screen first
    UpdateSplashScreen(
        root,
        APP_VERSION,
        GITHUB_OWNER,
        GITHUB_REPO,
        show_main_app
    )
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

## Step 5: Create Your First Release

### Build Locally (Optional Test)

```bash
pyinstaller --onefile --windowed --name "MyApp" main.py
```

Your exe will be in `dist/MyApp.exe`

### Create GitHub Release

1. **Commit your changes**:
```bash
git add .
git commit -m "Add auto-updater functionality"
git push
```

2. **Create and push version tag**:
```bash
git tag v1.0.0
git push origin v1.0.0
```

3. **GitHub Actions will automatically**:
   - Build your application
   - Create a release named "Release v1.0.0"
   - Upload the exe as a release asset

4. **Check GitHub Actions**:
   - Go to your repository → "Actions" tab
   - Watch the workflow run
   - When complete, go to "Releases" to see your first release

## Step 6: Test the Auto-Updater

1. **Download v1.0.0** exe from GitHub releases
2. **Run it** - it should check for updates and open normally (no updates available)

3. **Create a new version**:
   - Update `APP_VERSION = "1.1.0"` in your code
   - Make some changes to your app
   - Commit and create tag:
   ```bash
   git add .
   git commit -m "Release v1.1.0 - Added new features"
   git tag v1.1.0
   git push origin v1.1.0
   ```

4. **Run the old v1.0.0** exe again:
   - Update splash should appear
   - Should detect v1.1.0 is available
   - Click "Update Now" to test automatic update
   - App should download, install, and restart with new version

## Step 7: Future Releases

For each new release, follow this workflow:

1. **Update version** in code:
```python
APP_VERSION = "1.2.0"  # Increment version
```

2. **Make your changes** and test locally

3. **Commit changes**:
```bash
git add .
git commit -m "Release v1.2.0 - Bug fixes and improvements"
git push
```

4. **Create and push tag**:
```bash
git tag v1.2.0
git push origin v1.2.0
```

5. **Edit release notes** (optional but recommended):
   - Go to GitHub → Releases
   - Edit the auto-generated release
   - Add detailed release notes about changes

## Version Numbering

Use semantic versioning (MAJOR.MINOR.PATCH):
- `v1.0.0` → Initial release
- `v1.0.1` → Bug fixes
- `v1.1.0` → New features (backwards compatible)
- `v2.0.0` → Major changes (breaking changes)

## Troubleshooting

### Update Check Not Working

**Problem**: App doesn't detect updates

**Solutions**:
- Verify `GITHUB_OWNER` and `GITHUB_REPO` are correct
- Ensure your repository is **public** (or add authentication for private repos)
- Check that releases are not set as "Draft"
- Verify tag format is exactly `vX.Y.Z` (e.g., `v1.0.0`)
- Check internet connection

**Debug**:
```python
# Add this temporarily to see error messages
import sys
sys.stdout = open('debug.log', 'w')
sys.stderr = sys.stdout
```

### Exe Not Building in GitHub Actions

**Problem**: Workflow fails during build step

**Solutions**:
- Check the Actions logs for specific error
- Ensure all dependencies are in `requirements.txt`
- Verify the PyInstaller command matches your file structure
- Check that your code doesn't have syntax errors

**Common fixes**:
```yaml
# If you have additional data files:
pyinstaller --onefile --windowed --add-data "data;data" --name "MyApp" main.py

# If you have multiple Python files:
pyinstaller --onefile --windowed --name "MyApp" main.py --hidden-import=mymodule
```

### Update Installation Fails

**Problem**: Update downloads but doesn't install

**Solutions**:
- Run the application as **Administrator**
- Check Windows antivirus isn't blocking the update
- Ensure exe names match between versions
- Check Windows permissions on the installation folder

### Download Progress Not Showing

**Problem**: Progress bar stays at 0%

**Solutions**:
- Check that the GitHub release has the exe asset attached
- Verify the exe filename matches exactly (case-sensitive)
- Check file size isn't 0 bytes in the release

### App Crashes on Startup

**Problem**: App closes immediately after starting

**Solutions**:
- Run from command line to see error messages:
```bash
MyApp.exe
```
- Check all dependencies are included by PyInstaller
- Add missing modules with `--hidden-import`

## Optional Enhancements

### Add Application Icon

1. Create or obtain an `.ico` file
2. Place it in your project root
3. Update PyInstaller command:
```yaml
pyinstaller --onefile --windowed --icon=icon.ico --name "MyApp" main.py
```

### Customize Update Dialog

Modify the `UpdateSplashScreen` class to change:
- Colors: Edit `bg` and `fg` parameters
- Fonts: Change `font=('Arial', 16, 'bold')`
- Window size: Modify `geometry("500x350")`
- Border style: Change or remove `overrideredirect(True)`

### Add Manual Update Check Button

Add a button in your app to manually check for updates:

```python
def manual_update_check(self):
    """Manual update check from menu or button"""
    updater = AutoUpdater(APP_VERSION, GITHUB_OWNER, GITHUB_REPO)
    update_info = updater.check_for_updates()
    
    if update_info is None:
        messagebox.showerror("Error", "Failed to check for updates.")
    elif update_info['available']:
        # Show update dialog
        UpdateSplashScreen(
            self.root,
            APP_VERSION,
            GITHUB_OWNER,
            GITHUB_REPO,
            lambda: None  # No callback needed for manual check
        )
    else:
        messagebox.showinfo("No Updates", "You're running the latest version!")

# Add to menu:
menu.add_command(label="Check for Updates", command=self.manual_update_check)
```

### Silent Auto-Updates

For silent updates without user interaction, modify `handle_update_check_result`:

```python
def handle_update_check_result(self):
    if self.update_info and self.update_info['available']:
        # Auto-update without showing dialog
        self.start_update()
    else:
        self.skip_update()
```

### Update Notifications

Add a system notification when update is available:

```python
# Windows notification
from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast(
    "Update Available",
    f"Version {update_info['version']} is ready to install!",
    duration=10
)
```

### Skip Version Feature

Allow users to skip a specific version:

```python
import json

def save_skipped_version(version):
    with open('config.json', 'w') as f:
        json.dump({'skipped_version': version}, f)

def get_skipped_version():
    try:
        with open('config.json', 'r') as f:
            return json.load(f).get('skipped_version')
    except:
        return None

# In UpdateSplashScreen, add a "Skip This Version" button
```

### Beta/Pre-release Channel

Check for pre-releases:

```python
# In check_for_updates(), use this endpoint instead:
self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"

# Then filter for pre-releases:
for release in response.json():
    if release.get('prerelease'):
        # Process pre-release
```

### Update Log

Keep a log of updates:

```python
import datetime

def log_update(from_version, to_version):
    with open('update_log.txt', 'a') as f:
        f.write(f"{datetime.datetime.now()}: Updated from {from_version} to {to_version}\n")
```

## Security Considerations

- ✅ Always verify download integrity (consider adding checksum verification)
- ✅ Use HTTPS for all GitHub API calls (already implemented)
- ✅ Don't store GitHub tokens in the application code
- ✅ Consider code signing your executables for Windows SmartScreen
- ✅ For private repositories, implement secure authentication

## Best Practices

1. **Always test updates** on a separate machine before releasing
2. **Write clear release notes** for each version
3. **Use semantic versioning** consistently
4. **Keep a changelog** in your repository
5. **Test the rollback process** (what if update fails?)
6. **Monitor GitHub Actions** for build failures
7. **Keep dependencies updated** in requirements.txt

## Support

If you encounter issues:

1. Check the GitHub Actions logs for build errors
2. Test locally with PyInstaller before creating a release
3. Verify your GitHub repository settings
4. Check that releases are public (not draft)
5. Review the troubleshooting section above

## Example Folder Structure

```
your-repo/
├── .github/
│   └── workflows/
│       └── release.yml
├── main.py                 # Your main application with updater
├── requirements.txt        # Python dependencies
├── icon.ico               # Application icon (optional)
├── README.md              # This file
└── .gitignore
```

## Sample .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
env/
venv/

# PyInstaller
build/
dist/
*.spec

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
debug.log
```

---

**You're all set!** Your application now has professional auto-update functionality. Users will always have the latest version with minimal effort.

