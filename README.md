# Maklad-Tube
This Python application provides a user-friendly GUI for downloading YouTube videos and playlists. It allows users to specify video formats (MP4 or MP3) and quality settings. The application supports downloading single videos as well as entire playlists, displaying real-time download progress and completion status.


![time](https://github.com/Muhammed-Maklad/Maklad-Tube/assets/119490645/04d66951-4b42-410b-a27d-c183ac9fb89d)


## Features

- Download videos from YouTube by entering the URL.
- Choose between MP4 and MP3 formats.
- Select video quality (360p, 480p, 720p, 1080p).
- Download progress and completion status.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Muhammed-Maklad/Maklad-Tube.git
    cd Maklad-Tube
    ```

2. **Install dependencies:**
    Ensure you have Python installed, then install the required packages.
    ```sh
    pip install -r requirements.txt
    ```

3. **Run The code**
   ```
   MakladTude.py
   ```
5. **Make Sure You put the rigth path in line : 104 , 169 , 178**
6. **To Convert it To application You only need to  write that command**
   ```
   pyinstaller --onefile --noconsole --icon=Youtube.ico MakladUTube.py
   ```

## Usage

- Enter a YouTube video URL in the input field.
- Choose the desired format (MP4 or MP3) and quality.
- Select a download directory or use the default.
- By defulat it downloads in Downloads of the device
- Click the "Download" button to start downloading.

## Issues

If you encounter any issues or have suggestions for improvement, please [open an issue](https://github.com/Muhammed-Maklad/Maklad-Tube/issues).

## License

This project is licensed under the [MIT License](LICENSE).
