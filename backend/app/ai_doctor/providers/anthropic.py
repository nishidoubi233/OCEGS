"""
Anthropic 提供商实现
Anthropic provider implementation
"""
import httpx
from typing import List, Dict, Optional
from app.ai_doctor.providers.base import BaseAIProvider


class AnthropicProvider(BaseAIProvider):
    """
    Anthropic (Claude) 提供商实现
    Anthropic (Claude) provider implementation
    """

    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        调用 Anthropic Messages API
        Call Anthropic Messages API
        """
        url = self.base_url if self.base_url else "https://api.anthropic.com/v1/messages"
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        # 将消息中的 'system' 角色提取出来，因为 Anthropic 有专门的 system 字段
        # Extract 'system' message as Anthropic has a dedicated system field
        system_content = ""
        filtered_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_content = msg["content"]
            else:
                filtered_messages.append(msg)
        
        payload = {
            "model": self.model,
            "messages": filtered_messages,
            "system": system_content,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # 遵循 Anthropic 响应结构
                # Follow Anthropic response structure
                if "content" in data and len(data["content"]) > 0:
                    return data["content"][0]["text"]
                else:
                    return f"Error: Invalid response format from Anthropic"
            except Exception as e:
                return f"Error connecting to Anthropic: {str(e)}"
