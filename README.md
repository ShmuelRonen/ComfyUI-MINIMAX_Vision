# ComfyUI Minimax Vision Node

This custom node integrates Minimax's Vision capabilities into ComfyUI, allowing you to analyze images and generate descriptions using Minimax's advanced vision models. The model provides exceptionally detailed and comprehensive descriptions with minimal content restrictions, making it ideal for accurate and thorough image analysis.

![site](https://github.com/user-attachments/assets/e49d6cbe-6407-40de-8b59-9f4ffc77ec53)

## Model Capabilities

- Generates highly detailed, natural descriptions
- Provides comprehensive analysis of image elements
- Minimal content restrictions compared to other vision models
- Excellent at detecting and describing subtle details
- Robust handling of complex scenes and multiple objects
- Reliable recognition of artistic styles and technical elements
- Strong performance with both photographic and artistic content

## ⚠️ Important Note: This is a Paid API

This node uses Minimax's paid API service:
- Minimum credit purchase: $25
- Cost per prompt: Approximately 1-2 cents
- API access requires an account at [Minimax Platform](https://intl.minimaxi.com/user-center/basic-information)

## Features

- Image analysis and description generation
- Support for both MiniMax-Text-01 and abab6.5s-chat models
- Configurable generation parameters (temperature, max tokens, etc.)
- Error handling and rate limiting
- Detailed logging for troubleshooting

## Installation

1. Create a custom nodes directory in your ComfyUI installation if you haven't already:
```bash
cd ComfyUI/custom_nodes
```

2. Clone this repository:
```bash
git clone https://github.com/ShmuelRonen/ComfyUI-Minimax-Vision.git
```
3. Restart ComfyUI

## Setup

1. Create an account on [Minimax Platform](https://intl.minimaxi.com/user-center/basic-information)
2. Purchase credits (minimum $25)
3. Get your API key from the Minimax dashboard
4. Create a `config.json` file in the node directory:
```json
{
    "minimax_api_key": "your-api-key-here"
}
```

## Usage

1. In ComfyUI, find the node under "ComfyUI/Minimax Vision"
2. Connect an image input
3. Set your prompt and parameters:
   - Model: Choose between MiniMax-Text-01 (recommended) or abab6.5s-chat
   - Temperature: 0.0 to 2.0 (default: 0.9)
   - Max Tokens: Up to 1000192 (default: 4096)
   - Top P: 0.0 to 1.0 (default: 1.0)

## Parameters

- `prompt`: Text prompt describing what you want to know about the image
- `image`: Input image to analyze
- `model`: Choice of Minimax vision models
- `temperature`: Controls randomness of the output
- `max_tokens`: Maximum length of the generated response
- `top_p`: Controls diversity of the output

## Example Workflow

1. Load an image using ComfyUI's image loader node
2. Connect it to the Minimax Vision node
3. Set your prompt (e.g., "Describe this image in detail")
4. Run the workflow
5. The node will return a detailed, unrestricted description of the image

### Example Prompts

For best results, try prompts like:
- "Provide a detailed analysis of this image, including all visual elements"
- "Describe everything you see in this image, including technical details"
- "Give a comprehensive breakdown of this artwork's composition and style"
- "Analyze this image thoroughly, including all objects and their relationships"

The model excels at providing complete, unfiltered descriptions and can recognize subtle details that other models might miss.

## Error Messages

- "Please add your Minimax API key to config.json": Check your configuration file
- "Insufficient balance": Recharge your Minimax account
- "API Error": Check your API key and account status

## Limitations

- Requires active internet connection
- API costs money per use
- Rate limited to prevent excessive API calls
- Image size and format limitations apply

## Why Choose This Model

- **Superior Detail Level**: Provides exceptionally thorough and nuanced descriptions
- **Natural Language**: Responses feel more human and less restricted
- **Comprehensive Analysis**: Catches details that other models might overlook
- **Versatile Recognition**: Excellent with various image types including artwork, photos, and technical content
- **Cost-Effective**: High-quality results at approximately 1-2 cents per prompt
- **Reliable Performance**: Consistent, high-quality outputs across different use cases

## Support

For issues with:
- The node itself: Open an issue in this repository
- API or billing: Contact [Minimax Support](https://intl.minimaxi.com/)
- ComfyUI integration: Check the [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)

## Credits

- Minimax for their Vision API
- ComfyUI team for the base framework
