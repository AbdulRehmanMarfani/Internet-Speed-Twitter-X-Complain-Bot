# Internet Speed Tweeter

A Python script that checks your internet speed using Speedtest.net and automatically tweets a complaint to your ISP if the speeds are lower than what you’re paying for.

---

## Features

* Tests download and upload speed using [Speedtest.net](https://www.speedtest.net)
* Compares actual speeds with your promised speeds
* Logs into your Twitter (X) account and tweets a complaint if speeds are lower
* Can be run directly as a Python script or through a compiled `.exe` file

---

## Run the Executable (.exe)

1. Go to the [Releases](https://github.com/yourusername/internet-speed-tweeter/releases/latest) section of this repository
2. Download the `main.exe` file
3. Create a `.env` file in the same folder with the following format:

   ```
   PROMISED_DOWN=150
   PROMISED_UP=20
   EDGE_DRIVER_PATH=C:/path/to/msedgedriver.exe
   X_EMAIL=your_email@example.com
   X_PASSWORD=your_password
   X_USERNAME=your_username
   ```
4. Double-click `main.exe` to run

> Make sure the Edge WebDriver path is correct and matches your Edge browser version

---

## Run from Source Code (Python)

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/internet-speed-tweeter.git
   cd internet-speed-tweeter
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the format shown above

4. Run the script:

   ```
   python main.py
   ```

---

## Requirements

* Microsoft Edge browser
* Edge WebDriver (matching version)
* Twitter (X) account
* `.env` file with all required variables

---

## Files

* `main.py` — Main Python script
* `main.exe` — Precompiled executable
* `requirements.txt` — Python packages list
* `.env.example` — Example environment config

---

## License

MIT License

