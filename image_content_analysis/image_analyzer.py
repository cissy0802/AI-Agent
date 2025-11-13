"""
Image Content Analyzer using GPT-4o API
Analyzes images and answers questions about their content using OpenAI's vision capabilities.
"""

import os
import base64
import argparse
import logging
from pathlib import Path
from typing import Optional, Union
import requests
from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError, AuthenticationError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ImageAnalyzer:
    """Analyzes image content using GPT-4o vision API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the image analyzer
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from OPENAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. "
                "Provide it as an argument or set OPENAI_API_KEY environment variable."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"  # GPT-4o with vision capabilities
    
    def _encode_image(self, image_path: str) -> str:
        """
        Encode image file to base64 string
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded string of the image
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def _get_image_data(self, image_source: str) -> dict:
        """
        Get image data in the format required by OpenAI API
        
        Args:
            image_source: Path to local image file or URL to image
            
        Returns:
            Dictionary with image data for API request
        """
        # Check if it's a URL
        if image_source.startswith(('http://', 'https://')):
            return {
                "type": "image_url",
                "image_url": {"url": image_source}
            }
        
        # Otherwise, treat as local file path
        image_path = Path(image_source)
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_source}")
        
        # Encode local image to base64
        base64_image = self._encode_image(str(image_path))
        
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{image_path.suffix[1:]};base64,{base64_image}"
            }
        }
    
    def analyze_image(
        self,
        image_source: str,
        prompt: str = "Describe this image in detail. Include all important elements, objects, people, text, colors, and any other notable features.",
        max_tokens: int = 300
    ) -> str:
        """
        Analyze an image and get a description
        
        Args:
            image_source: Path to local image file or URL to image
            prompt: Custom prompt for image analysis
            max_tokens: Maximum number of tokens in the response
            
        Returns:
            Analysis result as a string
        """
        try:
            logger.info(f"Analyzing image: {image_source}")
            
            image_data = self._get_image_data(image_source)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            image_data
                        ]
                    }
                ],
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            logger.info("Analysis completed successfully")
            return result
            
        except RateLimitError as e:
            error_msg = (
                "API quota exceeded. You have exceeded your current OpenAI API quota.\n"
                "Please check your plan and billing details at: https://platform.openai.com/account/billing\n"
                f"Error details: {str(e)}"
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        except AuthenticationError as e:
            error_msg = (
                "Authentication failed. Please check your OpenAI API key.\n"
                "Make sure it's set correctly in the OPENAI_API_KEY environment variable or --api-key argument.\n"
                f"Error details: {str(e)}"
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        except APIConnectionError as e:
            error_msg = (
                "Failed to connect to OpenAI API. Please check your internet connection.\n"
                f"Error details: {str(e)}"
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        except APIError as e:
            error_msg = f"OpenAI API error: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            raise
    
    def ask_question(
        self,
        image_source: str,
        question: str,
        max_tokens: int = 300
    ) -> str:
        """
        Ask a specific question about an image
        
        Args:
            image_source: Path to local image file or URL to image
            question: Question to ask about the image
            max_tokens: Maximum number of tokens in the response
            
        Returns:
            Answer to the question
        """
        try:
            logger.info(f"Answering question about image: {image_source}")
            logger.info(f"Question: {question}")
            
            image_data = self._get_image_data(image_source)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": question},
                            image_data
                        ]
                    }
                ],
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            logger.info("Question answered successfully")
            return result
            
        except RateLimitError as e:
            error_msg = (
                "API quota exceeded. You have exceeded your current OpenAI API quota.\n"
                "Please check your plan and billing details at: https://platform.openai.com/account/billing\n"
                f"Error details: {str(e)}"
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        except AuthenticationError as e:
            error_msg = (
                "Authentication failed. Please check your OpenAI API key.\n"
                "Make sure it's set correctly in the OPENAI_API_KEY environment variable or --api-key argument.\n"
                f"Error details: {str(e)}"
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        except APIConnectionError as e:
            error_msg = (
                "Failed to connect to OpenAI API. Please check your internet connection.\n"
                f"Error details: {str(e)}"
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        except APIError as e:
            error_msg = f"OpenAI API error: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise


def main():
    """Main function for command-line interface"""
    parser = argparse.ArgumentParser(
        description="Analyze images using GPT-4o vision API"
    )
    parser.add_argument(
        "image",
        type=str,
        help="Path to local image file or URL to image"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)"
    )
    parser.add_argument(
        "--question",
        "-q",
        type=str,
        help="Ask a specific question about the image"
    )
    parser.add_argument(
        "--prompt",
        "-p",
        type=str,
        default="Describe this image in detail. Include all important elements, objects, people, text, colors, and any other notable features.",
        help="Custom prompt for image analysis (default: detailed description)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=300,
        help="Maximum number of tokens in response (default: 300)"
    )
    
    args = parser.parse_args()
    
    try:
        analyzer = ImageAnalyzer(api_key=args.api_key)
        
        if args.question:
            # Answer a specific question
            result = analyzer.ask_question(
                image_source=args.image,
                question=args.question,
                max_tokens=args.max_tokens
            )
            print("\n" + "="*60)
            print("QUESTION:")
            print(args.question)
            print("\n" + "="*60)
            print("ANSWER:")
            print(result)
        else:
            # General analysis
            result = analyzer.analyze_image(
                image_source=args.image,
                prompt=args.prompt,
                max_tokens=args.max_tokens
            )
            print("\n" + "="*60)
            print("IMAGE ANALYSIS:")
            print("="*60)
            print(result)
        
    except RuntimeError as e:
        # RuntimeError is raised for API errors with user-friendly messages
        print(f"\n❌ Error: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Failed to analyze image: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

