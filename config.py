"""Конфигурация для OpenAPI Documentation Generator."""

from typing import Literal
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class LLMConfig:
    """Конфигурация для LLM провайдеров."""
    provider: Literal["ollama", "openai", "anthropic", "huggingface"] = "ollama"
    model: str = "mistral"
    api_key: str = ""
    base_url: str = "http://localhost:11434"  # Для Ollama
    temperature: float = 0.7
    max_tokens: int = 2000


@dataclass
class DocumentationConfig:
    """Конфигурация для генератора документации."""
    output_dir: str = "docs"
    input_dir: str = "examples"
    include_examples: bool = True
    include_schemas: bool = True
    include_security: bool = True
    language: Literal["ru", "en"] = "ru"
    generate_toc: bool = True
    generate_diagrams: bool = False


def get_llm_from_config(config: LLMConfig):
    """Инициализирует LLM на основе конфигурации."""
    from langchain_community.llms import Ollama
    from langchain_openai import ChatOpenAI
    from langchain_anthropic import ChatAnthropic
    from langchain_huggingface import HuggingFaceEndpoint
    
    if config.provider == "ollama":
        return Ollama(
            model=config.model,
            base_url=config.base_url,
            temperature=config.temperature,
        )
    elif config.provider == "openai":
        return ChatOpenAI(
            api_key=config.api_key or os.getenv("OPENAI_API_KEY"),
            model_name=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
    elif config.provider == "anthropic":
        return ChatAnthropic(
            api_key=config.api_key or os.getenv("ANTHROPIC_API_KEY"),
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
    elif config.provider == "huggingface":
        return HuggingFaceEndpoint(
            repo_id=config.model,
            huggingfacehub_api_token=config.api_key or os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            temperature=config.temperature,
            max_new_tokens=config.max_tokens,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {config.provider}")
