# YouTube Video Downloader

A professional, user-friendly Python script to download YouTube videos and playlists with quality selection. Built with `yt-dlp`, this downloader provides an interactive interface to choose your preferred video quality and handles both individual videos and entire playlists.

## Features

- 🎥 **Single Video Downloads**: Download individual YouTube videos
- 📋 **Playlist Support**: Download entire playlists with consistent quality selection
- 🎯 **Quality Selection**: Interactive menu to choose from available video qualities (4K, 2K, 1080p, 720p, etc.)
- 📊 **Detailed Information**: Shows video duration, resolution, bitrate, and file size estimates
- 🔄 **Smart Fallback**: Multiple download methods with automatic fallback for reliability
- 📁 **Organized Storage**: Creates a dedicated download folder (`yt_downloads`)
- ⚡ **Robust Error Handling**: Built-in retry mechanisms and error recovery
- 🎵 **Audio Quality**: Automatically combines best available audio with selected video quality

## Prerequisites

- Python 3.6 or higher
- Internet connection
- Sufficient disk space for downloads

## Installation

### Ubuntu 24.04 LTS Setup

1. **Clone or download the repository**:
   ```bash
   git clone <your-repo-url>
   cd youtube-downloader
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv myenv
   ```

3. **Activate the virtual environment**:
   ```bash
   source myenv/bin/activate
   ```

4. **Install required dependencies**:
   ```bash
   pip install yt-dlp
   ```

### Other Operating Systems

**Windows:**
```cmd
python -m venv myenv
myenv\Scripts\activate
pip install yt-dlp
```

**macOS:**
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install yt-dlp
```

## Usage

### Running the Downloader

1. **Activate your virtual environment** (Ubuntu 24.04 LTS):
   ```bash
   source myenv/bin/activate
   ```

2. **Run the script**:
   ```bash
   python3 yt_download.py
   ```

### Single Video Download

1. Enter a YouTube video URL when prompted
2. Review the video information (title, duration, views)
3. Select your preferred quality from the interactive menu
4. Confirm the download to start

**Example:**
```
Enter YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Video: Never Gonna Give You Up
Channel: Rick Astley
Duration: 3:33
Views: 1,400,000,000

Available video qualities:
--------------------------------------------------------------------------------
  # | Quality | Resolution | FPS | Format | Bitrate | Duration | Audio
--------------------------------------------------------------------------------
  1 |    1080p |   1920x1080 |  30 |    mp4 |   2500k |     3:33 | AAC 128k
  2 |     720p |   1280x720  |  30 |    mp4 |   1500k |     3:33 | AAC 128k
  3 |     480p |    854x480  |  30 |    mp4 |   1000k |     3:33 | AAC 128k

Select quality (1-3) or 'q' to quit: 1
```

### Playlist Download

1. Enter a YouTube playlist URL
2. The script will analyze the first video to show available qualities
3. Select your preferred quality (applies to all videos in the playlist)
4. Confirm to download the entire playlist

**Example:**
```
Enter YouTube URL: https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMZQB_qXt6Pg-0s0iP

Playlist: My Favorite Songs
Number of videos: 25

Selected: 1080p quality for all videos in the playlist
Start downloading the entire playlist? (y/n): y

Downloading video 1/25: Song Title 1
Downloading video 2/25: Song Title 2
...
```

## File Organization

Downloads are saved to a `yt_downloads` folder in the same directory as the script:

```
your-project/
├── yt_download.py
├── yt_downloads/
│   ├── Video Title [1080p].mp4
│   ├── Another Video [720p].mp4
│   └── Playlist Video [4K].mp4
└── myenv/
```

## Quality Options

The downloader automatically detects and displays available qualities:

- **4K** (2160p): Ultra high definition
- **2K** (1440p): Quad HD
- **1080p**: Full HD
- **720p**: HD
- **480p**: Standard definition
- **360p**: Low definition
- **240p**: Very low definition

Each quality option shows:
- Resolution (width x height)
- Frame rate (FPS)
- Video format (mp4, webm, etc.)
- Estimated bitrate
- Duration
- Audio quality

## Advanced Features

### Smart Download Methods

The script uses multiple fallback methods for maximum compatibility:

1. **Primary**: Selected quality + best audio (merged to MP4)
2. **Fallback 1**: Selected quality only
3. **Fallback 2**: Best available quality under 1080p

### Audio Handling

- Automatically selects the best available audio quality
- Combines video and audio streams seamlessly
- Defaults to AAC format for maximum compatibility

### Error Recovery

- Built-in retry mechanisms for network issues
- Fragment retry for interrupted downloads
- Multiple user-agent headers to avoid blocking
- Graceful handling of restricted or private videos

## Tips for Best Results

1. **Use a stable internet connection** for large downloads
2. **Ensure sufficient disk space** before downloading playlists
3. **Keep yt-dlp updated** for the latest site compatibility:
   ```bash
   pip install --upgrade yt-dlp
   ```
4. **Use lower qualities** if you experience frequent interruptions

## Troubleshooting

### Common Issues

**"No formats available"**: The video might be private, restricted, or live-only.

**Download fails repeatedly**: Try updating yt-dlp or check your internet connection.

**"Command not found"**: Make sure your virtual environment is activated.

### Error Messages

```bash
# If you see import errors:
pip install --upgrade yt-dlp

# If you see permission errors on Ubuntu:
chmod +x yt_download.py

# To check if yt-dlp is working:
yt-dlp --version
```

## Virtual Environment Management

### Activating the Environment
```bash
# Ubuntu/macOS/Linux
source myenv/bin/activate

# Windows
myenv\Scripts\activate
```

### Deactivating the Environment
```bash
deactivate
```

### Removing the Environment
```bash
rm -rf myenv  # Linux/macOS
rmdir /s myenv  # Windows
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and personal use. Please respect YouTube's Terms of Service and copyright laws when downloading content.

## Disclaimer

This tool is for personal use only. Users are responsible for complying with YouTube's Terms of Service and applicable copyright laws. Do not download copyrighted content without permission.

---

**Happy downloading! 🎬**