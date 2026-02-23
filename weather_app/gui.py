"""Simple Tkinter GUI for the weather_app package.

Usage: create `WeatherApp()` and call `.run()`.
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox

from .weather import fetch_weather_for_location


class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather App")
        self._build()

    def _build(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.grid()

        ttk.Label(frm, text="Location (city, state or ZIP):").grid(column=0, row=0, sticky="w")
        self.location_var = tk.StringVar(value="London")
        ttk.Entry(frm, textvariable=self.location_var, width=40).grid(column=1, row=0)

        self.status = tk.StringVar(value="Ready")
        ttk.Button(frm, text="Lookup", command=self.refresh).grid(column=0, row=1, pady=8)
        ttk.Label(frm, textvariable=self.status).grid(column=1, row=1, sticky="w")

        self.output = tk.Text(frm, width=70, height=12, wrap="word")
        self.output.grid(column=0, row=2, columnspan=2, pady=(8, 0))

    def _set_status(self, txt: str):
        self.status.set(txt)

    def refresh(self):
        thread = threading.Thread(target=self._do_refresh, daemon=True)
        thread.start()

    def _do_refresh(self):
        self._set_status("Resolving location...")
        location = self.location_var.get().strip() or "London"
        try:
            data = fetch_weather_for_location(location)
        except Exception as e:
            self._set_status("Error")
            messagebox.showerror("Error", str(e))
            return

        self._set_status("OK")
        self.output.delete("1.0", tk.END)
        city = data.get("city")
        lat = data.get("lat")
        lon = data.get("lon")
        temp = data.get("temp_c")
        lines = [f"Location: {city}", f"Coordinates: {lat}, {lon}", f"Temp (°C): {temp}"]
        # include raw summary if helpful
        self.output.insert(tk.END, "\n".join(lines))

    def run(self):
        self.root.mainloop()
