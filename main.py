import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time
import sys
import os
import winshell
from win32com.client import Dispatch
from pathlib import Path


class PomodoroApp:
    def __init__(self):
        try:
            # Version info
            self.version = "1.0.0"
            self.app_name = "Tiny Timer"
            
            # Create desktop shortcut on first run
            self.create_desktop_shortcut()
            
            # Create a small, top-level, always-on-top window
            self.root = tk.Tk()
            self.root.title(f"Tiny Timer v{self.version}")
            
            # Calculate position for bottom right corner
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x_position = screen_width - 450  # 450 pixels from right edge
            y_position = screen_height - 35  # 35 pixels from bottom edge
            
            self.root.geometry(f"+{x_position}+{y_position}")
            self.root.overrideredirect(True)  # Remove title bar for a sleek look
            self.root.attributes("-topmost", True)  # Keep window on top

            # Timer variables
            self.pomodoro_time = 25 * 60  # 25 minutes for Pomodoro
            self.current_time = self.pomodoro_time
            self.timer_running = False

            # UI Layout
            self.frame = tk.Frame(self.root) 
            self.frame.pack(fill="both", expand=True)
            # Add hover bindings
            self.frame.bind("<Enter>", self.show_checkmarks)
            self.frame.bind("<Leave>", self.hide_checkmarks)


            # Timer Label - displays time and handles click events to show buttons
            self.label = tk.Label(
                self.frame, text="25:00", font=("Helvetica", 10), fg="black",
            )
            self.label.grid(row=0, column=0, padx=1)
            self.label.bind("<Button-1>", self.show_buttons)


            # Add checkmark counter (initially hidden)
            self.completed_pomodoros = 0
            self.checkmark_label = tk.Label(
                self.frame,
                text="",
                font=("Helvetica", 10),
                fg="green",
            )
            self.checkmark_label.grid(row=0, column=5, padx=1)
            self.checkmark_label.grid_remove()  # Initially hide checkmarks

            # Create play/pause toggle button
            self.pause_button = tk.Button(
                self.frame,
                text="⏯️",
                font=("Helvetica", 10),
                fg="black",
                command=self.toggle_timer,
                borderwidth=0,
                highlightthickness=0,
            )

            # Create reset button
            self.reset_button = tk.Button(
                self.frame,
                text="↻",
                font=("Helvetica", 10),
                fg="black",
                command=self.reset_timer,
                borderwidth=0,
                highlightthickness=0,
            )
            
            # Add quit button (moved before layout)
            self.quit_button = tk.Button(
                self.frame,
                text="x",   
                font=("Helvetica", 10),
                fg="black",
                command=self.quit_app,
                borderwidth=0,
                highlightthickness=0,
            )
            
            # Buttons layout
            self.pause_button.grid(row=0, column=2, padx=0)
            self.reset_button.grid(row=0, column=3, padx=0)
            self.quit_button.grid(row=0, column=4, padx=0)

            # Initially hide all buttons
            self.pause_button.grid_remove()
            self.reset_button.grid_remove()
            self.quit_button.grid_remove()

            # Add button visibility timer
            self.hide_buttons_job = None

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Tiny Timer: {str(e)}")
            sys.exit(1)

    def create_desktop_shortcut(self):
        try:
            # Get path to executable
            if getattr(sys, 'frozen', False):
                # If running as compiled executable
                application_path = sys.executable
            else:
                # If running as script
                application_path = os.path.abspath(__file__)

            # Get desktop path
            desktop = winshell.desktop()
            
            # Create shortcut path
            shortcut_path = os.path.join(desktop, f"{self.app_name}.lnk")
            
            # Only create shortcut if it doesn't exist
            if not os.path.exists(shortcut_path):
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = application_path
                shortcut.WorkingDirectory = os.path.dirname(application_path)
                shortcut.IconLocation = application_path  # Use the executable itself as the icon
                shortcut.save()
                
        except Exception as e:
            # Fail silently - shortcut creation is not critical
            print(f"Failed to create shortcut: {str(e)}")

    def toggle_timer(self):
        if self.timer_running:
            self.pause_timer()
        else:
            self.start_timer()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            Thread(target=self.update_timer).start()

    def update_timer(self):
        try:
            while self.timer_running and self.current_time > 0:
                mins, secs = divmod(self.current_time, 60)
                time_str = f"{mins:02}:{secs:02}"
                self.label.config(text=time_str)
                self.current_time -= 1
                time.sleep(1)

            if self.current_time == 0:
                self.completed_pomodoros += 1
                messagebox.showinfo("Tiny Timer", "Nice work!")
                self.reset_timer(clear_checkmarks=False)
                
        except Exception as e:
            messagebox.showerror("Error", f"Timer error: {str(e)}")
            self.pause_timer()

    def pause_timer(self):
        self.timer_running = False

    def reset_timer(self, clear_checkmarks=False):
        self.timer_running = False
        self.current_time = self.pomodoro_time
        self.label.config(text="25:00")
        # Only reset checkmarks if explicitly requested
        if clear_checkmarks:
            self.completed_pomodoros = 0
            self.checkmark_label.config(text="")

    def quit_app(self):
        self.timer_running = False  # Stop the timer if it's running
        self.root.destroy()  # Close the application window
 
    def show_buttons(self, event=None):
        # Cancel any pending hide job
        if self.hide_buttons_job:
            self.root.after_cancel(self.hide_buttons_job)
        
        # Show all buttons
        self.pause_button.grid()
        self.reset_button.grid()
        self.quit_button.grid()
        
        # Schedule hiding buttons after 4 seconds
        self.hide_buttons_job = self.root.after(4000, self.hide_buttons)

    def hide_buttons(self):
        # Hide all buttons instead of just pause
        self.pause_button.grid_remove()
        self.reset_button.grid_remove()
        self.quit_button.grid_remove()

    def show_checkmarks(self, event=None):
        if self.completed_pomodoros > 0:
            self.checkmark_label.config(text="✓" * self.completed_pomodoros)
            self.checkmark_label.grid()

    def hide_checkmarks(self, event=None):
        self.checkmark_label.grid_remove()

    def run(self):
        self.root.mainloop()


# Run the Pomodoro app
app = PomodoroApp()
app.run()
