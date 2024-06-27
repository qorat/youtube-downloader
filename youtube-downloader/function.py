import os
import ffmpeg
from pytube import YouTube

def convert_bytes(size):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while size >= 1024 and index < len(suffixes) - 1:
        size /= 1024.0
        index += 1
    return "{:.2f} {}".format(size, suffixes[index])

def downloadVideo(yt, _res, _abr, output_path, progress_callback, keep_temp_files=False):
    try:
        title = sanitize_filename(yt.title)
        video_filename = os.path.join(output_path, f"{title}_video")
        audio_filename = os.path.join(output_path, f"{title}_audio")
        output_filename = os.path.join(output_path, f"{title}.mp4")

        # Check if file already exists and rename if necessary
        output_filename = get_unique_filename(output_filename)

        # Download video
        video_stream = yt.streams.filter(res=_res).first()
        video_stream.download(filename=video_filename)
        progress_callback(33)

        # Download audio
        audio_stream = yt.streams.filter(abr=_abr).first()
        audio_stream.download(filename=audio_filename)
        progress_callback(66)

        # Merge video and audio
        video = ffmpeg.input(video_filename)
        audio = ffmpeg.input(audio_filename)
        combined = ffmpeg.concat(video, audio, v=1, a=1)
        output = ffmpeg.output(combined, output_filename, format="mp4", vcodec="libx264", acodec="aac", **{"b:v": "2M", "rc-lookahead": "32"})
        ffmpeg.run(output, overwrite_output=True)
        progress_callback(100)

        # Clean up temporary files
        if not keep_temp_files:
            os.remove(video_filename)
            os.remove(audio_filename)

    except Exception as e:
        # Clean up any partially downloaded files
        for file in [video_filename, audio_filename, output_filename]:
            if os.path.exists(file):
                os.remove(file)
        raise Exception(f"Error during download: {str(e)}")

def get_unique_filename(filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}_{counter}{extension}"
        counter += 1
    return filename

def getVideoQuality(yt):
    try:
        return sorted(set(stream.resolution for stream in yt.streams.filter(progressive=False, file_extension="mp4", type="video")), key=lambda x: int(x[:-1]) if x != None else 0, reverse=True)
    except Exception as e:
        raise Exception(f"Error getting video quality: {str(e)}")

def getAudioQuality(yt):
    try:
        return sorted(set(stream.abr for stream in yt.streams.filter(only_audio=True, file_extension="mp4")), key=lambda x: int(x[:-4]) if x != None else 0, reverse=True)
    except Exception as e:
        raise Exception(f"Error getting audio quality: {str(e)}")

def isLinkValid(link):
    try:
        yt = YouTube(link)
        yt.check_availability()
        return True
    except:
        return False

def format_view_count(views):
    if views < 1000:
        return str(views)
    elif views < 1_000_000:
        return f"{views / 1000:.1f}K"
    elif views < 1_000_000_000:
        return f"{views / 1_000_000:.1f}M"
    elif views < 1_000_000_000_000:
        return f"{views / 1_000_000_000:.1f}B"
    else:
        return f"{views / 1_000_000_000_000:.1f}T"

def seconds_to_time_string(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def sanitize_filename(filename):
    # Remove invalid characters from filename
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename.strip()

def get_total_file_size(yt, video_quality, audio_quality):
    try:
        video_size = yt.streams.filter(res=video_quality).first().filesize
        audio_size = yt.streams.filter(abr=audio_quality).first().filesize
        return video_size + audio_size
    except Exception as e:
        raise Exception(f"Error calculating file size: {str(e)}")