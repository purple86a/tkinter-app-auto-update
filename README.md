# Auto-Updater Setup Guide

## Step 1: Install Required Dependencies

Add these to your `requirements.txt`:
```
requests
packaging
```

Install them:
```bash
pip install requests packaging
```

## Step 2: Integrate the Updater into Your App

1. Copy the `AutoUpdater`, `UpdaterDialog`, and `check_for_updates_on_startup` classes into your main application file (or a separate `updater.py` module)

2. In your main application file, update these values:
```python
APP_VERSION = "1.0.0"  # Your current version
GITHUB_OWNER = "yourusername"  # Your GitHub username
GITHUB_REPO = "your-repo-name"  # Your repo name
```

3. After creating your Tkinter root window, add this line:
```python
check_for_updates_on_startup(root, APP_VERSION, GITHUB_OWNER, GITHUB_REPO)
```

**Example:**
```python
if __name__ == "__main__":
    APP_VERSION = "1.0.0"
    GITHUB_OWNER = "john-doe"
    GITHUB_REPO = "my-awesome-app"
    
    root = tk.Tk()
    root.title(f"My App v{APP_VERSION}")
    
    # Your app code here...
    
    # Add this line before mainloop
    check_for_updates_on_startup(root, APP_VERSION, GITHUB_OWNER, GITHUB_REPO)
    
    root.mainloop()
```

## Step 3: Set Up GitHub Actions Workflow

1. Create `.github/workflows/release.yml` in your repository
2. Copy the workflow content from the artifact
3. Customize these values in the workflow:
   - `--name "MyApp"` → Your app name
   - `main.py` → Your main Python file
   - `MyApp.exe` → Your desired exe name
   - Add `--icon=icon.ico` if you have an icon file

## Step 4: Create Your First Release

1. **Update your version** in your code:
   ```python
   APP_VERSION = "1.0.0"
   ```

2. **Commit and push** your changes:
   ```bash
   git add .
   git commit -m "Release v1.0.0"
   git push
   ```

3. **Create and push a tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

4. GitHub Actions will automatically:
   - Build your exe
   - Create a release
   - Upload the exe to the release

## Step 5: Test the Updater

1. Create a new release with a higher version number (e.g., v1.1.0)
2. Run your v1.0.0 exe
3. It should detect the update and prompt you

## Step 6: Future Releases

For each new release:

1. Update `APP_VERSION` in your code:
   ```python
   APP_VERSION = "1.1.0"  # New version
   ```

2. Commit changes:
   ```bash
   git add .
   git commit -m "Release v1.1.0"
   git push
   ```

3. Create and push tag:
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

4. Edit the release notes on GitHub (optional but recommended)

## Troubleshooting

### Update check not working
- Verify your `GITHUB_OWNER` and `GITHUB_REPO` are correct
- Check that your releases are public
- Ensure tag format is `vX.Y.Z` (e.g., v1.0.0)

### Exe not building
- Check the PyInstaller command in the workflow
- Make sure all dependencies are in `requirements.txt`
- Check GitHub Actions logs for errors

### Update fails to install
- Ensure the exe name matches between builds
- Check Windows permissions
- Try running the app as administrator

## Optional Enhancements

### Add an icon
In the workflow, add:
```yaml
--icon=icon.ico
```

### Silent updates
Modify the `check_for_updates_on_startup` to auto-update without dialog

### Update check button
Add a manual "Check for Updates" button in your app:
```python
def manual_update_check():
    updater = AutoUpdater(APP_VERSION, GITHUB_OWNER, GITHUB_REPO)
    update_info = updater.check_for_updates()
    
    if update_info and update_info['available']:
        UpdaterDialog(root, updater, update_info)
    else:
        messagebox.showinfo("No Updates", "You're running the latest version!")
```

### Skip versions
Store the last skipped version and don't prompt again until a newer version is available