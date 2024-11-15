import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time
import sys
import os
import winshell
from win32com.client import Dispatch
from pathlib import Path


class TinyTimer:
    def __init__(self, testing_mode=False):
        try:
            # Read version from file
            version_path = Path(__file__).parent / "version" / "version.txt"
            try:
                with open(version_path, "r") as f:
                    self.version = f.read().strip()
            except FileNotFoundError:
                self.version = "1.x.x"  # Fallback version if file not found
            print(f"Version: {self.version}")

            # Only create shortcut if not in testing mode
            if not testing_mode:
                self.create_desktop_shortcut()

            # Create a small, top-level, always-on-top window
            self.root = tk.Tk()
            self.root.title(f"Tiny Timer v{self.version}")

            # Calculate position for bottom right corner
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x_position = screen_width - 460  # 460 pixels from right edge
            y_position = screen_height - 35  # 35 pixels from bottom edge

            self.root.geometry(f"+{x_position}+{y_position}")
            self.root.overrideredirect(True)  # Remove title bar for a sleek look
            self.root.attributes("-topmost", True)  # Keep window on top

            # Timer variables TODO: make time text dynamic
            self.pomodoro_time = 25 * 60  # 25 minutes for Pomodoro
            self.time_text = "25:00"
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
                self.frame,
                text=self.time_text,
                font=("Helvetica", 10),
                fg="black",
            )
            self.label.grid(row=0, column=0, padx=1)
            self.label.bind("<Button-1>", self.handle_label_click)

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
            self.reset_button.grid(row=0, column=3, padx=0)
            self.quit_button.grid(row=0, column=4, padx=0)

            # Initially hide all buttons
            self.reset_button.grid_remove()
            self.quit_button.grid_remove()

            # Add button visibility timer
            self.hide_buttons_job = None

            # Check less frequently (every 45 seconds instead of every second)
            self.check_topmost()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Tiny Timer: {str(e)}")
            sys.exit(1)

    def create_desktop_shortcut(self):
        try:
            # Get path to executable
            if getattr(sys, "frozen", False):
                application_path = sys.executable
            else:
                application_path = os.path.abspath(__file__)

            # Get desktop path
            desktop = winshell.desktop()

            # Create shortcut path - using "Tiny Timer" as the app name
            shortcut_path = os.path.join(desktop, "Tiny Timer.lnk")

            # Only create shortcut if it doesn't exist
            if not os.path.exists(shortcut_path):
                shell = Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = application_path
                shortcut.WorkingDirectory = os.path.dirname(application_path)
                shortcut.IconLocation = application_path
                shortcut.save()

        except Exception as e:
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
                self.label.config(text="SLOTH TIME")
                self.completed_pomodoros += 1
                self.show_completion_dialog()
                self.reset_timer(clear_checkmarks=False)

        except Exception as e:
            messagebox.showerror("Error", f"Timer error: {str(e)}")
            self.pause_timer()

    def show_completion_dialog(self):
        # Create custom dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Tiny Timer")
        dialog.attributes("-topmost", True)
        
        # Load and resize the image
        image = tk.PhotoImage(file="sloth.gif")
    
        # Create a canvas to hold both image and text
        canvas = tk.Canvas(dialog, width=image.width(), height=image.height())
        canvas.pack()
        
        # Place image on canvas
        canvas.create_image(0, 0, anchor="nw", image=image)
        
        # Create text with background
        text_bg = canvas.create_rectangle(
            160, 20, image.width()-160, 60,  # Adjust coordinates as needed
            fill="white",
        )
        text = canvas.create_text(
            image.width()/2,42,  # Center text (adjust Y coordinate as needed)
            text="Nice work!",
            font=("Helvetica", 16, "bold"),
            fill="black"
        )
        
        # Keep reference to prevent garbage collection
        dialog.image = image
        
        # Congrs message and start next session button
        ok_button = tk.Button(
            dialog,
            text="Start Next Session",  # Fixed truncated text
            command=lambda: self.start_next_session(dialog)  # New command
        )
        ok_button.pack(pady=10)
        
        # Center the dialog on screen
        # Get screen dimensions
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        
        # Make dialog update its dimensions
        dialog.update_idletasks()
        
        # Calculate center position
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        x_position = (screen_width - dialog_width) // 2
        y_position = (screen_height - dialog_height) // 2
        
        # Set the position
        dialog.geometry(f"+{x_position}+{y_position}")
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def start_next_session(self, dialog):
        dialog.destroy()  # Close the dialog first
        self.reset_timer(clear_checkmarks=False)
        # Use root.after to start the timer after a brief delay
        self.root.after(100, self.start_timer)

    def pause_timer(self):
        self.timer_running = False

    def reset_timer(self, clear_checkmarks=False):
        # Force stop any running timer
        self.pause_timer()
        # Reset to initial state
        self.current_time = self.pomodoro_time
        self.label.config(text=self.time_text)
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
        self.reset_button.grid()
        self.quit_button.grid()

        # Schedule hiding buttons after 4 seconds
        self.hide_buttons_job = self.root.after(4000, self.hide_buttons)

    def hide_buttons(self):
        # Hide all buttons instead of just pause
        self.reset_button.grid_remove()
        self.quit_button.grid_remove()

    def show_checkmarks(self, event=None):
        if self.completed_pomodoros > 0:
            self.checkmark_label.config(text="✓" * self.completed_pomodoros)
            self.checkmark_label.grid()

    def hide_checkmarks(self, event=None):
        self.checkmark_label.grid_remove()

    def check_topmost(self):
        """Periodically ensures window stays on top"""
        self.root.attributes("-topmost", False)
        self.root.attributes("-topmost", True)
        # Check every 45000ms (45 seconds)
        self.root.after(45000, self.check_topmost)

    def run(self):
        self.root.mainloop()

    def handle_label_click(self, event=None):
        """Handle click on timer label - toggle timer and show buttons"""
        self.toggle_timer()  # Toggle timer state
        self.show_buttons()  # Show control buttons


# Run the Pomodoro app
app = TinyTimer(testing_mode=False)  # Set to True while testing
app.run()
