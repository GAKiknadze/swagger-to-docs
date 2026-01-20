# 🚀 Быстрая справка

## Установка за 30 секунд

```bash
# 1. Клонируем или переходим в директорию
cd swagger-to-docs

# 2. Запускаем скрипт установки
bash setup.sh

# 3. Выбираем провайдер (рекомендуется Ollama)
```

## Запуск за 10 секунд

```bash
# Интерактивный CLI (самый простой)
python cli.py

# Или примеры
python examples.py 1
```

## Основные команды

### Обработка OpenAPI файлов

```bash
# Интерактивно
python cli.py
# → Опция 1 → Путь к файлу/директории

# Программно
python -c "
from config import LLMConfig, get_llm_from_config
from advanced_generator import AdvancedOpenAPIDocGenerator

llm = get_llm_from_config(LLMConfig())
gen = AdvancedOpenAPIDocGenerator(llm)
gen.process_directory('examples')
"
```

### Анализ спецификации

```bash
# Интерактивно
python cli.py
# → Опция 2 → Путь к файлу

# Программно
python -c "
from utils import load_openapi, OpenAPIAnalyzer

spec = load_openapi('examples/petstore.json')
analyzer = OpenAPIAnalyzer(spec)
print(analyzer.get_statistics())
"
```

### Экспорт данных

```bash
# Интерактивно
python cli.py
# → Опция 3 → Выбрать формат

# Программно
python -c "
from utils import load_openapi, OpenAPIExporter

spec = load_openapi('examples/petstore.json')
exporter = OpenAPIExporter(spec)
exporter.export_endpoints_csv('endpoints.csv')
exporter.generate_postman_collection('postman.json')
"
```

### Валидация файла

```bash
# Интерактивно
python cli.py
# → Опция 4 → Путь к файлу

# Программно
python -c "
from utils import load_openapi, OpenAPIValidator

spec = load_openapi('examples/petstore.json')
is_valid, errors = OpenAPIValidator.is_valid_openapi(spec)
print('Valid!' if is_valid else f'Errors: {errors}')
"
```

## Конфигурация

### Через .env файл

```bash
# Скопировать пример
cp .env.example .env

# Отредактировать
nano .env
```

### Переменные окружения

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export OLLAMA_BASE_URL="http://localhost:11434"
```

## Примеры использования

### Пример 1: Ollama (локально)

```bash
# Убедиться, что Ollama запущена
ollama serve

# В другом терминале
python cli.py
# Выбрать опцию 1 → examples
```

### Пример 2: OpenAI API

```bash
export OPENAI_API_KEY="sk-..."
python examples.py 2
```

### Пример 3: Claude (Anthropic)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python examples.py 3
```

### Пример 4: Обработка конкретного файла

```python
from advanced_generator import AdvancedOpenAPIDocGenerator
from config import LLMConfig, get_llm_from_config

llm = get_llm_from_config(LLMConfig())
gen = AdvancedOpenAPIDocGenerator(llm)
gen.process_openapi_file("examples/petstore.json")
```

## Структура выхода

```
docs/
├── swagger_petstore/              # Для каждого API файла
│   ├── README.md                  # Оглавление с таблицей
│   ├── tags/                      # Документация по тегам
│   │   └── pets.md                # GET /pets, POST /pets, etc
│   └── endpoints/                 # Документация по эндпоинтам
│       ├── get_pets.md            # GET /pets
│       ├── post_pets.md           # POST /pets
│       └── get_pets_petid.md      # GET /pets/{petId}
```

## Поддерживаемые LLM

| Провайдер | Модели | Локально | Бесплатно | Качество |
|-----------|--------|----------|-----------|----------|
| Ollama | mistral, llama2, neural-chat | ✅ | ✅ | ⭐⭐⭐ |
| OpenAI | GPT-3.5, GPT-4 | ❌ | ❌ | ⭐⭐⭐⭐⭐ |
| Anthropic | Claude 3 | ❌ | ❌ | ⭐⭐⭐⭐ |
| HuggingFace | Llama, Mistral | ❌ | ✅ | ⭐⭐⭐ |

## Рекомендации

### Для начинающих
- Используйте `python cli.py` (интерактивный интерфейс)
- Установите Ollama для локального использования
- Начните с примера `petstore.json`

### Для опытных
- Используйте `advanced_generator.py` напрямую
- Кастомизируйте промпты в конфигурации
- Интегрируйте в ваш workflow

### Для высоконагруженных систем
- Обрабатывайте файлы отдельно, не всю директорию
- Используйте более быстрые модели (mistral вместо gpt-4)
- Уменьшайте max_tokens

## Решение проблем

### Ollama не работает
```bash
ollama serve
ollama pull mistral
```

### OpenAI не работает
```bash
export OPENAI_API_KEY="sk-..."
python -c "from langchain_openai import ChatOpenAI; print('OK')"
```

### Ошибка памяти
```python
LLMConfig(max_tokens=1000)  # Уменьшить
LLMConfig(model="mistral")  # Более легкая модель
```

### Ошибка парсинга JSON
```bash
# Проверить валидность
python cli.py
# Опция 4: Валидировать файл
```

## Тестирование

```bash
# Запустить все тесты
pytest test_openapi.py -v

# Запустить конкретный тест
pytest test_openapi.py::TestOpenAPIAnalyzer::test_get_statistics -v

# С покрытием
pytest test_openapi.py --cov=. --cov-report=html
```

## Полезные ссылки

- 📖 [Полная документация](README.md)
- 🎓 [Подробное руководство](USAGE.md)
- 🏗️ [Структура проекта](STRUCTURE.md)
- 🔗 [OpenAPI Spec](https://spec.openapis.org/)
- 🦜 [LangChain Docs](https://python.langchain.com/)
- 🐘 [Ollama GitHub](https://github.com/ollama/ollama)

## Горячие клавиши CLI

| Клавиша | Действие |
|---------|----------|
| `1` | Обработать файлы |
| `2` | Анализировать |
| `3` | Экспортировать |
| `4` | Валидировать |
| `5` | Конфигурация |
| `6` | Выход |

## Частые вопросы

**Q: Нужно ли подключение к интернету?**
A: Нет, если используете Ollama. Да, если используете OpenAI/Claude.

**Q: Сколько это стоит?**
A: Бесплатно с Ollama. С OpenAI/Claude зависит от использования.

**Q: Какая модель лучше?**
A: Для начинающих - mistral. Для лучшего качества - gpt-4.

**Q: Можно ли использовать offline?**
A: Да, с Ollama.

**Q: Поддерживается ли YAML?**
A: Да, автоматически.

**Q: Можно ли экспортировать в HTML?**
A: Нет, только Markdown. HTML можно сгенерировать из Markdown.

---

**Версия:** 0.1.0  
**Последнее обновление:** 20 января 2026 г.
