"""
Google Gemini 提供商实现
Google Gemini provider implementation
"""
import httpx
from typing import List, Dict, Optional
from app.ai_doctor.providers.base import BaseAIProvider


class GeminiProvider(BaseAIProvider):
    """
    Google Gemini 提供商实现
    Google Gemini provider implementation
    """

    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        调用 Gemini API (Google AI SDK 格式)
        Call Gemini API (Google AI SDK format)
        """
        root = self.base_url if self.base_url else "https://generativelanguage.googleapis.com"
        # 兼容性处理
        # Compatibility handling
        root = root.rstrip("/")
        
        is_google = "generativelanguage.googleapis.com" in root
        endpoint = f"{root}/v1beta/models/{self.model}:generateContent"
        
        # 如果是 Google 官方接口，通常在 URL 中传 key
        # If it's official Google API, usually pass key in URL
        url = f"{endpoint}?key={self.api_key}" if is_google else endpoint
        
        headers = {"Content-Type": "application/json"}
        # 如果不是官方接口，可能需要 header 传 key
        # If not official, might need key in header
        if not is_google:
            headers["x-goog-api-key"] = self.api_key

        # 转换消息格式：system -> systemInstruction, user/assistant -> contents
        # Convert message format: system -> systemInstruction, user/assistant -> contents
        system_instruction = None
        contents = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = {"parts": [{"text": msg["content"]}]}
            else:
                role = "model" if msg["role"] == "assistant" else "user"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        
        if system_instruction:
            payload["systemInstruction"] = system_instruction

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # 遵循 Gemini 响应结构
                # Follow Gemini response structure
                if "candidates" in data and len(data["candidates"]) > 0:
                    parts = data["candidates"][0].get("content", {}).get("parts", [])
                    if parts:
                        return "".join([p.get("text", "") for p in parts])
                
                return f"Error: Invalid or empty response from Gemini"
            except Exception as e:
                return f"Error connecting to Gemini: {str(e)}"
