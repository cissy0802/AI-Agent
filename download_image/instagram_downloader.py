"""
Instagram Image Downloader
Downloads all images from a public Instagram profile
"""

import instaloader
import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InstagramDownloader:
    """Downloads images from Instagram profiles"""
    
    def __init__(self, download_dir: str = "downloads", username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the Instagram downloader
        
        Args:
            download_dir: Directory to save downloaded images
            username: Instagram username for authentication (optional, but recommended)
            password: Instagram password (optional, but recommended)
        """
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        
        # Initialize Instaloader
        self.loader = instaloader.Instaloader(
            download_videos=False,  # Only download images
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,  # Set to True if you want JSON metadata
            compress_json=False,
            post_metadata_txt_pattern='',
            max_connection_attempts=3
        )
        
        # Try to login if credentials provided
        if username and password:
            try:
                logger.info(f"Attempting to login as {username}...")
                self.loader.login(username, password)
                logger.info("Login successful!")
            except Exception as e:
                logger.warning(f"Login failed: {e}")
                logger.warning("Continuing without login (may have limited access)")
        elif username:
            # Try to load session if it exists
            try:
                self.loader.load_session_from_file(username)
                logger.info(f"Loaded session for {username}")
            except FileNotFoundError:
                logger.info("No saved session found. Continuing without authentication.")
    
    def download_profile(self, profile_username: str, max_posts: Optional[int] = None) -> int:
        """
        Download all images from an Instagram profile
        
        Args:
            profile_username: Instagram username (without @)
            max_posts: Maximum number of posts to download (None for all)
            
        Returns:
            Number of posts downloaded
        """
        try:
            logger.info(f"Fetching profile: {profile_username}")
            profile = instaloader.Profile.from_username(self.loader.context, profile_username)
            
            logger.info(f"Profile found: {profile.full_name or profile_username}")
            logger.info(f"Total posts: {profile.mediacount}")
            
            # Create profile-specific directory
            profile_dir = self.download_dir / profile_username
            profile_dir.mkdir(exist_ok=True)
            
            # Change to profile directory for downloads
            original_dir = os.getcwd()
            os.chdir(profile_dir)
            
            try:
                downloaded_count = 0
                posts_to_download = max_posts if max_posts else profile.mediacount
                
                logger.info(f"Starting download of up to {posts_to_download} posts...")
                
                for post in profile.get_posts():
                    if max_posts and downloaded_count >= max_posts:
                        break
                    
                    try:
                        # Only download if it's a single image (not a carousel)
                        if post.typename == 'GraphImage':
                            self.loader.download_pic(
                                filename=post.shortcode,
                                url=post.url,
                                mtime=post.date_local
                            )
                            downloaded_count += 1
                            logger.info(f"Downloaded [{downloaded_count}/{posts_to_download}]: {post.shortcode}")
                        elif post.typename == 'GraphSidecar':
                            # For carousel posts, download all images
                            for idx, node in enumerate(post.get_sidecar_nodes()):
                                if node.is_video:
                                    continue  # Skip videos
                                self.loader.download_pic(
                                    filename=f"{post.shortcode}_{idx}",
                                    url=node.display_url,
                                    mtime=post.date_local
                                )
                            downloaded_count += 1
                            logger.info(f"Downloaded carousel [{downloaded_count}/{posts_to_download}]: {post.shortcode} ({post.typename})")
                        
                    except Exception as e:
                        logger.error(f"Error downloading post {post.shortcode}: {e}")
                        continue
                
                logger.info(f"Download complete! Downloaded {downloaded_count} posts.")
                return downloaded_count
                
            finally:
                os.chdir(original_dir)
                
        except instaloader.exceptions.ProfileNotExistsException:
            logger.error(f"Profile '{profile_username}' does not exist or is private.")
            return 0
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            logger.error(f"Profile '{profile_username}' is private and you're not following it.")
            logger.error("Please login with an account that follows this profile.")
            return 0
        except Exception as e:
            logger.error(f"Error downloading profile: {e}")
            return 0
    
    def download_single_post(self, post_url: str) -> bool:
        """
        Download a single Instagram post by URL
        
        Args:
            post_url: Full URL to the Instagram post
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Extract shortcode from URL
            # URL format: https://www.instagram.com/p/SHORTCODE/
            shortcode = post_url.split('/p/')[-1].rstrip('/')
            
            logger.info(f"Downloading post: {shortcode}")
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            
            # Create directory for single post
            post_dir = self.download_dir / "single_posts"
            post_dir.mkdir(exist_ok=True)
            
            original_dir = os.getcwd()
            os.chdir(post_dir)
            
            try:
                if post.typename == 'GraphImage':
                    self.loader.download_pic(
                        filename=post.shortcode,
                        url=post.url,
                        mtime=post.date_local
                    )
                    logger.info(f"Downloaded: {post.shortcode}")
                elif post.typename == 'GraphSidecar':
                    for idx, node in enumerate(post.get_sidecar_nodes()):
                        if node.is_video:
                            continue
                        self.loader.download_pic(
                            filename=f"{post.shortcode}_{idx}",
                            url=node.display_url,
                            mtime=post.date_local
                        )
                    logger.info(f"Downloaded carousel: {post.shortcode}")
                
                return True
            finally:
                os.chdir(original_dir)
                
        except Exception as e:
            logger.error(f"Error downloading post: {e}")
            return False


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='Download images from Instagram profiles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all images from a profile (no login required for public profiles)
  python instagram_downloader.py grapeot
  
  # Download with login (recommended for better access)
  python instagram_downloader.py grapeot --username your_username --password your_password
  
  # Download more posts (default is 10)
  python instagram_downloader.py grapeot --max-posts 50
  
  # Download to custom directory
  python instagram_downloader.py grapeot --output-dir my_downloads
  
  # Download a single post by URL
  python instagram_downloader.py --post-url "https://www.instagram.com/p/ABC123/"
        """
    )
    
    parser.add_argument('profile', nargs='?', help='Instagram username (without @)')
    parser.add_argument('--post-url', type=str, help='Download a single post by URL instead of a profile')
    parser.add_argument('--username', type=str, help='Your Instagram username (for authentication)')
    parser.add_argument('--password', type=str, help='Your Instagram password (for authentication)')
    parser.add_argument('--output-dir', type=str, default='downloads', 
                       help='Directory to save downloaded images (default: downloads)')
    parser.add_argument('--max-posts', type=int, default=10,
                       help='Maximum number of posts to download (default: 10)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.post_url and not args.profile:
        parser.error("Either provide a profile username or use --post-url")
    
    # Initialize downloader
    downloader = InstagramDownloader(
        download_dir=args.output_dir,
        username=args.username,
        password=args.password
    )
    
    # Download
    if args.post_url:
        success = downloader.download_single_post(args.post_url)
        if success:
            print(f"\n✓ Successfully downloaded post!")
            print(f"✓ Saved to: {args.output_dir}/single_posts/")
        else:
            print("\n✗ Failed to download post")
            sys.exit(1)
    else:
        count = downloader.download_profile(args.profile, max_posts=args.max_posts)
        if count > 0:
            print(f"\n✓ Successfully downloaded {count} posts from @{args.profile}")
            print(f"✓ Saved to: {args.output_dir}/{args.profile}/")
        else:
            print(f"\n✗ No posts were downloaded from @{args.profile}")
            sys.exit(1)


if __name__ == "__main__":
    main()

