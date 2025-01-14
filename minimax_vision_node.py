import requests
import base64
import io
from PIL import Image
import torch
import logging
import os
import json
import hashlib
import folder_paths
import sys
import time
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
        self.api_key = None
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum time between requests in seconds
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.api_key = config.get('minimax_api_key', '')
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                self.api_key = ''
        else:
            self.save_config()

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        config = {
            'minimax_api_key': self.api_key or ''
        }
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

config = Config()

class ComfyUIMinimaxVision:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "What is in this image?"}),
                "image": ("IMAGE",),
                "model": ("STRING", {"default": "MiniMax-Text-01", "choices": ["MiniMax-Text-01", "abab6.5s-chat"]}),
                "temperature": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 2.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 4096, "min": 1, "max": 1000192, "step": 1}),
                "top_p": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "ComfyUI/Minimax Vision"

    def process(self, prompt, image, model, temperature, max_tokens, top_p):
        try:
            if not config.api_key:
                return ("Please add your Minimax API key to config.json",)

            logger.info(f"Processing image. Type: {type(image)}, Shape: {getattr(image, 'shape', 'No shape')}")

            # Convert tensor to numpy array
            if isinstance(image, torch.Tensor):
                image = image.squeeze().cpu().numpy()

            # Handle channel order
            if len(image.shape) == 3 and image.shape[0] in [1, 3, 4]:
                image = image.transpose(1, 2, 0)

            # Convert to PIL Image
            if len(image.shape) == 2:
                pil_image = Image.fromarray((image * 255).astype('uint8'), 'L')
            elif len(image.shape) == 3:
                if image.shape[2] == 1:
                    pil_image = Image.fromarray((image[:, :, 0] * 255).astype('uint8'), 'L')
                elif image.shape[2] == 3:
                    pil_image = Image.fromarray((image * 255).astype('uint8'), 'RGB')
                elif image.shape[2] == 4:
                    pil_image = Image.fromarray((image * 255).astype('uint8'), 'RGBA').convert('RGB')
                else:
                    raise ValueError(f"Unexpected number of channels: {image.shape[2]}")
            else:
                raise ValueError(f"Unexpected image shape: {image.shape}")

            logger.info(f"Processed PIL Image size: {pil_image.size}")

            # Convert image to base64
            buffered = io.BytesIO()
            pil_image.save(buffered, format="JPEG", quality=95)
            base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{base64_image}"

            headers = {
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json"
            }

            messages = [
                {
                    "role": "system",
                    "content": "MM Intelligent Assistant is a large language model that is self-developed by MiniMax and does not call the interface of other products."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ]
            
            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "stream": False
            }

            # Add rate limiting
            current_time = time.time()
            time_since_last_request = current_time - config.last_request_time
            if time_since_last_request < config.min_request_interval:
                time.sleep(config.min_request_interval - time_since_last_request)
            
            logger.info("Sending request to Minimax API")
            response = requests.post("https://api.minimaxi.chat/v1/text/chatcompletion_v2", 
                                  headers=headers, json=data)
            config.last_request_time = time.time()

            if response.status_code == 200:
                try:
                    result = response.json()
                    logger.info(f"API Response: {result}")
                    
                    # Check for API-specific error codes in base_resp
                    if "base_resp" in result:
                        status_code = result["base_resp"].get("status_code")
                        status_msg = result["base_resp"].get("status_msg", "Unknown error")
                        
                        if status_code != 0:  # Non-zero status code indicates an error
                            error_message = f"Minimax API Error: {status_msg} (Code: {status_code})"
                            if status_code == 1008:
                                error_message = "Insufficient balance in your Minimax account. Please recharge your account balance."
                            logger.error(error_message)
                            return (error_message,)
                    
                    # Check if the response has the expected structure
                    if not isinstance(result, dict):
                        return (f"Unexpected response format: {result}",)
                        
                    if "choices" not in result or not result["choices"]:
                        return (f"API Error: {result.get('base_resp', {}).get('status_msg', 'Unknown error')}",)
                        
                    if "message" not in result["choices"][0]:
                        return (f"No message in first choice: {result}",)
                        
                    if "content" not in result["choices"][0]["message"]:
                        return (f"No content in message: {result}",)
                    
                    response_content = result["choices"][0]["message"]["content"]
                    logger.info("Received successful response from Minimax API")
                    return (response_content,)
                    
                except json.JSONDecodeError as e:
                    error_message = f"Failed to parse API response: {str(e)}, Response text: {response.text}"
                    logger.error(error_message)
                    return (error_message,)
                except KeyError as e:
                    error_message = f"Unexpected response structure: {str(e)}, Full response: {result}"
                    logger.error(error_message)
                    return (error_message,)
            else:
                try:
                    error_response = response.json()
                    error_message = f"API Error {response.status_code}: {error_response}"
                except:
                    error_message = f"API Error {response.status_code}: {response.text}"
                logger.error(error_message)
                return (error_message,)

        except Exception as e:
            error_message = f"Error in process method: {str(e)}"
            logger.exception(error_message)
            return (error_message,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "ComfyUIMinimaxVision": ComfyUIMinimaxVision,
}

# Node display name
NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUIMinimaxVision": "Minimax Vision"
}