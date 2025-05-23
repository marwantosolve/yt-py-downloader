#!/usr/bin/env python3
"""
YouTube Video Downloader with Quality Selection
A professional, user-friendly script to download YouTube videos with preferred quality.
"""

import yt_dlp
import os
import sys
import time
import random
from typing import List, Dict, Optional


class YouTubeDownloader:
  def __init__(self):
    """Initialize download directory and base options."""
    self.download_path = os.path.join(os.getcwd(), 'yt_downloads')
    os.makedirs(self.download_path, exist_ok=True)
    self.base_opts = {
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
        },
        'socket_timeout': 30,
        'retries': 3,
        'fragment_retries': 3,
        'skip_unavailable_fragments': True,
        'sleep_interval': 1,
        'max_sleep_interval': 3,
    }

  def get_video_info(self, url: str) -> Optional[Dict]:
    """Fetch video information without downloading."""
    ydl_opts = {'quiet': True, 'no_warnings': True, **self.base_opts}
    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)
    except Exception as e:
      print(f"Error: {str(e)}")
      return None

  def calculate_accurate_size(self, video_format: Dict, audio_format: Dict, duration: int = 0) -> int:
    """Calculate combined file size using available info."""
    video_size = video_format.get(
        'filesize') or video_format.get('filesize_approx')
    audio_size = audio_format.get('filesize') if audio_format else None
    if video_size and audio_size:
      return video_size + audio_size
    if duration > 0:
      video_bitrate = video_format.get('vbr') or video_format.get('tbr')
      audio_bitrate = audio_format.get('abr', 128) if audio_format else 128
      if video_bitrate:
        video_bytes = int((video_bitrate * 1000 / 8) * duration)
        audio_bytes = int((audio_bitrate * 1000 / 8) * duration)
        return video_bytes + audio_bytes
    height = video_format.get('height', 720)
    fps = video_format.get('fps', 30)
    vcodec = video_format.get('vcodec', 'avc1')
    bitrate_estimates = {
        2160: (25000, 15000, 18000),
        1440: (16000, 10000, 12000),
        1080: (8000, 5000, 6000),
        720: (5000, 3000, 3500),
        480: (2500, 1500, 1800),
        360: (1000, 600, 700),
        240: (700, 400, 500),
    }
    closest_height = min(bitrate_estimates.keys(),
                         key=lambda x: abs(x - height))
    base_bitrates = bitrate_estimates[closest_height]
    if 'av01' in vcodec.lower() or 'av1' in vcodec.lower():
      estimated_bitrate = base_bitrates[1]
    elif 'vp9' in vcodec.lower() or 'vp09' in vcodec.lower():
      estimated_bitrate = base_bitrates[2]
    else:
      estimated_bitrate = base_bitrates[0]
    if fps > 30:
      estimated_bitrate = int(estimated_bitrate * (fps / 30))
    if duration > 0:
      video_bytes = int((estimated_bitrate * 1000 / 8) * duration)
      audio_bytes = int((128 * 1000 / 8) * duration)
      return video_bytes + audio_bytes
    if video_size:
      if audio_format:
        audio_bitrate = audio_format.get('abr', 128)
        if duration > 0:
          audio_bytes = int((audio_bitrate * 1000 / 8) * duration)
          return video_size + audio_bytes
        else:
          audio_percentage = min(0.15, audio_bitrate / 1000)
          return int(video_size * (1 + audio_percentage))
      else:
        return video_size
    return 0

  def get_best_audio_format(self, formats: List[Dict]) -> Optional[Dict]:
    """Return the best quality audio format available."""
    audio_formats = [
        fmt for fmt in formats
        if fmt.get('acodec', 'none') != 'none' and fmt.get('vcodec', 'none') == 'none'
    ]
    if not audio_formats:
      return None
    audio_formats.sort(key=lambda x: x.get('abr', 0), reverse=True)
    return audio_formats[0]

  def format_file_size(self, size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
      return "Unknown"
    if size_bytes >= 1024**3:
      return f"{size_bytes / (1024**3):.1f} GB"
    elif size_bytes >= 1024**2:
      return f"{size_bytes / (1024**2):.0f} MB"
    elif size_bytes >= 1024:
      return f"{size_bytes / 1024:.0f} KB"
    else:
      return f"{size_bytes} B"

  def format_duration(self, seconds: int) -> str:
    """Format seconds to hh:mm:ss or mm:ss."""
    if seconds is None or seconds <= 0:
      return "?"
    h, m = divmod(seconds, 3600)
    m, s = divmod(m, 60)
    if h:
      return f"{h}:{m:02d}:{s:02d}"
    else:
      return f"{m}:{s:02d}"

  def display_available_formats(self, formats: List[Dict], duration: int = 0) -> List[Dict]:
    """Display available video formats with duration."""
    print("\nAvailable video qualities:")
    print("-" * 80)
    print("  # | Quality | Resolution | FPS | Format | Bitrate | Duration | Audio")
    print("-" * 80)
    best_audio = self.get_best_audio_format(formats)
    audio_info = f"AAC {best_audio.get('abr', '128')}k" if best_audio else "Included"
    video_formats = [fmt for fmt in formats if fmt.get(
        'height') and fmt.get('vcodec', 'none') != 'none']
    video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
    seen = set()
    unique_formats = []
    for fmt in video_formats:
      key = (fmt.get('height', 0), fmt.get('fps', 30))
      if key not in seen:
        seen.add(key)
        unique_formats.append(fmt)
    unique_formats.sort(key=lambda x: (
        x.get('height', 0), x.get('fps', 30)), reverse=True)
    display_formats = []
    for i, fmt in enumerate(unique_formats, 1):
      width = fmt.get('width', '?')
      height = fmt.get('height', '?')
      resolution = f"{width}x{height}"
      fps = fmt.get('fps', 30)
      ext = fmt.get('ext', 'mp4')
      bitrate = fmt.get('vbr') or fmt.get('tbr') or 0
      bitrate_str = f"{int(bitrate)}k" if bitrate else "?"
      fmt_duration = fmt.get('duration', duration)
      duration_str = self.format_duration(fmt_duration)
      if height >= 2160:
        quality_label = "4K"
      elif height >= 1440:
        quality_label = "2K"
      elif height >= 1080:
        quality_label = "1080p"
      elif height >= 720:
        quality_label = "720p"
      elif height >= 480:
        quality_label = "480p"
      elif height >= 360:
        quality_label = "360p"
      else:
        quality_label = f"{height}p"
      print(f"{i:2d} | {quality_label:>7} | {resolution:>10} | {fps:>3} | {ext:>6} | {bitrate_str:>7} | {duration_str:>8} | {audio_info}")
      display_formats.append(fmt)
    return display_formats

  def get_user_choice(self, max_options: int) -> int:
    """Prompt user to select a format."""
    while True:
      choice = input(
          f"Select quality (1-{max_options}) or 'q' to quit: ").strip()
      if choice.lower() == 'q':
        print("Download cancelled.")
        sys.exit(0)
      try:
        choice_num = int(choice)
        if 1 <= choice_num <= max_options:
          return choice_num - 1
        else:
          print(f"Please enter a number between 1 and {max_options}.")
      except ValueError:
        print("Please enter a valid number or 'q' to quit.")

  def download_video(self, url: str, format_id: str, title: str, quality_info: Dict):
    """Download the video using the selected format and show actual file size after download."""
    height = quality_info.get('height', 0)
    if height >= 2160:
      quality_label = "4K"
    elif height >= 1440:
      quality_label = "2K"
    elif height >= 1080:
      quality_label = "1080p"
    elif height >= 720:
      quality_label = "720p"
    elif height >= 480:
      quality_label = "480p"
    elif height >= 360:
      quality_label = "360p"
    else:
      quality_label = f"{height}p"
    safe_title = "".join(c for c in title if c.isalnum()
                         or c in (' ', '-', '_', '.')).rstrip()
    safe_title = safe_title[:80]
    filename_with_quality = f"{safe_title} [{quality_label}]"
    print(f"Saving to: {self.download_path}")
    download_methods = [
        {
            'name': 'Selected quality + best audio',
            'format': f'{format_id}+bestaudio/best',
            'merge_format': 'mp4'
        },
        {
            'name': 'Selected quality only',
            'format': f'best[format_id={format_id}]',
            'merge_format': None
        },
        {
            'name': 'Best available under 1080p',
            'format': 'best[height<=1080]/best',
            'merge_format': 'mp4'
        },
    ]
    for method in download_methods:
      try:
        ydl_opts = {
            'format': method['format'],
            'outtmpl': os.path.join(self.download_path, f'{filename_with_quality}.%(ext)s'),
            'noplaylist': True,
            **self.base_opts,
            'writeinfojson': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
        if method['merge_format']:
          ydl_opts['merge_output_format'] = method['merge_format']
        time.sleep(random.uniform(1, 2))
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          ydl.download([url])
        # Find the actual file (could be mp4, mkv, webm, etc.)
        for ext in ['mp4', 'mkv', 'webm', 'mov', 'flv']:
          file_path = os.path.join(
              self.download_path, f'{filename_with_quality}.{ext}')
          if os.path.exists(file_path):
            actual_size = os.path.getsize(file_path)
            print(
                f"Actual file size: {self.format_file_size(actual_size)} ({file_path})")
            break
        print(f"Download completed: {title}")
        print(f"Location: {self.download_path}")
        return
      except Exception as e:
        continue
    print("All download methods failed. Possible reasons: restricted/private video, regional blocking, or temporary issues.")

  def run(self):
    """Main application flow."""
    print("YouTube Video Downloader")
    print("=" * 30)
    while True:
      url = input("Enter YouTube URL (or 'q' to quit): ").strip()
      if url.lower() == 'q':
        print("Goodbye.")
        sys.exit(0)
      if not url:
        print("Please enter a valid URL.")
        continue
      if not any(domain in url for domain in ['youtube.com', 'youtu.be', 'm.youtube.com']):
        print("This doesn't look like a YouTube URL. Please try again.")
        continue
      break
    video_info = self.get_video_info(url)
    if not video_info:
      print("Could not fetch video information. Please check the URL and try again.")
      return
    if 'entries' in video_info:
      entries = [entry for entry in video_info['entries'] if entry]
      print(f"\nPlaylist: {video_info.get('title', 'Untitled Playlist')}")
      print(f"Number of videos: {len(entries)}")
      if not entries:
        print("No videos found in this playlist.")
        return
      first_video = entries[0]
      formats = first_video.get('formats', [])
      duration = first_video.get('duration', 0)
      if not formats:
        print("No formats available for the first video.")
        return
      video_formats = self.display_available_formats(formats, duration)
      if not video_formats:
        print("No video formats found. This might be a live stream or unavailable video.")
        return
      choice_index = self.get_user_choice(len(video_formats))
      selected_format = video_formats[choice_index]
      height = selected_format.get('height', '?')
      quality_name = "4K" if height >= 2160 else "2K" if height >= 1440 else f"{height}p"
      print(f"Selected: {quality_name} quality for all videos in the playlist")
      print(f"Resolution: {selected_format.get('width', '?')}x{height}")
      confirm = input(
          "Start downloading the entire playlist? (y/n): ").strip().lower()
      if confirm not in ['y', 'yes']:
        print("Download cancelled.")
        return
      for idx, entry in enumerate(entries, 1):
        title = entry.get('title', f'Video {idx}')
        duration = entry.get('duration', 0)
        print(f"\nDownloading video {idx}/{len(entries)}: {title}")
        formats = entry.get('formats', [])
        fmt = next((f for f in formats if f.get('format_id')
                   == selected_format.get('format_id')), None)
        if not fmt:
          print("Selected quality not available for this video. Skipping.")
          continue
        self.download_video(entry['webpage_url'],
                            selected_format['format_id'], title, fmt)
      print("All available videos in the playlist have been processed.")
      return
    title = video_info.get('title', 'Unknown Title')
    duration = video_info.get('duration', 0)
    uploader = video_info.get('uploader', 'Unknown')
    view_count = video_info.get('view_count', 0)
    print(f"\nVideo: {title}")
    print(f"Channel: {uploader}")
    if duration:
      mins, secs = divmod(duration, 60)
      print(f"Duration: {mins}:{secs:02d}")
    if view_count:
      print(f"Views: {view_count:,}")
    formats = video_info.get('formats', [])
    if not formats:
      print("No formats available for this video.")
      return
    video_formats = self.display_available_formats(formats, duration)
    if not video_formats:
      print("No video formats found. This might be a live stream or unavailable video.")
      return
    choice_index = self.get_user_choice(len(video_formats))
    selected_format = video_formats[choice_index]
    height = selected_format.get('height', '?')
    quality_name = "4K" if height >= 2160 else "2K" if height >= 1440 else f"{height}p"
    print(f"Selected: {quality_name} quality")
    print(f"Resolution: {selected_format.get('width', '?')}x{height}")
    confirm = input("Start download? (y/n): ").strip().lower()
    if confirm in ['y', 'yes']:
      self.download_video(
          url, selected_format['format_id'], title, selected_format)
    else:
      print("Download cancelled.")


def main():
  """Entry point for the downloader."""
  try:
    downloader = YouTubeDownloader()
    downloader.run()
  except KeyboardInterrupt:
    print("\nDownload interrupted by user.")
  except Exception as e:
    print(f"\nUnexpected error: {str(e)}")
    print("Make sure you have yt-dlp installed: pip install yt-dlp")
    print("If issues persist, try updating: pip install --upgrade yt-dlp")


if __name__ == "__main__":
  main()
