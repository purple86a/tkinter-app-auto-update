# Tkinter Auto-Update Framework

A **reusable auto-update framework** for Tkinter desktop applications with GitHub releases integration and MSI installer packaging. I implemented this project for fun and to explore many frameworks and tools hence the amount of releases (●'◡'●). Feel free to use it as a starting point for your own projects! You can also reach me by email if you have any suggestions or questions. Happy coding! (/≧▽≦)/

## 🎯 Overview

This framework demonstrates enterprise-grade auto-update capabilities that can be easily integrated into any Tkinter application. Users receive seamless, automatic updates through an elegant splash screen interface, with downloads tracked in real-time and installation handled automatically via Windows MSI installers.

### Key Features

- ✅ **Automatic Update Detection** — Checks GitHub releases on startup
- ✅ **Beautiful Update UI** — Professional splash screen with progress tracking
- ✅ **MSI Installer Packaging** — Windows Installer with Start Menu & Desktop shortcuts
- ✅ **GitHub Actions CI/CD** — Automated build pipeline with version management
- ✅ **Semantic Versioning** — Built-in version bumping with Bump2Version
- ✅ **Zero-Configuration Updates** — Users get updates with a single click
- ✅ **Threaded Downloads** — Non-blocking UI during update process
- ✅ **Production Ready** — Complete with changelog, credits, and documentation

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.7+** — Primary language
- **Tkinter** — GUI framework (no external dependencies)
- **PyInstaller** — Executable packaging and bundling
- **Requests** — HTTP client for GitHub API communication
- **Packaging** — Semantic version comparison

### Build & Deployment
- **WiX Toolset 6.x** — MSI installer creation
- **GitHub Actions** — Automated CI/CD pipeline
- **Bump2Version** — Automated semantic versioning
- **Pillow** — Icon format conversion (PNG → ICO)

### Infrastructure
- **GitHub Releases API** — Update distribution platform
- **Windows Installer XML** — Enterprise-grade installer packaging
- **Markdown** — Documentation and release notes

## 🚀 Why This Project is Reusable

This framework is designed from the ground up to be **easily integrated** into any Tkinter application:

### 1. **Modular Architecture**
- Self-contained `AutoUpdater` class handles all update logic
- Standalone `UpdateSplashScreen` component for UI
- Clean separation between update framework and demo application
- Zero dependencies on the sample application code

### 2. **Configuration-Based Design**
Simply update three variables to integrate into your app:
```python
GITHUB_OWNER = "your-username"    # Your GitHub username
GITHUB_REPO = "your-repo-name"    # Your repository name
APP_NAME = "YourApp"              # Your application name
```

### 3. **Drop-In Integration**
The update framework requires **minimal changes** to existing code:
- Copy two classes (`AutoUpdater` and `UpdateSplashScreen`)
- Wrap your main window initialization with the update callback
- Configure your GitHub repository settings
- Done!

### 4. **Customizable Components**
- Modify splash screen colors, fonts, and layout
- Adjust update check frequency and behavior
- Customize MSI installer branding and install paths
- Extend with logging, notifications, or analytics

### 5. **Comprehensive Documentation**
- Step-by-step integration guide included
- Troubleshooting section for common issues
- Complete CI/CD workflow examples
- Version management best practices

## 🏆 Production Standards

This project adheres to professional development practices suitable for enterprise deployment:

### Version Management
- **Semantic Versioning** following [SemVer 2.0.0](https://semver.org/)
- **Automated Version Bumping** via Bump2Version configuration
- **Changelog Maintenance** following [Keep a Changelog](https://keepachangelog.com/) format
- **Git Tag Automation** for release tracking

See [`VERSIONING.md`](VERSIONING.md) for complete version management workflow.

### Continuous Integration/Deployment
- **Automated Builds** triggered by Git tags
- **Multi-Stage Pipeline** with dependency caching
- **Artifact Verification** before release
- **Automatic Release Creation** with extracted changelog notes
- **Platform-Specific Builds** optimized for Windows x64

GitHub Actions workflow: [`.github/workflows/build-release.yml`](.github/workflows/build-release.yml)

### Code Quality
- **Type-Safe Version Comparison** using the `packaging` library
- **Error Handling** with graceful fallbacks
- **Threading** for non-blocking network operations
- **Resource Management** with PyInstaller bundle support
- **Debug Logging** for troubleshooting production issues

### User Experience
- **Non-Intrusive Updates** with skip option
- **Progress Feedback** with real-time download tracking
- **Automatic Restart** after successful installation
- **Release Notes Display** rendered from Markdown
- **Professional UI Design** with custom styling

### Installer Quality
- **MSI Packaging** following Windows Installer standards
- **Silent Upgrade Support** with downgrade protection
- **Registry Integration** for proper Windows integration
- **Shortcut Management** for Start Menu and Desktop
- **Launch After Install** option for improved UX
- **Unique Product GUIDs** for version tracking

### Documentation
- **Comprehensive README** with integration guide
- **Inline Code Comments** explaining complex logic
- **Changelog Tracking** for all releases
- **Credits Attribution** for third-party assets
- **Versioning Guide** for maintainers

## 📋 Quick Start

### For Users (Installing the Application)

1. Download the latest `MyApp.msi` from [Releases](../../releases)
2. Run the installer and follow the prompts
3. Launch the application from Start Menu or Desktop shortcut
4. Updates will be checked automatically on each launch

### For Developers (Integrating the Framework)

#### **Step 1: Copy the Update Framework**

Copy these classes from `main.py` into your application:
- `AutoUpdater` (lines 44-141)
- `UpdateSplashScreen` (lines 144-419)
- Helper functions: `get_resource_path()`, `get_install_dir()`, `get_installed_exe_path()`

#### **Step 2: Configure Your Application**

Update the configuration constants:
```python
GITHUB_OWNER = "your-username"
GITHUB_REPO = "your-repo-name"
APP_NAME = "YourApp"
__version__ = "1.0.0"
```

#### **Step 3: Modify Your Main Entry Point**

Wrap your existing Tkinter initialization:
```python
def main():
    root = tk.Tk()
    root.withdraw()  # Hide until update check completes
    
    def show_main_app():
        root.deiconify()
        YourMainApplicationClass(root)
    
    # Show update splash screen first
    UpdateSplashScreen(root, __version__, show_main_app)
    root.mainloop()

if __name__ == "__main__":
    main()
```

#### **Step 4: Set Up GitHub Actions**

1. Copy `.github/workflows/build-release.yml` to your repository
2. Copy `installer.wxs` and customize with your app details
3. Create `.bumpversion.cfg` for version management
4. Add dependencies to `requirements.txt`

#### **Step 5: Create Your First Release**

```bash
# Update CHANGELOG.md with your changes
# Then bump the version and push
bumpversion patch  # or minor, or major
git push --follow-tags
```

GitHub Actions will automatically build and create the release!

## 📁 Project Structure

```
tkinter-app-auto-update/
├── .github/
│   └── workflows/
│       └── build-release.yml    # CI/CD pipeline
├── main.py                       # Complete demo application with updater
├── installer.wxs                 # WiX installer definition
├── app_icon.png                  # Application icon (source)
├── requirements.txt              # Python dependencies
├── .bumpversion.cfg             # Version management configuration
├── CHANGELOG.md                 # Release history
├── VERSIONING.md                # Version management guide
├── CREDITS.md                   # Third-party attributions
└── README.md                    # This file
```

## 🔧 Customization Guide

### Branding the Installer

Edit `installer.wxs`:
```xml
<Package Name="YourApp" 
         Manufacturer="YourCompany"
         ...>
```

### Changing Update UI Appearance

Modify the `UpdateSplashScreen` class:
```python
# Colors
main_frame = tk.Frame(self, bg='#your-color', ...)

# Window size
self.geometry("600x400")  # width x height

# Fonts
self.title_label = tk.Label(..., font=('YourFont', 18, 'bold'))
```

### Adjusting Build Output

Update `.github/workflows/build-release.yml`:
```yaml
# Change executable name
pyinstaller ... --name "YourApp" main.py

# Add custom resources
pyinstaller ... --add-data "resources;resources" ...

# Set custom icon
pyinstaller ... --icon="your_icon.ico" ...
```

## 📖 Release Workflow

### Prerequisites
You need to have done the following:
- Create a virtual environment and activate it using the following:
```bash
python -m venv venv
venv\Scripts\activate
```
- Install bump2version using the following:
```bash
pip install bump2version
```

### 1. **Make Changes**
Update your code and test locally

### 2. **Update Changelog**
Add your changes to `CHANGELOG.md` under `[Unreleased]`

### 3. **Bump Version**
```bash
# For bug fixes (1.0.0 → 1.0.1)
bumpversion patch

# For new features (1.0.0 → 1.1.0)
bumpversion minor

# For breaking changes (1.0.0 → 2.0.0)
bumpversion major
```

This automatically:
- Updates `__version__` in `main.py`
- Creates a git commit
- Creates a git tag

### 4. **Push to GitHub**
```bash
git push --follow-tags
```

### 5. **Automated Build**
GitHub Actions will:
- Build the executable with PyInstaller
- Create the MSI installer with WiX
- Extract release notes from CHANGELOG.md
- Create a GitHub release with the MSI attached

### 6. **User Updates**
Users running older versions will see the update dialog on their next launch!

## 🧪 Testing Updates Locally

### Build Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Convert icon
python -c "from PIL import Image; img = Image.open('app_icon.png'); img.save('app_icon.ico')"

# Build with PyInstaller
pyinstaller --onefile --noconsole --add-data "app_icon.png;." --icon="app_icon.ico" --name "main" main.py

# Build MSI (requires WiX Toolset 6.x)
wix build -arch x64 -d Version=1.0.0 -o dist/MyApp.msi installer.wxs
```

### Test Update Flow
1. Create a test release on GitHub with version `v1.1.0`
2. Upload a test MSI to the release
3. Run your local build (version `1.0.0`)
4. The update dialog should appear automatically

## 🛡️ Security Considerations

- ✅ **HTTPS-Only Communication** with GitHub API
- ✅ **No Hardcoded Credentials** in source code
- ✅ **Secure Download** via authenticated GitHub releases
- ⚠️ **Consider Code Signing** for production deployments to avoid Windows SmartScreen warnings
- ⚠️ **Checksum Verification** can be added for enhanced security

## 🐛 Troubleshooting

### Update Check Fails
**Cause:** Network issues or incorrect repository configuration  
**Solution:** Verify `GITHUB_OWNER` and `GITHUB_REPO` are correct and repository is public

### MSI Build Fails
**Cause:** Missing WiX Toolset or incorrect version  
**Solution:** Install WiX 6.x: `dotnet tool install --global wix`

### Icon Not Showing
**Cause:** Icon not bundled or path incorrect  
**Solution:** Ensure `--add-data "app_icon.png;."` in PyInstaller command and `get_resource_path()` usage

### Application Won't Start After Update
**Cause:** Antivirus blocking or permission issues  
**Solution:** Run as Administrator once, or add exception to antivirus

For more detailed troubleshooting, see the inline comments in `main.py`.

## 🎨 Credits

This project uses third-party assets and open-source software:

- See [`CREDITS.md`](CREDITS.md) for attribution of icons and artwork
- Built with open-source tools: Python, Tkinter, PyInstaller, WiX Toolset
- Implemented to expirement and explore current frameworks

## 📄 License

This is a demonstration project. Feel free to use and modify the auto-update framework for your own applications. Please maintain attribution for third-party assets as documented in [`CREDITS.md`](CREDITS.md) if you are going to use the icon of the application in your own application.

## 🤝 Contributing & Versioning

For developers looking to contribute or fork this project:

- **Versioning Guide:** See [`VERSIONING.md`](VERSIONING.md) for version management workflow
- **Changelog Format:** Follow [Keep a Changelog](https://keepachangelog.com/) guidelines  
- **Version Scheme:** We use [Semantic Versioning](https://semver.org/)

### Quick Version Bump Reference

```bash
bumpversion patch   # Bug fixes (1.0.0 → 1.0.1)
bumpversion minor   # New features (1.0.0 → 1.1.0)
bumpversion major   # Breaking changes (1.0.0 → 2.0.0)
git push --follow-tags
```

---

**Made with ❤️ for the Python/Tkinter community** • [Report Issues](../../issues) • [View Releases](../../releases)
