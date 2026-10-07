import tkinter as tk
import threading
import random
import time
import subprocess
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key


class AutoclickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Autoclicker")
        self.root.geometry("300x360")
        self.root.resizable(False, False)

        self.clicking = False
        self.program_running = True
        self.click_count = 0

        self.min_delay_var = tk.DoubleVar(value=0.08)
        self.max_delay_var = tk.DoubleVar(value=0.19)
        self.jitter_var = tk.IntVar(value=2)

        # --- GUI Aufbau ---
        tk.Label(root, text="Autoclicker", font=("Arial", 14, "bold")).pack(pady=(10, 0))

        self.status_label = tk.Label(root, text="PAUSIERT", fg="red", font=("Arial", 16, "bold"))
        self.status_label.pack(pady=(5, 0))

        self.counter_label = tk.Label(root, text="Klicks: 0", font=("Arial", 10))
        self.counter_label.pack()

        # Delay-Regler
        tk.Label(root, text="Min. Verzögerung (Sek.):").pack(pady=(15, 0))
        tk.Scale(root, from_=0.03, to=2.0, resolution=0.01, orient="horizontal",
                 variable=self.min_delay_var, length=200,
                 command=self._validate_delays).pack()

        tk.Label(root, text="Max. Verzögerung (Sek.):").pack()
        tk.Scale(root, from_=0.03, to=2.0, resolution=0.01, orient="horizontal",
                 variable=self.max_delay_var, length=200,
                 command=self._validate_delays).pack()

        # Jitter-Regler
        tk.Label(root, text="Pixel-Jitter (0 = aus):").pack()
        tk.Scale(root, from_=0, to=5, resolution=1, orient="horizontal",
                 variable=self.jitter_var, length=200).pack()

        # Hotkey-Info
        tk.Label(root, text="F9: Start/Stopp | F10: Beenden | F11: Reset Zähler",
                 font=("Arial", 8, "italic"), fg="gray").pack(pady=10)

        # --- Threads starten ---
        self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
        self.click_thread.start()

        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _validate_delays(self, _=None):
        """Verhindert dass Min > Max ist."""
        if self.min_delay_var.get() > self.max_delay_var.get():
            self.max_delay_var.set(self.min_delay_var.get())

    def click_loop(self):
        """Der Klick-Thread mit Pixel-Jitter über xdotool."""
        mouse = Controller()
        while self.program_running:
            if self.clicking:
                jitter = self.jitter_var.get()

                if jitter > 0:
                    dx = random.randint(-jitter, jitter)
                    dy = random.randint(-jitter, jitter)
                    # xdotool für die Bewegung (funktioniert sauber auf Multi-Monitor)
                    subprocess.Popen(["xdotool", "mousemove_relative", "--", str(dx), str(dy)],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


                mouse.click(Button.left)

                self.click_count += 1
                self.root.after(0, self._update_counter)

                min_d = self.min_delay_var.get()
                max_d = self.max_delay_var.get()
                if min_d > max_d:
                    min_d = max_d
                time.sleep(random.uniform(min_d, max_d))
            else:
                time.sleep(0.05)

    def _update_counter(self):
        """Aktualisiert den Klick-Zähler."""
        self.counter_label.config(text=f"Klicks: {self.click_count:,}")

    def on_press(self, key):
        """Hotkey-Handler."""
        if key == Key.f9:
            self.clicking = not self.clicking
            self.root.after(0, self.update_status)
        elif key == Key.f10:
            self.root.after(0, self.on_close)
        elif key == Key.f11:
            self.click_count = 0
            self.root.after(0, self._update_counter)

    def update_status(self):
        """Aktualisiert die Status-Anzeige."""
        if self.clicking:
            self.status_label.config(text="LÄUFT", fg="green")
        else:
            self.status_label.config(text="PAUSIERT", fg="red")

    def on_close(self):
        """Sauberes Beenden."""
        self.clicking = False
        self.program_running = False
        try:
            self.listener.stop()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoclickerApp(root)
    root.mainloop()
