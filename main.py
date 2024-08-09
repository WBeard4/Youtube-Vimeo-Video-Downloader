import os
import platform
import subprocess
import sys
import re
import unicodedata

# Currently only working for Windows, will be adding mac functionality later
def get_videos_path():
    if platform.system() == 'Windows':
        return os.path.join(os.environ['USERPROFILE'], 'Videos')
    elif platform.system() == 'Darwin':
        return os.path.join(os.environ['HOME'], 'Movies')
    else:
        raise Exception('Unsupported operating system.')



def sanitize_filename(filename):
    # Normalize the Unicode string to NFKD form to decompose characters
    normalized_filename = unicodedata.normalize('NFKD', filename)
    
    # Remove any combining marks (diacritics)
    sanitized_filename = "".join(c for c in normalized_filename if not unicodedata.combining(c))
    
    # Replace or remove invalid characters (anything other than alphanumerics, spaces, dots, and underscores)
    sanitized_filename = re.sub(r'[^a-zA-Z0-9 ._]', '', sanitized_filename)
    
    # Trim whitespace and return
    return sanitized_filename.strip()


def get_executable_paths():
    try:
        # Determine the base directory, whether running as a script or an executable
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)  # For bundled executable
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # For script

        # Paths to ffmpeg and yt-dlp
        ffmpeg_path = os.path.join(base_dir, 'ffmpeg\\ffmpeg.exe')
        yt_dlp_path = os.path.join(base_dir, 'yt-dlp\\yt-dlp.exe')

        # Check if the files exist
        if not os.path.exists(ffmpeg_path):
            print(f"Error: FFmpeg not found at {ffmpeg_path}")
            sys.exit(1)

        if not os.path.exists(yt_dlp_path):
            print(f"Error: yt-dlp not found at {yt_dlp_path}")
            sys.exit(1)

        print(f"FFmpeg path: {ffmpeg_path}")
        print(f"yt-dlp path: {yt_dlp_path}")

        # Return the paths
        return yt_dlp_path, ffmpeg_path

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

yt_dlp_path, ffmpeg_path = get_executable_paths()

        
def download_video(url, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Construct yt-dlp command

    try:
        command = [
            yt_dlp_path, 
            '--impersonate', 'Safari',  # Ensure impersonation target is specified
            '--format', 'bestvideo+bestaudio/best',  # Format selection
            '--merge-output-format', 'mp4',  # Merge formats into mp4
            '--ffmpeg-location', ffmpeg_path,  # Specify FFmpeg location
            '--output', os.path.join(output_path, '%(title)s.%(ext)s'),  # Output location
            url
        ]


        print(f'''Video downloading now, and will be output to {output_path}.
            The console will close automatically when the video is downloaded.''')
        
        subprocess.run(command, check=True)
        print(f"Video downloaded and merged successfully to {output_path}")

    # Error reporting for debugging    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError as fnf_error:
        print(f"FileNotFoundError: {fnf_error}")
        print(f"Failed to find file. Command attempted: {command}")
    except PermissionError as p_error:
        print(f"PermissionError: {p_error}")
        print(f"Command attempted: {command}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

# Actual script, get user input and run the commands and subprocess command
video_url = ""
while 'youtube.com' not in video_url.lower() and "vimeo.com" not in video_url.lower():
    video_url = input("Please paste the video url here. Youtube or Vimeo only: ")
output_path = get_videos_path()
download_video(video_url, output_path)
