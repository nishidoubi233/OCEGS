"""
AI 提供商基类
Base AI Provider class for multi-model integration
"""
import abc
from typing import List, Dict, Any, Optional


class BaseAIProvider(abc.ABC):
    """
    AI 提供商基类
    Abstract base class for all AI providers
    """

    def __init__(self, api_key: str, base_url: Optional[str] = None, model: str = ""):
        # API 密钥 / API Key
        self.api_key = api_key
        # 基础 URL (可选) / Base URL (optional)
        self.base_url = base_url
        # 模型名称 / Model name
        self.model = model

    @abc.abstractmethod
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        生成对话响应
        Generate chat completion response
        
        Args:
            messages: 消息列表 / List of messages [{'role': 'user', 'content': '...'}]
            temperature: 随机性 / Temperature for randomness
            max_tokens: 最大令牌数 / Maximum tokens to generate
            
        Returns:
            str: AI 响应内容 / AI response content
        """
        pass
