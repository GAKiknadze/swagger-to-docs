"""Примеры использования OpenAPI Documentation Generator."""

from pathlib import Path
from config import LLMConfig, DocumentationConfig, get_llm_from_config
from advanced_generator import AdvancedOpenAPIDocGenerator


def example_with_ollama():
    """Пример использования с Ollama (локально)."""
    print("=" * 60)
    print("Example 1: Using Ollama (Local)")
    print("=" * 60)
    
    # Конфигурируем Ollama
    llm_config = LLMConfig(
        provider="ollama",
        model="mistral",  # или "llama2", "neural-chat"
        base_url="http://localhost:11434"
    )
    
    doc_config = DocumentationConfig(
        output_dir="docs",
        input_dir="examples",
        language="ru"
    )
    
    try:
        llm = get_llm_from_config(llm_config)
        generator = AdvancedOpenAPIDocGenerator(llm, output_dir=doc_config.output_dir)
        generator.process_directory(doc_config.input_dir)
    except Exception as e:
        print(f"Error: {e}")
        print("\n💡 Убедитесь, что Ollama запущена:")
        print("   1. ollama serve")
        print("   2. ollama pull mistral")


def example_with_openai():
    """Пример использования с OpenAI API."""
    print("=" * 60)
    print("Example 2: Using OpenAI GPT")
    print("=" * 60)
    
    import os
    
    # Получаем API ключ из переменной окружения
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return
    
    llm_config = LLMConfig(
        provider="openai",
        model="gpt-3.5-turbo",  # или "gpt-4"
        api_key=api_key,
        temperature=0.7
    )
    
    doc_config = DocumentationConfig(
        output_dir="docs",
        input_dir="examples",
        language="ru"
    )
    
    try:
        llm = get_llm_from_config(llm_config)
        generator = AdvancedOpenAPIDocGenerator(llm, output_dir=doc_config.output_dir)
        generator.process_directory(doc_config.input_dir)
    except Exception as e:
        print(f"Error: {e}")


def example_with_anthropic():
    """Пример использования с Claude (Anthropic)."""
    print("=" * 60)
    print("Example 3: Using Claude (Anthropic)")
    print("=" * 60)
    
    import os
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        return
    
    llm_config = LLMConfig(
        provider="anthropic",
        model="claude-3-sonnet-20240229",
        api_key=api_key
    )
    
    doc_config = DocumentationConfig(
        output_dir="docs",
        input_dir="examples",
        language="ru"
    )
    
    try:
        llm = get_llm_from_config(llm_config)
        generator = AdvancedOpenAPIDocGenerator(llm, output_dir=doc_config.output_dir)
        generator.process_directory(doc_config.input_dir)
    except Exception as e:
        print(f"Error: {e}")


def example_english_documentation():
    """Пример создания документации на английском языке."""
    print("=" * 60)
    print("Example 4: English Documentation")
    print("=" * 60)
    
    llm_config = LLMConfig(
        provider="ollama",
        model="mistral"
    )
    
    try:
        llm = get_llm_from_config(llm_config)
        generator = AdvancedOpenAPIDocGenerator(
            llm, 
            output_dir="docs_en",
            language="en"  # Английский язык
        )
        generator.process_directory("examples")
    except Exception as e:
        print(f"Error: {e}")


def example_specific_files():
    """Пример обработки конкретных файлов."""
    print("=" * 60)
    print("Example 5: Process Specific Files")
    print("=" * 60)
    
    llm_config = LLMConfig(provider="ollama", model="mistral")
    
    try:
        llm = get_llm_from_config(llm_config)
        generator = AdvancedOpenAPIDocGenerator(llm)
        
        # Обрабатываем конкретные файлы
        specific_files = [
            "examples/petstore.json",
            "examples/petstore-expanded.json"
        ]
        
        for file in specific_files:
            if Path(file).exists():
                generator.process_openapi_file(file)
            else:
                print(f"File not found: {file}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    """Запуск примеров."""
    print("\n🚀 OpenAPI Documentation Generator Examples\n")
    
    # Выбираем, какой пример запустить
    examples = {
        "1": ("Ollama (Local)", example_with_ollama),
        "2": ("OpenAI GPT", example_with_openai),
        "3": ("Claude (Anthropic)", example_with_anthropic),
        "4": ("English Docs", example_english_documentation),
        "5": ("Specific Files", example_specific_files),
    }
    
    print("Available examples:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    
    print("\nUsage:")
    print("  python examples.py <number>")
    print("  Example: python examples.py 1\n")
    
    import sys
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        if choice in examples:
            _, func = examples[choice]
            func()
        else:
            print(f"❌ Invalid choice: {choice}")
    else:
        print("💡 Running Ollama example by default...")
        example_with_ollama()
