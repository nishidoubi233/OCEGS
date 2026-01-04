"""
OpenAI 提供商实现 (兼容 OpenAI、SiliconFlow 等)
OpenAI provider implementation (Compatible with OpenAI, SiliconFlow, etc.)
"""
import httpx
import json
from typing import List, Dict, Optional
from app.ai_doctor.providers.base import BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    """
    OpenAI 格式提供商实现
    OpenAI format provider implementation
    """

    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        调用 OpenAI 兼容接口
        Call OpenAI compatible API
        """
        # 默认使用 OpenAI 官方 API，如果 base_url 为空
        # Default to OpenAI official API if base_url is empty
        url = self.base_url if self.base_url else "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # 遵循 OpenAI 标准响应结构
                # Follow OpenAI standard response structure
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    return f"Error: Invalid response format from {url}"
            except Exception as e:
                return f"Error connecting to AI backend: {str(e)}"
