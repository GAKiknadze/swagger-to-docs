#!/bin/bash
# Скрипт для быстрого запуска OpenAPI Documentation Generator

set -e

echo "🚀 OpenAPI Documentation Generator Setup"
echo "========================================"
echo ""

# Проверяем Python версию
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python версия: $python_version"

# Создаем виртуальное окружение если его нет
if [ ! -d "venv" ]; then
    echo "📦 Создаю виртуальное окружение..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
fi

# Активируем виртуальное окружение
source venv/bin/activate || . venv/Scripts/activate
echo "✅ Виртуальное окружение активировано"

# Устанавливаем зависимости
echo ""
echo "📥 Установка зависимостей..."
pip install --upgrade pip > /dev/null 2>&1

# Спрашиваем какой провайдер установить
echo ""
echo "Выберите LLM провайдер для установки:"
echo "  1. Ollama (локально, бесплатно)"
echo "  2. OpenAI API"
echo "  3. Anthropic (Claude)"
echo "  4. Все"
echo "  5. Базовые зависимости (без LLM)"

read -p "Выбор (1-5) [5]: " provider_choice
provider_choice=${provider_choice:-5}

case $provider_choice in
    1)
        echo "📦 Установка Ollama..."
        pip install -e ".[ollama]" > /dev/null 2>&1
        echo "✅ Ollama установлена"
        ;;
    2)
        echo "📦 Установка OpenAI..."
        pip install -e ".[openai]" > /dev/null 2>&1
        echo "✅ OpenAI установлена"
        ;;
    3)
        echo "📦 Установка Anthropic..."
        pip install -e ".[anthropic]" > /dev/null 2>&1
        echo "✅ Anthropic установлена"
        ;;
    4)
        echo "📦 Установка всех провайдеров..."
        pip install -e ".[ollama,openai,anthropic]" > /dev/null 2>&1
        echo "✅ Все провайдеры установлены"
        ;;
    *)
        echo "📦 Установка базовых зависимостей..."
        pip install -e . > /dev/null 2>&1
        echo "✅ Базовые зависимости установлены"
        ;;
esac

echo ""
echo "✨ Установка завершена!"
echo ""
echo "🎯 Далее вы можете:"
echo ""
echo "1. 🖥️  Запустить интерактивный CLI:"
echo "   python cli.py"
echo ""
echo "2. 📚 Обработать примеры:"
echo "   python examples.py 1"
echo ""
echo "3. 📖 Прочитать полное руководство:"
echo "   cat USAGE.md"
echo ""
echo "4. 🧪 Запустить тесты:"
echo "   pytest test_openapi.py -v"
echo ""
echo "5. 💻 Запустить основной скрипт:"
echo "   python main.py"
echo ""

# Опционально запустить CLI
read -p "Запустить интерактивный CLI сейчас? (y/n) [n]: " run_cli
if [ "$run_cli" = "y" ]; then
    echo ""
    python cli.py
fi
