# YouTube Video Downloader

## Overview

This YouTube Video Downloader is a Python-based application with a graphical user interface. It allows users to download YouTube videos in various qualities, with separate options for video and audio quality selection. The application is built with PyQt6 for the GUI, pytube for YouTube interaction, and FFmpeg for video processing.

## Features

- Download YouTube videos in multiple quality options
- Select audio quality separately from video quality
- User-friendly graphical interface
- Save and load user preferences
- Automatic file renaming to avoid conflicts
- Option to keep or delete temporary files
- NVENC support for faster encoding on compatible NVIDIA systems
- Thumbnail preview of videos
- Progress bar for download and processing status

## Requirements

- Python 3.7+
- PyQt6
- pytube
- ffmpeg-python
- FFmpeg (system installation)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/qorat/youtube-downloader.git
   cd youtube-downloader
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Enter a YouTube URL in the input field.
3. Click "Search" to load the video information.
4. Select your desired video and audio quality.
5. Click "Download" and choose a save location.
6. Wait for the download and processing to complete.

## Settings

Access the settings menu to customize:
- Default output path
- Default video and audio quality
- Option to keep temporary files
- Auto-renaming of existing files

## Project Structure

- `main.py`: The main application file with the GUI implementation
- `function.py`: Contains core functionalities for video downloading and processing
- `settings.py`: Manages user settings and preferences
- `requirements.txt`: List of Python package dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [pytube](https://github.com/pytube/pytube) for YouTube video downloading capabilities
- [FFmpeg](https://ffmpeg.org/) for video processing functionality

## Disclaimer

This tool is intended for personal use only. Please respect YouTube's terms of service and content creators' rights when using this software. The developers of this application are not responsible for any misuse or violation of YouTube's policies.
