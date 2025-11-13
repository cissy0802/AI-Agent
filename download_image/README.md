# Instagram Image Downloader

A Python program to download images from Instagram profiles using the `instaloader` library.

## Features

- Download all images from public Instagram profiles
- Download single posts by URL
- Support for carousel posts (multiple images in one post)
- Optional authentication for better access (especially for private profiles)
- Configurable download limits
- Automatic organization by profile name

## Requirements

- Python 3.7+
- Internet connection

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (Public Profiles)

For public profiles, you can download without logging in:

```bash
python instagram_downloader.py cissychen0802
```

This will download the first 10 images from the `cissychen0802` profile to the `downloads/cissychen0802/` directory (default limit is 10 posts).

### With Authentication (Recommended)

For better access and to download from private profiles you follow, use authentication:

```bash
python instagram_downloader.py cissychen0802 --username your_username --password your_password
```

**Note:** The first time you login, `instaloader` will save a session file, so you may not need to provide credentials every time.

### Download Limited Number of Posts

By default, the script downloads 10 posts. To download a different number:

```bash
# Download 20 posts instead of the default 10
python instagram_downloader.py cissychen0802 --max-posts 20

# Download all posts (no limit)
python instagram_downloader.py cissychen0802 --max-posts 9999
```

### Custom Output Directory

To save images to a different directory:

```bash
python instagram_downloader.py cissychen0802 --output-dir my_instagram_downloads
```

### Download a Single Post

To download a specific post by URL:

```bash
python instagram_downloader.py --post-url "https://www.instagram.com/p/ABC123/"
```

## Command-Line Options

- `profile` - Instagram username (without @) to download from
- `--post-url` - Download a single post by URL instead of a profile
- `--username` - Your Instagram username (for authentication)
- `--password` - Your Instagram password (for authentication)
- `--output-dir` - Directory to save downloaded images (default: `downloads`)
- `--max-posts` - Maximum number of posts to download (default: 10)

## Output Structure

```
downloads/
├── cissychen0802/
│   ├── ABC123.jpg
│   ├── DEF456.jpg
│   └── ...
└── single_posts/
    └── ...
```

## Important Notes

1. **Rate Limiting**: Instagram has rate limits. The script includes automatic rate limiting, but downloading many posts may take time.

2. **Private Profiles**: To download from private profiles, you must:
   - Login with an account that follows the private profile
   - Use the `--username` and `--password` flags

3. **Videos**: This script only downloads images. Videos are skipped.

4. **Terms of Service**: Please respect Instagram's Terms of Service and use this tool responsibly. Only download content you have permission to download.

5. **Session Files**: After logging in, `instaloader` saves a session file (usually `your_username_session-*.json`). This allows you to use the tool without providing credentials every time.

## Troubleshooting

**"Profile does not exist or is private"**
- Check that the username is correct (no @ symbol)
- If the profile is private, you need to login with an account that follows it

**"Login failed"**
- Check your username and password
- Instagram may require 2FA verification - you may need to use an app-specific password
- Try logging in manually on Instagram first to ensure your account is not locked

**"No posts downloaded"**
- The profile might not have any image posts (only videos)
- Check your internet connection
- Try logging in with credentials for better access

**Rate limiting errors**
- Wait a few minutes and try again
- Reduce the number of posts downloaded at once using `--max-posts`

## Example

```bash
# Download 10 images from cissychen0802 profile (default)
python instagram_downloader.py cissychen0802

# Download first 20 posts with authentication
python instagram_downloader.py cissychen0802 --username myuser --password mypass --max-posts 20

# Download to custom directory
python instagram_downloader.py cissychen0802 --output-dir instagram_backup
```

