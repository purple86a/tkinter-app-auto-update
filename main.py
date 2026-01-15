import tkinter as tk
from tkinter import ttk, messagebox
import requests
import subprocess
import sys
import os
import tempfile
import shutil
from packaging import version
import threading

GITHUB_OWNER = "purple86a"
GITHUB_REPO = "tkinter-app-auto-update"
APP_NAME = "MyApp"  # Change this to your app name
__version__ = "1.1.12"

def get_install_dir():
    """Get the fixed install directory for the app."""
    return os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), APP_NAME)

def get_installed_exe_path():
    """Get the path where the exe should be installed."""
    return os.path.join(get_install_dir(), f"{APP_NAME}.exe")

def is_installed():
    """Check if the app is running from the fixed install location."""
    install_dir = get_install_dir()
    installed_exe = get_installed_exe_path()
    current_exe = sys.executable
    
    # Check if we're already running from the install location
    return os.path.normcase(os.path.normpath(current_exe)) == os.path.normcase(os.path.normpath(installed_exe))

class AutoUpdater:
    def __init__(self, current_version):
        self.current_version = current_version
        self.api_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
        
    def check_for_updates(self):
        """Check if a new version is available."""
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data['tag_name'].lstrip('v')
            
            if version.parse(latest_version) > version.parse(self.current_version):
                return {
                    'available': True,
                    'version': latest_version,
                    'download_url': self._get_exe_download_url(release_data),
                    'release_notes': release_data.get('body', 'No release notes available.')
                }
            
            return {'available': False}
            
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return None
    
    def _get_exe_download_url(self, release_data):
        """Extract the .msi download URL from release assets."""
        for asset in release_data.get('assets', []):
            if asset['name'].endswith('.msi'):
                return asset['browser_download_url']
        return None
    
    def download_update(self, download_url, progress_callback=None):
        """Download the update file."""
        try:
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, f"update_{GITHUB_REPO}.msi")
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            progress_callback(downloaded, total_size)
            
            return temp_file
            
        except Exception as e:
            print(f"Error downloading update: {e}")
            return None
    
    def install_update(self, installer_path, original_exe_path=None):
        """Install the update and restart the application."""
        try:
            # DEBUG: Write debug info to a log file
            debug_log = os.path.join(tempfile.gettempdir(), 'update_debug.txt')
            with open(debug_log, 'w') as f:
                f.write(f"=== Update Debug Log (MSI Mode) ===\n")
                f.write(f"installer_path: {installer_path}\n")
                f.write(f"installer exists: {os.path.exists(installer_path)}\n")
                f.write(f"current PID: {os.getpid()}\n")

            # Command to run the MSI
            # /i: install
            # /passive: show progress bar but no user interaction required (unattended)
            # /norestart: don't restart computer automatically
            msi_cmd = f'msiexec /i "{installer_path}" /passive /norestart'
            
            # Create a batch script to run the MSI and exit
            batch_script = os.path.join(tempfile.gettempdir(), 'run_update.bat')
            with open(batch_script, 'w') as f:
                f.write('@echo off\n')
                f.write(f'echo Starting MSI install >> "{debug_log}"\n')
                # Wait briefly to ensure the python process closes
                f.write('timeout /t 2 /nobreak > nul\n')
                f.write(f'{msi_cmd}\n')
                f.write(f'echo MSI started >> "{debug_log}"\n')
            
            # Start the batch script detached
            subprocess.Popen(['cmd', '/c', batch_script], 
                           creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Exit this application immediately so the installer can overwrite files
            sys.exit(0)
            
        except Exception as e:
            print(f"Error installing update: {e}")
            return False


class UpdateSplashScreen(tk.Toplevel):
    """Splash screen that checks for updates before showing main app."""
    
    def __init__(self, parent, app_version, on_complete_callback, original_exe_path=None):
        super().__init__(parent)
        
        self.updater = AutoUpdater(app_version)
        self.on_complete_callback = on_complete_callback
        self.update_info = None
        self.original_exe_path = original_exe_path
        
        # Window setup
        self.title("Checking for Updates")
        self.geometry("500x350")
        self.resizable(False, False)
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (250)
        y = (self.winfo_screenheight() // 2) - (175)
        self.geometry(f"+{x}+{y}")
        
        # Remove window decorations for splash effect
        self.overrideredirect(True)
        
        # Main frame with border
        main_frame = tk.Frame(self, bg='#2c3e50', padx=2, pady=2)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = tk.Label(
            content_frame,
            text="Checking for Updates...",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        self.title_label.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(
            content_frame,
            text="Please wait...",
            font=('Arial', 10),
            bg='white',
            fg='#666'
        )
        self.status_label.pack(pady=5)
        
        # Progress bar (hidden initially)
        self.progress_frame = tk.Frame(content_frame, bg='white')
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=('Arial', 9),
            bg='white',
            fg='#666'
        )
        self.progress_label.pack()
        
        # Release notes (hidden initially)
        self.notes_frame = tk.Frame(content_frame, bg='white')
        notes_label = tk.Label(
            self.notes_frame,
            text="What's New:",
            font=('Arial', 10, 'bold'),
            bg='white',
            anchor='w'
        )
        notes_label.pack(fill=tk.X, padx=20)
        
        self.notes_text = tk.Text(
            self.notes_frame,
            wrap=tk.WORD,
            height=8,
            font=('Arial', 9),
            bg='#f5f5f5',
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.notes_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Buttons (hidden initially)
        self.button_frame = tk.Frame(content_frame, bg='white')
        
        self.update_button = tk.Button(
            self.button_frame,
            text="Update Now",
            command=self.start_update,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor='hand2'
        )
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        self.skip_button = tk.Button(
            self.button_frame,
            text="Skip Update",
            command=self.skip_update,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10),
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor='hand2'
        )
        self.skip_button.pack(side=tk.LEFT, padx=5)
        
        # Start checking for updates
        self.after(500, self.check_updates)
    
    def check_updates(self):
        """Check for updates in background thread."""
        def check():
            self.update_info = self.updater.check_for_updates()
            self.after(0, self.handle_update_check_result)
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
    
    def handle_update_check_result(self):
        """Handle the result of update check."""
        if self.update_info is None:
            # Error checking updates - skip and open app
            self.status_label.config(text="Unable to check for updates")
            self.after(1500, self.skip_update)
            return
        
        if not self.update_info['available']:
            # No updates available - open app
            self.status_label.config(text="You're up to date!")
            self.after(1000, self.skip_update)
            return
        
        # Update available - show update UI
        self.show_update_available()
    
    def show_update_available(self):
        """Show the update available screen."""
        self.title_label.config(
            text=f"Update Available: v{self.update_info['version']}"
        )
        self.status_label.config(text="A new version is ready to install")
        
        # Show release notes
        self.notes_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.notes_text.delete('1.0', tk.END)
        self.notes_text.insert('1.0', self.update_info['release_notes'])
        self.notes_text.config(state='disabled')
        
        # Show buttons
        self.button_frame.pack(pady=15)
    
    def start_update(self):
        """Start the update process."""
        # Hide buttons
        self.button_frame.pack_forget()
        self.notes_frame.pack_forget()
        
        # Show progress
        self.title_label.config(text="Downloading Update...")
        self.status_label.config(text="Please wait, do not close the application")
        self.progress_frame.pack(pady=20)
        
        # Disable skip
        self.skip_button.config(state='disabled')
        
        # Download in background
        def download():
            def progress(downloaded, total):
                percent = (downloaded / total * 100) if total > 0 else 0
                self.after(0, lambda: self.update_progress(downloaded, total, percent))
            
            download_url = self.update_info['download_url']
            if not download_url:
                self.after(0, lambda: messagebox.showerror(
                    "Error", "No download URL found in release."
                ))
                self.after(0, self.skip_update)
                return
            
            installer_path = self.updater.download_update(download_url, progress)
            
            if installer_path:
                self.after(0, lambda: self.install_update(installer_path))
            else:
                self.after(0, lambda: messagebox.showerror(
                    "Error", "Failed to download update."
                ))
                self.after(0, self.skip_update)
        
        thread = threading.Thread(target=download, daemon=True)
        thread.start()
    
    def update_progress(self, downloaded, total, percent):
        """Update the progress bar."""
        self.progress_bar['value'] = percent
        
        # Convert bytes to MB
        downloaded_mb = downloaded / (1024 * 1024)
        total_mb = total / (1024 * 1024)
        
        self.progress_label.config(
            text=f"{downloaded_mb:.1f} MB / {total_mb:.1f} MB ({percent:.1f}%)"
        )
    
    def install_update(self, installer_path):
        """Install the downloaded update."""
        self.title_label.config(text="Installing Update...")
        self.progress_label.config(text="Application will restart shortly...")
        self.updater.install_update(installer_path, self.original_exe_path)
    
    def skip_update(self):
        """Skip update and open main application."""
        self.destroy()
        self.on_complete_callback()


class MainApplication:
    """Your main application."""
    
    def __init__(self, root, app_version):
        self.root = root
        self.app_version = app_version
        
        self.root.title(f"My Application v{app_version}")
        self.root.geometry("800x600")
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400)
        y = (self.root.winfo_screenheight() // 2) - (300)
        self.root.geometry(f"+{x}+{y}")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the main application UI."""
        # Header
        header_frame = tk.Frame(self.root, bg='#3498db', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="My Awesome Application",
            font=('Arial', 24, 'bold'),
            bg='#3498db',
            fg='white'
        )
        title.pack(expand=True)
        
        version_label = tk.Label(
            header_frame,
            text=f"Version {self.app_version}",
            font=('Arial', 10),
            bg='#3498db',
            fg='white'
        )
        version_label.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor='se')
        
        # Content area
        content_frame = tk.Frame(self.root, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        welcome_label = tk.Label(
            content_frame,
            text="Welcome to the Application!",
            font=('Arial', 18),
            bg='white',
            fg='#2c3e50'
        )
        welcome_label.pack(pady=30)
        
        info_label = tk.Label(
            content_frame,
            text="This is a demo application with auto-update functionality.\n\n"
                 "The updater checked for updates before this window appeared.\n"
                 "If an update was available, you would have seen the update dialog first.",
            font=('Arial', 11),
            bg='white',
            fg='#666',
            justify=tk.CENTER
        )
        info_label.pack(pady=20)
        
        # Some example buttons
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(pady=30)
        
        btn1 = tk.Button(
            button_frame,
            text="Button 1",
            command=lambda: messagebox.showinfo("Info", "Button 1 clicked!"),
            bg='#3498db',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor='hand2'
        )
        btn1.pack(side=tk.LEFT, padx=10)
        
        btn2 = tk.Button(
            button_frame,
            text="Button 2",
            command=lambda: messagebox.showinfo("Info", "Button 2 clicked!"),
            bg='#2ecc71',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor='hand2'
        )
        btn2.pack(side=tk.LEFT, padx=10)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#ecf0f1', height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="© 2025 Your Company Name",
            font=('Arial', 9),
            bg='#ecf0f1',
            fg='#666'
        )
        footer_label.pack(expand=True)


def main():
    # ============= CONFIGURATION =============
    APP_VERSION = __version__
    # =========================================
    
    # When using MSI, we don't need manual copying/relaunching.
    # The installer handles placement.
    
    # Create root window (hidden initially)
    root = tk.Tk()
    root.withdraw()  # Hide main window until update check is complete
    
    def show_main_app():
        """Called after update check/installation is complete."""
        root.deiconify()  # Show main window
        MainApplication(root, APP_VERSION)
    
    # Show update splash screen first
    splash = UpdateSplashScreen(
        root,
        APP_VERSION,
        show_main_app
    )
    
    root.mainloop()


if __name__ == "__main__":
    main()