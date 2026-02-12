import requests
from typing import List, Optional, ClassVar, Dict, Any
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs.chat_result import ChatResult
from langchain_core.outputs.chat_generation import ChatGeneration

class PostChatModel(BaseChatModel):
    model_name: str = "post-chat-model"

    # ===== 默认配置=====
    DEFAULT_URL: ClassVar[str]= "xxxx"
    DEFAULT_HEADERS: ClassVar[dict] = {"Content-Type": "application/json","Authorization": "xxxxx"}
    DEFAULT_TIMEOUT: ClassVar[int] = 600

    # ===== 默认 =====
    url: str = DEFAULT_URL
    headers: Dict[str, str] = DEFAULT_HEADERS
    timeout: int = DEFAULT_TIMEOUT
    default_model_meta: Dict[str, Any] = {
        "frequency_penalty": 0,
        "max_tokens": 16384,
        "response_format": {"type": "json_object"},
        "stream": False,      
        "temperature": 0.95,
        "top_k": 0,
        "top_p": 0.9,
    }

    def __init__(
        self,
        url: Optional[str] = None,
        headers: Optional[dict] = None,
        timeout: Optional[int] = None,
        default_model_meta: Optional[dict] = None,
    ):
        super().__init__()
        self.url = url or self.DEFAULT_URL
        self.headers = headers or self.DEFAULT_HEADERS
        self.timeout = timeout or self.DEFAULT_TIMEOUT

        # 默认 model_meta，可被 invoke() 时覆盖
        self.default_model_meta = default_model_meta or {
            "frequency_penalty": 0,
            "max_tokens": 16384,
            "response_format": {"type": "json_object"},
            "stream": False,      
            "temperature": 0.95,
            "top_k": 0,
            "top_p": 0.9,
        }

    @property
    def _llm_type(self) -> str:
        return "post_chat_model"

    def _messages_to_openai(self, messages: List[BaseMessage]):
        """
        LangChain Message -> OpenAI-style dict
        """
        role_mapping = {
            "human": "user",
            "ai": "assistant",
            "system": "system"
        }
        return [
            {
                "role": role_mapping.get(m.type, m.type),
                "content": m.content
            }
            for m in messages
        ]

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        model_meta = self.default_model_meta.copy()

        # 允许在 invoke() 时动态覆盖
        for k in ["temperature", "top_p", "top_k", "max_tokens", "frequency_penalty"]:
            if k in kwargs:
                model_meta[k] = kwargs[k]

        data = {
            "max_completion_tokens": kwargs.get(
                "max_completion_tokens", 65535
            ),
            "messages": self._messages_to_openai(messages),
            "model_meta": model_meta,
            "stream": self.default_model_meta["stream"]
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json=data,
            timeout=self.timeout,
        )
        response.raise_for_status()

        result = response.json()

        # === 关键：拆解 ===
        choices = result.get("choices", [])
        if not choices:
            raise ValueError(f"Empty choices from LLM: {result}")

        message = choices[0].get("message", {})
        content = message.get("content", "")

        chat_generation = ChatGeneration(message=AIMessage(content=content))
        
        # 创建并返回ChatResult对象
        return ChatResult(generations=[chat_generation])
