# Image Content Analyzer

A Python program that utilizes the GPT-4o API to analyze image content. It can describe images in detail and answer questions about their content using OpenAI's vision capabilities.

## Features

- **Image Description**: Get detailed descriptions of images including objects, people, text, colors, and other notable features
- **Question Answering**: Ask specific questions about image content
- **Multiple Input Formats**: Supports both local image files and image URLs
- **Customizable Prompts**: Use custom prompts for specific analysis needs
- **Secure API Key Handling**: Supports API key via environment variable or command-line argument

## Requirements

- Python 3.7+
- OpenAI API key (get one at https://platform.openai.com/api-keys)
- Internet connection

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key as an environment variable (recommended):

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or you can provide it via the `--api-key` argument (less secure).

## Usage

### Basic Image Description

Analyze an image and get a detailed description:

```bash
python image_analyzer.py path/to/image.jpg
```

Or with an image URL:

```bash
python image_analyzer.py https://example.com/image.jpg
```

### Ask Questions About Images

Ask a specific question about an image:

```bash
python image_analyzer.py path/to/image.jpg --question "What is written on the sign in this image?"
```

Or using the short form:

```bash
python image_analyzer.py path/to/image.jpg -q "How many people are in this image?"
```

### Custom Analysis Prompts

Use a custom prompt for specific analysis needs:

```bash
python image_analyzer.py path/to/image.jpg --prompt "List all the objects in this image and their colors"
```

### Adjust Response Length

Control the maximum length of the response:

```bash
python image_analyzer.py path/to/image.jpg --max-tokens 500
```

### Using API Key as Argument

If you prefer not to use environment variables:

```bash
python image_analyzer.py path/to/image.jpg --api-key your-api-key-here
```

## Supported Image Formats

The program supports common image formats including:
- JPEG/JPG
- PNG
- GIF
- WebP
- BMP

## Examples

### Example 1: Describe a photo

```bash
python image_analyzer.py vacation_photo.jpg
```

Output:
```
============================================================
IMAGE ANALYSIS:
============================================================
This image shows a beautiful beach scene at sunset. The sky 
is painted in warm orange and pink hues. There are several 
palm trees in the foreground, and the ocean appears calm 
with gentle waves. Two beach chairs are positioned near the 
water's edge...
```

### Example 2: Extract text from image

```bash
python image_analyzer.py document.jpg -q "What text is visible in this image?"
```

### Example 3: Count objects

```bash
python image_analyzer.py scene.jpg -q "How many cars are visible in this image?"
```

### Example 4: Analyze from URL

```bash
python image_analyzer.py https://example.com/chart.png -q "What does this chart show?"
```

## Programmatic Usage

You can also use the `ImageAnalyzer` class in your own Python code:

```python
from image_analyzer import ImageAnalyzer

# Initialize analyzer
analyzer = ImageAnalyzer()  # Uses OPENAI_API_KEY env var

# Get image description
description = analyzer.analyze_image("path/to/image.jpg")
print(description)

# Ask a question
answer = analyzer.ask_question(
    "path/to/image.jpg",
    "What is the main subject of this image?"
)
print(answer)
```

## Error Handling

The program includes comprehensive error handling for:
- Missing API keys
- Invalid image paths
- Network errors
- API errors
- Unsupported image formats

## Notes

- The GPT-4o model is used for vision analysis, which provides high-quality image understanding
- API usage will incur costs based on OpenAI's pricing (check https://openai.com/pricing)
- Large images may take longer to process
- The default max_tokens is 300, but you can increase it for more detailed responses

## Troubleshooting

**Error: "OpenAI API key is required"**
- Make sure you've set the `OPENAI_API_KEY` environment variable or provided it via `--api-key`

**Error: "Image file not found"**
- Check that the image path is correct and the file exists
- Use absolute paths if relative paths don't work

**Error: API rate limits or quota exceeded**
- Check your OpenAI account usage and billing
- You may need to wait before making more requests

