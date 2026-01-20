#!/usr/bin/env python3
"""
🚀 OpenAPI to Markdown Documentation Generator v0.1.0

Полный LangChain скрипт для преобразования OpenAPI/Swagger спецификаций 
в профессиональную документацию на Markdown с разделением по тегам и эндпоинтам.

📂 Созданные файлы:

ОСНОВНОЕ:
├── main.py                      - Базовая реализация с LangChain Chains
├── advanced_generator.py        - Продвинутая реализация с LCEL
├── config.py                    - Конфигурация LLM провайдеров
├── utils.py                     - Утилиты для анализа OpenAPI
├── cli.py                       - Интерактивный CLI интерфейс
├── examples.py                  - Готовые примеры использования

КОНФИГУРАЦИЯ И УСТАНОВКА:
├── pyproject.toml               - Конфигурация pip пакета
├── requirements.txt             - Зависимости (альтернатива pip install -e)
├── .env.example                 - Пример переменных окружения
├── setup.sh                     - Скрипт автоматической установки

ДОКУМЕНТАЦИЯ:
├── README.md                    - Полная документация
├── USAGE.md                     - Подробное руководство
├── QUICKSTART.md                - Быстрая справка
├── STRUCTURE.md                 - Структура проекта
├── CHANGELOG.md                 - История изменений

ТЕСТИРОВАНИЕ:
└── test_openapi.py              - Юнит-тесты

═══════════════════════════════════════════════════════════════════════════════

🎯 ЧТО РЕАЛИЗОВАНО:

1️⃣  ДВА ПОДХОДА К ГЕНЕРАЦИИ:
   • main.py - использует LangChain Chains (классический подход)
   • advanced_generator.py - использует LCEL (современный подход)

2️⃣  ПОДДЕРЖКА МНОЖЕСТВА LLM:
   • Ollama (локально, бесплатно, приватно)
   • OpenAI (GPT-3.5, GPT-4)
   • Anthropic (Claude)
   • HuggingFace (Llama и другие)

3️⃣  ПОЛНЫЙ ЦИКЛ ОБРАБОТКИ:
   • Загрузка OpenAPI файлов (JSON и YAML)
   • Валидация спецификаций
   • Анализ и группировка по тегам
   • Генерирование Markdown документации
   • Создание структурированной файловой иерархии

4️⃣  СТРУКТУРИРОВАННАЯ ДОКУМЕНТАЦИЯ:
   • Отдельный файл для каждого тега (категории эндпоинтов)
   • Отдельный файл для каждого эндпоинта
   • Автоматическое оглавление
   • Перекрестные ссылки

5️⃣  ИНТЕРАКТИВНЫЙ CLI:
   • Меню с 6 опциями
   • Интерактивная конфигурация LLM
   • Валидация файлов
   • Анализ спецификаций
   • Экспорт в разные форматы

6️⃣  АНАЛИЗ И ЭКСПОРТ:
   • Статистика по API
   • Поиск по тегам и методам
   • Экспорт в CSV
   • Экспорт статистики в JSON
   • Генерирование Postman коллекций

7️⃣  МНОГОЯЗЫЧНОСТЬ:
   • Документация на русском (по умолчанию)
   • Поддержка английского языка
   • Легко добавлять новые языки

8️⃣  ГОТОВЫЕ ПРИМЕРЫ:
   • Petstore API (простой пример)
   • GitHub API (реальный API)
   • USPTO API (большой API)
   • И другие примеры OpenAPI

═══════════════════════════════════════════════════════════════════════════════

🚀 БЫСТРЫЙ СТАРТ:

1. Установка:
   bash setup.sh

2. Использование (интерактивно):
   python cli.py

3. Обработка примера:
   python examples.py 1

═══════════════════════════════════════════════════════════════════════════════

📊 ПРИМЕРЫ ВЫХОДНЫХ ФАЙЛОВ:

docs/swagger_petstore/
├── README.md                    # Оглавление с полной таблицей
├── tags/
│   └── pets.md                 # Документация для тега "pets"
└── endpoints/
    ├── get_pets.md             # GET /pets
    ├── post_pets.md            # POST /pets
    └── get_pets_petid.md       # GET /pets/{petId}

Каждый файл содержит:
- Описание эндпоинта/тега
- Параметры запроса
- Request Body (если требуется)
- Возможные ответы с кодами статуса
- Примеры curl запросов
- Описание ошибок

═══════════════════════════════════════════════════════════════════════════════

🔧 ОСНОВНЫЕ КЛАССЫ:

OpenAPIDocumentationGenerator (main.py)
├── load_openapi_spec()         - Загрузка JSON файлов
├── extract_endpoints()         - Извлечение эндпоинтов
├── group_by_tags()            - Группировка по тегам
├── generate_endpoint_doc()    - Генерирование документации
└── process_directory()        - Обработка всей директории

AdvancedOpenAPIDocGenerator (advanced_generator.py)
├── load_spec()               - Загрузка JSON/YAML
├── extract_endpoints()       - Извлечение эндпоинтов
├── process_openapi_file()   - Обработка одного файла
└── process_directory()      - Обработка директории

OpenAPIAnalyzer (utils.py)
├── get_statistics()         - Получить статистику
├── find_endpoints_by_tag()  - Поиск по тегу
├── find_endpoints_by_method()  - Поиск по методу HTTP
├── list_all_endpoints()    - Список всех эндпоинтов
└── get_all_schemas()       - Получить все схемы

OpenAPIExporter (utils.py)
├── export_endpoints_csv()       - Экспорт в CSV
├── export_statistics_json()     - Статистика в JSON
└── generate_postman_collection()  - Postman коллекция

OpenAPIDocCLI (cli.py)
├── configure_llm()         - Конфигурирование LLM
├── process_files()        - Обработка файлов
├── analyze_file()         - Анализ спецификации
├── export_data()         - Экспорт данных
├── validate_file()       - Валидация файла
└── run()                - Главный цикл CLI

═══════════════════════════════════════════════════════════════════════════════

🛠️  КОНФИГУРАЦИЯ:

LLMConfig:
├── provider    - Провайдер (ollama, openai, anthropic, huggingface)
├── model       - Название модели
├── api_key     - API ключ (если требуется)
├── base_url    - URL для Ollama
├── temperature - Температура для LLM (0.0-1.0)
└── max_tokens  - Максимум токенов в ответе

DocumentationConfig:
├── output_dir  - Директория для выходных файлов
├── input_dir   - Директория с OpenAPI файлами
├── language    - Язык документации (ru/en)
├── include_examples  - Включать примеры
├── include_schemas   - Включать схемы
└── include_security  - Включать информацию о безопасности

═══════════════════════════════════════════════════════════════════════════════

📋 ФАЙЛОВЫЕ СТРУКТУРЫ:

Входные файлы (examples/):
- petstore.json
- petstore-expanded.json
- api.github.com.json
- api-with-examples.json
- link-example.json
- tictactoe.json
- uspto.json

Выходные файлы (docs/<api_name>/):
- README.md                      # Оглавление
- tags/<tag_name>.md            # Документация по тегам
- endpoints/<method>_<path>.md  # Документация по эндпоинтам

Экспортированные файлы (exports/):
- <api>_endpoints.csv           # CSV с эндпоинтами
- <api>_stats.json              # Статистика JSON
- <api>_postman.json            # Postman коллекция

═══════════════════════════════════════════════════════════════════════════════

🔄 РАБОЧИЙ ПРОЦЕСС:

1. Загрузка OpenAPI файла
   ↓
2. Валидация спецификации
   ↓
3. Извлечение эндпоинтов
   ↓
4. Группировка по тегам
   ↓
5. Для каждого тега:
   - Генерирование обзорной документации
   - Создание файла tags/<tag>.md
   ↓
6. Для каждого эндпоинта:
   - Форматирование операции
   - Извлечение информации о безопасности
   - Генерирование документации через LLM
   - Создание файла endpoints/<method>_<path>.md
   ↓
7. Создание главного файла README.md с оглавлением

═══════════════════════════════════════════════════════════════════════════════

💡 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

Пример 1: Базовое использование
from advanced_generator import AdvancedOpenAPIDocGenerator
from config import LLMConfig, get_llm_from_config

llm = get_llm_from_config(LLMConfig())
gen = AdvancedOpenAPIDocGenerator(llm)
gen.process_directory("examples")

Пример 2: Анализ спецификации
from utils import load_openapi, OpenAPIAnalyzer

spec = load_openapi("examples/petstore.json")
analyzer = OpenAPIAnalyzer(spec)
stats = analyzer.get_statistics()
print(f"Всего эндпоинтов: {stats['total_endpoints']}")

Пример 3: Экспорт в разные форматы
from utils import load_openapi, OpenAPIExporter

spec = load_openapi("examples/petstore.json")
exporter = OpenAPIExporter(spec)
exporter.export_endpoints_csv("endpoints.csv")
exporter.generate_postman_collection("postman.json")

Пример 4: Использование с OpenAI
from config import LLMConfig, get_llm_from_config

llm = get_llm_from_config(
    LLMConfig(provider="openai", model="gpt-4", api_key="sk-...")
)
gen = AdvancedOpenAPIDocGenerator(llm)
gen.process_directory("examples")

═══════════════════════════════════════════════════════════════════════════════

🌍 ПОДДЕРЖИВАЕМЫЕ LLM:

Ollama (http://localhost:11434)
├── mistral          - Быстрая, хорошее качество
├── llama2           - Стабильная, универсальная
├── neural-chat      - Для чатов
└── другие модели доступны

OpenAI
├── gpt-3.5-turbo    - Быстрая, дешевая
└── gpt-4            - Лучшее качество, дороже

Anthropic
├── claude-3-sonnet  - Баланс качества и скорости
├── claude-3-opus    - Лучшее качество, медленнее
└── claude-3-haiku   - Быстрая, упрощенная

HuggingFace
├── meta-llama/Llama-2-7b-chat-hf
├── mistralai/Mistral-7B-Instruct-v0.2
└── другие модели

═══════════════════════════════════════════════════════════════════════════════

📚 ДОКУМЕНТАЦИЯ:

README.md
├── Описание особенностей
├── Быстрый старт
├── Примеры использования
├── API документация
├── Решение проблем
└── Ссылки на ресурсы

USAGE.md
├── Установка
├── Использование CLI
├── Программное использование
├── 6 полных примеров
├── Советы и трюки
└── Решение проблем

QUICKSTART.md
├── Установка за 30 секунд
├── Запуск за 10 секунд
├── Основные команды
├── Частые вопросы
└── Горячие клавиши

STRUCTURE.md
├── Файловая структура
├── Описание каждого модуля
├── Диаграммы архитектуры
├── Поток данных
└── Расширяемость

═══════════════════════════════════════════════════════════════════════════════

✅ ТЕСТИРОВАНИЕ:

Юнит-тесты (test_openapi.py):
├── TestOpenAPIValidator    - Валидация спецификаций
├── TestOpenAPIAnalyzer     - Анализ спецификаций
├── TestOpenAPIExporter     - Экспорт данных
└── TestIntegration         - Интеграционные тесты

Запуск:
pytest test_openapi.py -v

═══════════════════════════════════════════════════════════════════════════════

🎁 ГОТОВЫЕ ПРИМЕРЫ (examples.py):

1. Ollama (локально, бесплатно)
   python examples.py 1

2. OpenAI GPT-3.5/GPT-4
   python examples.py 2

3. Claude (Anthropic)
   python examples.py 3

4. Документация на английском
   python examples.py 4

5. Обработка конкретных файлов
   python examples.py 5

═══════════════════════════════════════════════════════════════════════════════

🚀 РАЗВЕРТЫВАНИЕ:

Как Python пакет:
pip install -e .

С опциональными зависимостями:
pip install -e ".[ollama]"      # Ollama
pip install -e ".[openai]"      # OpenAI
pip install -e ".[anthropic]"   # Claude
pip install -e ".[ollama,openai,anthropic]"  # Все

Через requirements.txt:
pip install -r requirements.txt

═══════════════════════════════════════════════════════════════════════════════

🔮 БУДУЩИЕ УЛУЧШЕНИЯ:

v0.2.0:
- HTML выход
- Генерирование диаграмм
- Streaming для длинных генераций
- Кеширование результатов
- Web UI

v0.3.0:
- GraphQL поддержка
- gRPC документация
- API diff генерирование
- Интерактивный API explorer

v1.0.0:
- Стабильный API
- Полное покрытие тестами
- Оптимизация производительности
- Энтерпрайз функции

═══════════════════════════════════════════════════════════════════════════════

📞 ПОДДЕРЖКА:

Проблемы: Откройте issue на GitHub
Вопросы: Посмотрите документацию или примеры
Вклад: Приветствуются pull requests

═══════════════════════════════════════════════════════════════════════════════

Создано: 20 января 2026 г.
Версия: 0.1.0
Лицензия: BSD 3-Clause
"""

print(__doc__)
