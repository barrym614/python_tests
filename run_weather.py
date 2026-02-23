"""Launcher script for the weather_app GUI.

Run from the workspace root with:

    python run_weather.py

"""
from weather_app.gui import WeatherApp


def main():
    app = WeatherApp()
    app.run()


if __name__ == "__main__":
    main()
