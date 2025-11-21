import subprocess
import os

def compress_video(input_path, output_path, target_size_mb=450):
    """
    Compresses a video file to a target size using ffmpeg.
    
    Args:
        input_path: Path to input video
        output_path: Path to save compressed video
        target_size_mb: Target file size in MB (default 450 MB to stay under 500 MB limit)
    
    Returns:
        output_path if successful, None if failed
    """
    try:
        # FFmpeg installation path
        ffmpeg_path = r"C:\Users\dkaough\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin\ffmpeg.exe"
        ffprobe_path = r"C:\Users\dkaough\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin\ffprobe.exe"
        
        # Get input video duration
        probe_cmd = [
            ffprobe_path,
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_path
        ]
        
        result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        duration = float(result.stdout.strip())
        
        # Calculate target bitrate (in kbps)
        # Formula: (target_size_MB * 8192) / duration_seconds
        target_bitrate = int((target_size_mb * 8192) / duration)
        
        # Ensure minimum quality
        if target_bitrate < 500:
            target_bitrate = 500
        
        print(f"Compressing video: {input_path}")
        print(f"Duration: {duration:.2f}s, Target bitrate: {target_bitrate}k")
        
        # Compress video with ffmpeg
        compress_cmd = [
            ffmpeg_path,
            '-i', input_path,
            '-c:v', 'libx264',  # H.264 codec
            '-b:v', f'{target_bitrate}k',  # Video bitrate
            '-c:a', 'aac',  # Audio codec
            '-b:a', '128k',  # Audio bitrate
            '-preset', 'medium',  # Encoding speed/quality balance
            '-movflags', '+faststart',  # Optimize for streaming
            '-y',  # Overwrite output file
            output_path
        ]
        
        print("Running ffmpeg compression...")
        subprocess.run(compress_cmd, check=True, capture_output=True, timeout=600)
        
        # Check output file size
        output_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Compression complete! Output size: {output_size_mb:.2f} MB")
        
        if output_size_mb > target_size_mb * 1.1:  # Allow 10% overage
            print(f"Warning: Output size ({output_size_mb:.2f} MB) exceeds target ({target_size_mb} MB)")
        
        return output_path
        
    except subprocess.TimeoutExpired:
        print("Error: FFmpeg compression timed out (>10 minutes)")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error: FFmpeg failed: {e.stderr.decode() if e.stderr else str(e)}")
        return None
    except Exception as e:
        print(f"Error compressing video: {e}")
        return None


def get_video_info(video_path):
    """
    Gets video file information (duration, size, bitrate).
    
    Returns:
        dict with 'duration', 'size_mb', 'bitrate' or None if failed
    """
    try:
        # FFmpeg installation path
        ffprobe_path = r"C:\Users\dkaough\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin\ffprobe.exe"
        
        # Get duration
        probe_cmd = [
            ffprobe_path,
            '-v', 'error',
            '-show_entries', 'format=duration,size,bit_rate',
            '-of', 'json',
            video_path
        ]
        
        result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        import json
        data = json.loads(result.stdout)
        
        format_data = data.get('format', {})
        
        return {
            'duration': float(format_data.get('duration', 0)),
            'size_mb': int(format_data.get('size', 0)) / (1024 * 1024),
            'bitrate': int(format_data.get('bit_rate', 0)) / 1000  # Convert to kbps
        }
        
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None
