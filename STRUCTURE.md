# 📂 Структура проекта

## Файловая организация

```
swagger-to-docs/
├── 📄 main.py                      # Базовая реализация (LangChain Chains)
├── 📄 advanced_generator.py        # Продвинутая реализация (LCEL)
├── 📄 config.py                    # Конфигурация LLM и документации
├── 📄 utils.py                     # Утилиты для OpenAPI
├── 📄 cli.py                       # Интерактивный CLI интерфейс
├── 📄 examples.py                  # Примеры использования
├── 📄 test_openapi.py              # Юнит-тесты
│
├── 📋 pyproject.toml               # Конфигурация проекта (pip install)
├── 📋 requirements.txt              # Зависимости (pip install -r)
├── 📋 .env.example                 # Пример файла конфигурации
├── 📋 setup.sh                     # Скрипт для быстрой установки
│
├── 📚 README.md                    # Основная документация
├── 📚 USAGE.md                     # Подробное руководство
├── 📚 STRUCTURE.md                 # Этот файл
│
├── 📁 examples/                    # Примеры OpenAPI файлов
│   ├── petstore.json               # Petstore API (OpenAPI 3.0)
│   ├── petstore-expanded.json      # Расширенный Petstore
│   ├── api.github.com.json         # GitHub API
│   ├── api-with-examples.json      # API с примерами
│   ├── link-example.json           # Пример ссылок
│   ├── tictactoe.json              # Tic-Tac-Toe API
│   └── uspto.json                  # USPTO API
│
├── 📁 docs/                        # (Создается после обработки)
│   └── swagger_petstore/           # Документация для каждого API
│       ├── README.md               # Оглавление
│       ├── tags/                   # Документация по тегам
│       │   ├── pets.md
│       │   ├── other_tag.md
│       │   └── ...
│       └── endpoints/              # Документация по эндпоинтам
│           ├── get_pets.md
│           ├── post_pets.md
│           ├── get_pets_petid.md
│           └── ...
│
└── 📁 exports/                     # (Создается при экспорте)
    ├── petstore_endpoints.csv      # Экспорт в CSV
    ├── petstore_stats.json         # Статистика JSON
    └── petstore_postman.json       # Postman коллекция
```

## Описание основных файлов

### Генераторы документации

#### `main.py`
**Базовая реализация с использованием LangChain Chains**

- Класс `OpenAPIDocumentationGenerator`
- Использует `LLMChain` для генерации
- Методы:
  - `process_openapi_file()` - обработка одного файла
  - `process_directory()` - обработка всей директории
  - `extract_endpoints()` - извлечение эндпоинтов
  - `generate_endpoint_doc()` - генерирование документации
  - `create_index_file()` - создание оглавления

#### `advanced_generator.py`
**Продвинутая реализация с использованием LCEL (LangChain Expression Language)**

- Класс `AdvancedOpenAPIDocGenerator`
- Использует более новый API LangChain
- Лучше структурирована
- Поддерживает многоязычность
- Методы аналогичны `main.py`, но с лучшей организацией

### Конфигурация и утилиты

#### `config.py`
**Конфигурация LLM и документации**

- `LLMConfig` dataclass - конфигурация LLM провайдеров
- `DocumentationConfig` dataclass - настройки документации
- `get_llm_from_config()` - фабрика для создания LLM

Поддерживаемые провайдеры:
- Ollama (локально, бесплатно)
- OpenAI (ChatGPT)
- Anthropic (Claude)
- HuggingFace

#### `utils.py`
**Утилиты для работы с OpenAPI спецификациями**

Классы:
- `OpenAPIValidator` - валидация спецификаций
- `OpenAPIAnalyzer` - анализ спецификаций
- `OpenAPIExporter` - экспорт в разные форматы

Функции:
- `load_openapi()` - загрузка JSON/YAML
- `save_openapi()` - сохранение спецификации

### Интерфейсы

#### `cli.py`
**Интерактивный CLI интерфейс**

- Класс `OpenAPIDocCLI`
- Меню с 6 опциями:
  1. Обработка файлов
  2. Анализ спецификаций
  3. Экспорт данных
  4. Валидация
  5. Конфигурация
  6. Выход

#### `examples.py`
**Примеры использования программного API**

- 5 готовых примеров
- Запуск: `python examples.py <номер>`
- Демонстрирует различные LLM провайдеры

### Документация и конфигурация

#### `README.md`
Основная документация проекта:
- Описание особенностей
- Быстрый старт
- Примеры использования
- API документация
- Решение проблем

#### `USAGE.md`
Подробное руководство:
- Пошаговые инструкции установки
- Использование каждой опции CLI
- Примеры программного использования
- Советы и трюки
- Решение проблем

#### `pyproject.toml`
Конфигурация pip пакета:
- Метаинформация проекта
- Основные зависимости
- Опциональные зависимости для каждого провайдера
- Версия Python

#### `requirements.txt`
Альтернативный способ установки зависимостей

#### `.env.example`
Пример файла конфигурации для переменных окружения:
- API ключи
- Пути к директориям
- Параметры LLM

#### `setup.sh`
Bash скрипт для быстрой установки:
- Проверка Python версии
- Создание виртуального окружения
- Установка зависимостей
- Опциональный запуск CLI

### Примеры и тесты

#### `examples/`
Директория с примерами OpenAPI спецификаций:
- `petstore.json` - простой Petstore API (отличный для обучения)
- `petstore-expanded.json` - расширенная версия
- `api.github.com.json` - GitHub API
- `api-with-examples.json` - API с примерами использования
- `link-example.json` - демонстрирует ссылки между компонентами
- `tictactoe.json` - простая игра
- `uspto.json` - USPTO API (реальный API)

#### `test_openapi.py`
Юнит-тесты:
- Тесты для `OpenAPIValidator`
- Тесты для `OpenAPIAnalyzer`
- Тесты для `OpenAPIExporter`
- Интеграционные тесты

Запуск: `pytest test_openapi.py -v`

## Поток данных

```
OpenAPI файл (JSON/YAML)
        ↓
    [Загрузка]
        ↓
    load_openapi()
        ↓
    Валидация (OpenAPIValidator)
        ↓
    [Анализ] → OpenAPIAnalyzer
        ↓        ├── Статистика
        ↓        ├── Поиск по тегам
        ↓        └── Поиск по методам
        ↓
    [Генерирование] → LLM
        ↓         ├── Промпты
        ↓         ├── Генерация документации
        ↓         └── Форматирование
        ↓
    [Сохранение]
        ↓
    Markdown файлы (docs/)
    ├── tags/*.md
    ├── endpoints/*.md
    └── README.md
```

## Архитектура генератора

### Базовая реализация (main.py)

```
┌─────────────────────────────────────────┐
│  OpenAPIDocumentationGenerator         │
├─────────────────────────────────────────┤
│ - llm: LLM                              │
│ - output_dir: Path                      │
│ - endpoint_chain: LLMChain              │
│ - tag_chain: LLMChain                   │
├─────────────────────────────────────────┤
│ load_openapi_spec()                     │
│ extract_endpoints()                     │
│ group_by_tags()                         │
│ format_operation()                      │
│ generate_endpoint_doc()                 │
│ generate_tag_overview()                 │
│ process_openapi_file()                  │
│ process_directory()                     │
└─────────────────────────────────────────┘
```

### Продвинутая реализация (advanced_generator.py)

```
┌─────────────────────────────────────────┐
│  AdvancedOpenAPIDocGenerator            │
├─────────────────────────────────────────┤
│ - llm: BaseLanguageModel                │
│ - output_dir: Path                      │
│ - language: str                         │
│ - endpoint_chain: LCEL Chain            │
│ - tag_chain: LCEL Chain                 │
│ - overview_chain: LCEL Chain            │
├─────────────────────────────────────────┤
│ load_spec()                             │
│ extract_endpoints()                     │
│ format_operation()                      │
│ get_components_summary()                │
│ get_security_info()                     │
│ process_openapi_file()                  │
│ process_directory()                     │
└─────────────────────────────────────────┘
```

## Расширяемость

### Добавление нового LLM провайдера

1. Добавить в `config.py`:
```python
elif config.provider == "new_provider":
    return NewProviderLLM(...)
```

2. Обновить `LLMConfig.provider` literal

3. Добавить в `pyproject.toml` опциональные зависимости

### Добавление нового формата экспорта

1. Добавить метод в `OpenAPIExporter`:
```python
def export_new_format(self, output_path: str):
    # реализация
```

2. Интегрировать в CLI (cli.py)

### Кастомизация промптов

В `advanced_generator.py` измените шаблоны в `_setup_prompts()`:
```python
endpoint_template = """Ваш кастомный промпт..."""
```

## Зависимости

### Основные
- langchain >= 0.1.0
- langchain-core >= 0.1.0
- langchain-community >= 0.0.1
- pyyaml >= 6.0

### Опциональные
- ollama >= 0.0.1 (для Ollama)
- openai >= 1.0.0 (для OpenAI)
- langchain-openai >= 0.0.1 (для OpenAI)
- anthropic >= 0.7.0 (для Claude)
- langchain-anthropic >= 0.0.1 (для Claude)

### Для разработки
- pytest >= 7.0
- black >= 23.0
- ruff >= 0.0.200

---

Созданный 📅 20 января 2026г.
