# Weather App

Simple standalone Python app with a Tkinter UI that shows current weather.

Quick start

1. Install runtime dependency:

```bash
pip install -r weather_app/requirements.txt
```

2. Run the GUI:

```bash
python run_weather.py
```

3. To fetch real data, set the `WEATHER_API_KEY` environment variable to an OpenWeatherMap API key, or paste it into the UI.

Installation and platform notes

 - Python packages (pip): keep these in `weather_app/requirements.txt`. Install them from the workspace root:

```bash
python3 -m pip install -r weather_app/requirements.txt
```

- System packages (Ubuntu/Debian): GUI support and optional headless runner require OS packages installed via `apt`:

```bash
sudo apt update
sudo apt install -y python3-tk xvfb
```

- If you are on a different Linux distribution, install the equivalent system packages (`python3-tk` or the Tk bindings for your distro).

Running (GUI)

From the project root (`/home/barry/Documents/python_tests`):

```bash
python3 run_weather.py
```

Running headless (no display)

If you're on a server without an X display, use `xvfb-run` to simulate a display:

```bash
xvfb-run python3 run_weather.py
```

Running with a real API key

```bash
export WEATHER_API_KEY="your_openweathermap_api_key"
python3 run_weather.py
```

Tests

Run the unit tests from the workspace root (ensures `weather_app` is importable):

```bash
PYTHONPATH=. python3 -m unittest discover -s weather_app/tests -v
```

Troubleshooting

- `ModuleNotFoundError: No module named 'weather_app'`: run commands from the repository root or set `PYTHONPATH=.` as shown above.
- `ModuleNotFoundError: No module named 'tkinter'`: install the OS Tk package (`python3-tk` on Ubuntu/Debian) and re-run.
