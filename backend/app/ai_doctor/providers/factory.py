"""
AI 提供商工厂
Factory for AI providers
"""
from typing import Optional
from app.ai_doctor.providers.base import BaseAIProvider
from app.ai_doctor.providers.openai import OpenAIProvider
from app.ai_doctor.providers.anthropic import AnthropicProvider
from app.ai_doctor.providers.gemini import GeminiProvider


class AIProviderFactory:
    """
    提供商工厂类
    AI Provider Factory
    """
    
    @staticmethod
    def get_provider(
        provider_name: str, 
        api_key: str, 
        model: str, 
        base_url: Optional[str] = None
    ) -> BaseAIProvider:
        """
        获取具体的提供商实例
        Get specific provider instance
        """
        p_name = provider_name.lower()
        
        if p_name == "openai" or p_name == "siliconflow" or p_name == "modelscope":
            # SiliconFlow 和 ModelScope 使用 OpenAI 兼容接口
            # SiliconFlow and ModelScope use OpenAI compatible interface
            default_url = None
            if p_name == "siliconflow":
                default_url = "https://api.siliconflow.cn/v1/chat/completions"
            elif p_name == "modelscope":
                default_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
                
            return OpenAIProvider(api_key, base_url or default_url, model)
            
        elif p_name == "anthropic":
            return AnthropicProvider(api_key, base_url, model)
            
        elif p_name == "gemini":
            return GeminiProvider(api_key, base_url, model)
            
        else:
            # 默认回退到 OpenAI 格式，因为它是事实上的标准
            # Fallback to OpenAI format as it's the de-facto standard
            return OpenAIProvider(api_key, base_url, model)
