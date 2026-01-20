# 📚 OpenAPI to Markdown Documentation Generator

Мощный инструмент для преобразования OpenAPI/Swagger спецификаций в полноценную документацию на Markdown с использованием LangChain и LLM.

## ✨ Особенности

- 🤖 **LangChain Integration**: Использует LangChain Expression Language (LCEL) для генерации документации
- 🌍 **Множество LLM провайдеров**: Поддержка Ollama, OpenAI, Anthropic, HuggingFace
- 📄 **Структурированная генерация**: Отдельные файлы для каждого тега и эндпоинта
- 🏷️ **Группировка по тегам**: Автоматическая организация документации по категориям
- 🛡️ **Анализ безопасности**: Документирование требований к авторизации
- 📊 **Статистика и аналитика**: Встроенные инструменты для анализа OpenAPI
- 🌐 **Многоязычная поддержка**: Русский и английский языки
- 📝 **Примеры использования**: Готовые примеры curl запросов

## 🚀 Быстрый старт

### Установка зависимостей

```bash
pip install -e ".[ollama]"
# или для OpenAI:
pip install -e ".[openai]"
# или для Claude:
pip install -e ".[anthropic]"
```

### Базовое использование

#### С Ollama (локально)

```bash
# 1. Убедитесь, что Ollama запущена
ollama serve

# 2. В другом терминале скачайте модель
ollama pull mistral

# 3. Запустите генератор
python main.py
```

#### С OpenAI API

```bash
export OPENAI_API_KEY="sk-..."
python examples.py 2
```

#### С Claude (Anthropic)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python examples.py 3
```

## 📖 Примеры использования

### Пример 1: Обработка директории с OpenAPI файлами

```python
from config import LLMConfig, get_llm_from_config
from advanced_generator import AdvancedOpenAPIDocGenerator

# Инициализируем LLM
llm_config = LLMConfig(provider="ollama", model="mistral")
llm = get_llm_from_config(llm_config)

# Создаем генератор
generator = AdvancedOpenAPIDocGenerator(llm, output_dir="docs", language="ru")

# Обрабатываем директорию
generator.process_directory("examples")
```

### Пример 2: Обработка одного файла

```python
generator.process_openapi_file("examples/petstore.json")
```

### Пример 3: Анализ OpenAPI спецификации

```python
from utils import load_openapi, OpenAPIAnalyzer

spec = load_openapi("examples/petstore.json")
analyzer = OpenAPIAnalyzer(spec)

# Получить статистику
stats = analyzer.get_statistics()
print(f"Всего эндпоинтов: {stats['total_endpoints']}")

# Найти эндпоинты по тегу
pets_endpoints = analyzer.find_endpoints_by_tag("pets")

# Получить все схемы
schemas = analyzer.get_all_schemas()
```

### Пример 4: Экспорт в разные форматы

```python
from utils import load_openapi, OpenAPIExporter

spec = load_openapi("examples/petstore.json")
exporter = OpenAPIExporter(spec)

# Экспорт в CSV
exporter.export_endpoints_csv("endpoints.csv")

# Экспорт статистики в JSON
exporter.export_statistics_json("stats.json")

# Генерирование Postman коллекции
exporter.generate_postman_collection("postman.json")
```

## 📁 Структура проекта

```
swagger-to-docs/
├── main.py                    # Базовая реализация
├── advanced_generator.py       # Продвинутая реализация с LCEL
├── config.py                  # Конфигурация LLM и документации
├── utils.py                   # Утилиты для работы с OpenAPI
├── examples.py                # Примеры использования
├── examples/                  # Примеры OpenAPI файлов
│   ├── petstore.json
│   ├── petstore-expanded.json
│   ├── api.github.com.json
│   └── ...
└── docs/                      # Сгенерированная документация
    ├── swagger_petstore/
    │   ├── README.md          # Оглавление
    │   ├── tags/              # Документация по тегам
    │   │   ├── pets.md
    │   │   └── ...
    │   └── endpoints/         # Документация по эндпоинтам
    │       ├── get_pets.md
    │       ├── post_pets.md
    │       └── ...
```

## 🛠️ Конфигурация

### LLM конфигурация (config.py)

```python
@dataclass
class LLMConfig:
    provider: Literal["ollama", "openai", "anthropic", "huggingface"] = "ollama"
    model: str = "mistral"
    api_key: str = ""
    base_url: str = "http://localhost:11434"  # Для Ollama
    temperature: float = 0.7
    max_tokens: int = 2000
```

### Документация конфигурация

```python
@dataclass
class DocumentationConfig:
    output_dir: str = "docs"
    input_dir: str = "examples"
    include_examples: bool = True
    include_schemas: bool = True
    include_security: bool = True
    language: Literal["ru", "en"] = "ru"
    generate_toc: bool = True
    generate_diagrams: bool = False
```

## 📝 API Документация

### OpenAPIDocumentationGenerator

Базовая реализация с использованием LangChain Chains.

**Методы:**
- `process_openapi_file(file_path)` - Обработать один OpenAPI файл
- `process_directory(directory)` - Обработать всю директорию
- `extract_endpoints(spec)` - Извлечь эндпоинты
- `generate_endpoint_doc(key, endpoint, spec)` - Сгенерировать документацию эндпоинта

### AdvancedOpenAPIDocGenerator

Продвинутая реализация с использованием LCEL.

**Методы:**
- `process_openapi_file(file_path)` - Обработать OpenAPI файл
- `process_directory(directory)` - Обработать директорию
- `load_spec(file_path)` - Загрузить спецификацию

### OpenAPIAnalyzer

Анализирует OpenAPI спецификации.

**Методы:**
- `get_statistics()` - Получить статистику
- `find_endpoints_by_tag(tag)` - Найти эндпоинты по тегу
- `find_endpoints_by_method(method)` - Найти эндпоинты по HTTP методу
- `get_request_body_schema(path, method)` - Получить схему запроса
- `get_response_schemas(path, method)` - Получить схемы ответов
- `list_all_endpoints()` - Список всех эндпоинтов

### OpenAPIExporter

Экспортирует информацию в разные форматы.

**Методы:**
- `export_endpoints_csv(output_path)` - CSV с эндпоинтами
- `export_statistics_json(output_path)` - JSON со статистикой
- `generate_postman_collection(output_path)` - Postman коллекция

## 🔧 Поддерживаемые LLM провайдеры

### Ollama (Локально)

Бесплатный и приватный вариант.

```python
LLMConfig(
    provider="ollama",
    model="mistral",  # или "llama2", "neural-chat", etc.
    base_url="http://localhost:11434"
)
```

### OpenAI

Требует API ключ.

```python
LLMConfig(
    provider="openai",
    model="gpt-3.5-turbo",  # или "gpt-4"
    api_key="sk-..."
)
```

### Anthropic (Claude)

Требует API ключ.

```python
LLMConfig(
    provider="anthropic",
    model="claude-3-sonnet-20240229",
    api_key="sk-ant-..."
)
```

### HuggingFace

Требует API ключ.

```python
LLMConfig(
    provider="huggingface",
    model="meta-llama/Llama-2-7b-chat-hf",
    api_key="hf_..."
)
```

## 📋 Требования

- Python >= 3.10
- langchain >= 0.1.0
- langchain-core >= 0.1.0
- langchain-community >= 0.0.1
- pyyaml >= 6.0

## 🐛 Решение проблем

### Ollama не подключается

```bash
# Убедитесь, что Ollama запущена
ollama serve

# Проверьте, доступна ли модель
ollama list

# Если модель не установлена
ollama pull mistral
```

### OpenAI API ошибка

```bash
# Проверьте API ключ
export OPENAI_API_KEY="sk-..."

# Проверьте соединение
python -c "from langchain_openai import ChatOpenAI; print('OK')"
```

### Ошибка парсинга OpenAPI

Убедитесь, что файл валидный JSON/YAML:

```python
from utils import load_openapi, OpenAPIValidator

spec = load_openapi("file.json")
is_valid, errors = OpenAPIValidator.is_valid_openapi(spec)

if not is_valid:
    print("Ошибки валидации:")
    for error in errors:
        print(f"  - {error}")
```

## 🤝 Контрибьютинг

Приветствуются pull requests и issues!

## 📄 Лицензия

MIT License

## 🔗 Дополнительные ресурсы

- [OpenAPI Specification](https://spec.openapis.org/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [OpenAI API](https://platform.openai.com/docs/api-reference)

---

**Создано с ❤️ для работы с API документацией**