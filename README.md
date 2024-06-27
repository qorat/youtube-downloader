# YouTube Video Downloader

This is a Python-based YouTube video downloader with a graphical user interface. It allows users to download YouTube videos in various qualities, with options for both video and audio.

## Features

- Download YouTube videos in various qualities
- Select audio quality separately
- User-friendly graphical interface
- Save user preferences
- Automatic file renaming to avoid conflicts
- Option to keep or delete temporary files
- NVENC support for faster encoding on compatible systems

## Requirements

- Python 3.7+
- PyQt6
- pytube
- ffmpeg-python

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - On macOS: `brew install ffmpeg`
   - On Linux: `sudo apt-get install ffmpeg`

## Usage

Run the main script:
```
python main.py
```

1. Enter a YouTube URL in the input field.
2. Click "Search" to load the video information.
3. Select your desired video and audio quality.
4. Click "Download" and choose a save location.
5. Wait for the download to complete.

## Settings

Access the settings menu to customize:
- Default output path
- Default video and audio quality
- Option to keep temporary files
- Auto-renaming of existing files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [pytube](https://github.com/pytube/pytube) for YouTube video downloading
- [FFmpeg](https://ffmpeg.org/) for video processing

## Disclaimer

This tool is for personal use only. Respect YouTube's terms of service and content creators' rights when using this software.
