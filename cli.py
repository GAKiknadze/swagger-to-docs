#!/usr/bin/env python3
"""Интерактивный CLI для OpenAPI Documentation Generator."""

import sys
import os
from pathlib import Path
from typing import Optional
import json

from config import LLMConfig, DocumentationConfig, get_llm_from_config
from advanced_generator import AdvancedOpenAPIDocGenerator
from utils import (
    load_openapi,
    OpenAPIValidator,
    OpenAPIAnalyzer,
    OpenAPIExporter
)


class OpenAPIDocCLI:
    """Интерактивный CLI инструмент."""
    
    def __init__(self):
        self.config = None
        self.generator = None
    
    def print_header(self):
        """Печатает заголовок."""
        print("\n" + "=" * 70)
        print("📚 OpenAPI to Markdown Documentation Generator")
        print("=" * 70 + "\n")
    
    def print_menu(self):
        """Печатает главное меню."""
        print("Главное меню:")
        print("  1. Обработать OpenAPI файл/директорию")
        print("  2. Анализировать OpenAPI спецификацию")
        print("  3. Экспортировать в разные форматы")
        print("  4. Валидировать OpenAPI файл")
        print("  5. Настроить конфигурацию")
        print("  6. Выход")
        print()
    
    def configure_llm(self) -> Optional[LLMConfig]:
        """Интерактивная конфигурация LLM."""
        print("\n🤖 Конфигурация LLM провайдера")
        print("-" * 40)
        
        providers = {
            "1": "ollama",
            "2": "openai",
            "3": "anthropic",
            "4": "huggingface"
        }
        
        print("Доступные провайдеры:")
        for key, provider in providers.items():
            print(f"  {key}. {provider}")
        
        choice = input("\nВыберите провайдер (1-4): ").strip()
        
        if choice not in providers:
            print("❌ Неверный выбор")
            return None
        
        provider = providers[choice]
        
        models = {
            "ollama": ["mistral", "llama2", "neural-chat"],
            "openai": ["gpt-3.5-turbo", "gpt-4"],
            "anthropic": ["claude-3-sonnet-20240229", "claude-3-opus-20240229"],
            "huggingface": ["meta-llama/Llama-2-7b-chat-hf"]
        }
        
        print(f"\nДоступные модели для {provider}:")
        available_models = models.get(provider, [])
        for i, model in enumerate(available_models, 1):
            print(f"  {i}. {model}")
        
        model_choice = input("\nВыберите модель или введите свою: ").strip()
        
        if model_choice.isdigit() and 1 <= int(model_choice) <= len(available_models):
            model = available_models[int(model_choice) - 1]
        else:
            model = model_choice or available_models[0]
        
        config = LLMConfig(provider=provider, model=model)
        
        if provider != "ollama":
            api_key = input(f"Введите API ключ для {provider}: ").strip()
            if api_key:
                config.api_key = api_key
            else:
                print("⚠️  API ключ не введен, попробуем использовать переменную окружения")
        
        return config
    
    def process_files(self):
        """Обработать OpenAPI файлы."""
        print("\n📄 Обработка OpenAPI файлов")
        print("-" * 40)
        
        if not self.generator:
            print("❌ Генератор не инициализирован. Сначала настройте конфигурацию.")
            return
        
        input_path = input("Введите путь к файлу или директории (examples): ").strip() or "examples"
        
        path = Path(input_path)
        
        if not path.exists():
            print(f"❌ Путь не найден: {input_path}")
            return
        
        try:
            if path.is_file():
                print(f"\n✅ Обработка файла: {path}")
                self.generator.process_openapi_file(str(path))
            else:
                print(f"\n✅ Обработка директории: {path}")
                self.generator.process_directory(str(path))
            
            print("\n✨ Документация успешно создана!")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def analyze_file(self):
        """Анализировать OpenAPI файл."""
        print("\n📊 Анализ OpenAPI спецификации")
        print("-" * 40)
        
        file_path = input("Введите путь к OpenAPI файлу: ").strip()
        
        if not Path(file_path).exists():
            print(f"❌ Файл не найден: {file_path}")
            return
        
        try:
            spec = load_openapi(file_path)
            analyzer = OpenAPIAnalyzer(spec)
            
            # Валидация
            is_valid, errors = OpenAPIValidator.is_valid_openapi(spec)
            
            if is_valid:
                print("✅ OpenAPI спецификация валидна\n")
            else:
                print("⚠️  Найдены ошибки валидации:")
                for error in errors:
                    print(f"   - {error}")
                print()
            
            # Статистика
            stats = analyzer.get_statistics()
            
            print("📈 Статистика:")
            print(f"   Название: {stats['title']}")
            print(f"   Версия: {stats['version']}")
            print(f"   Всего эндпоинтов: {stats['total_endpoints']}")
            print(f"   Методы: {stats['methods']}")
            print(f"   Теги: {len(stats['tags'])}")
            print(f"   Схемы: {stats['schemas']}")
            print(f"   Схемы безопасности: {stats['security_schemes']}")
            
            print("\n🏷️  Теги и их эндпоинты:")
            for tag, count in sorted(stats['tags'].items()):
                print(f"   - {tag}: {count} эндпоинтов")
            
            # Дополнительная информация
            print("\n🔐 Схемы безопасности:")
            security_schemes = analyzer.get_security_schemes()
            if security_schemes:
                for name, scheme in security_schemes.items():
                    print(f"   - {name}: {scheme.get('type', 'unknown')}")
            else:
                print("   Нет определенных схем")
            
            # Опция для просмотра эндпоинтов
            show_endpoints = input("\nПоказать все эндпоинты? (y/n): ").strip().lower()
            if show_endpoints == 'y':
                endpoints = analyzer.list_all_endpoints()
                for ep in endpoints:
                    tags_str = ", ".join(ep['tags']) if ep['tags'] else "untagged"
                    print(f"   {ep['method']:6} {ep['path']:30} [{tags_str}]")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def export_data(self):
        """Экспортировать данные в разные форматы."""
        print("\n💾 Экспорт данных")
        print("-" * 40)
        
        file_path = input("Введите путь к OpenAPI файлу: ").strip()
        
        if not Path(file_path).exists():
            print(f"❌ Файл не найден: {file_path}")
            return
        
        try:
            spec = load_openapi(file_path)
            exporter = OpenAPIExporter(spec)
            
            print("\nДоступные форматы экспорта:")
            print("  1. CSV (список эндпоинтов)")
            print("  2. JSON (статистика)")
            print("  3. Postman коллекция")
            print("  4. Все форматы")
            
            choice = input("\nВыберите формат (1-4): ").strip()
            
            output_dir = "exports"
            Path(output_dir).mkdir(exist_ok=True)
            
            if choice in ["1", "4"]:
                csv_file = Path(output_dir) / f"{Path(file_path).stem}_endpoints.csv"
                exporter.export_endpoints_csv(str(csv_file))
                print(f"✅ CSV экспортирован в {csv_file}")
            
            if choice in ["2", "4"]:
                json_file = Path(output_dir) / f"{Path(file_path).stem}_stats.json"
                exporter.export_statistics_json(str(json_file))
                print(f"✅ JSON экспортирован в {json_file}")
            
            if choice in ["3", "4"]:
                postman_file = Path(output_dir) / f"{Path(file_path).stem}_postman.json"
                exporter.generate_postman_collection(str(postman_file))
                print(f"✅ Postman коллекция экспортирована в {postman_file}")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def validate_file(self):
        """Валидировать OpenAPI файл."""
        print("\n✔️  Валидация OpenAPI файла")
        print("-" * 40)
        
        file_path = input("Введите путь к OpenAPI файлу: ").strip()
        
        if not Path(file_path).exists():
            print(f"❌ Файл не найден: {file_path}")
            return
        
        try:
            spec = load_openapi(file_path)
            is_valid, errors = OpenAPIValidator.is_valid_openapi(spec)
            
            if is_valid:
                print("\n✅ OpenAPI спецификация ВАЛИДНА!")
                print(f"   Название: {spec.get('info', {}).get('title', 'Unknown')}")
                print(f"   Версия: {spec.get('info', {}).get('version', 'Unknown')}")
            else:
                print("\n❌ НАЙДЕНЫ ОШИБКИ ВАЛИДАЦИИ:\n")
                for i, error in enumerate(errors, 1):
                    print(f"{i}. {error}")
        
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка парсинга JSON: {e}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def configure(self):
        """Настроить конфигурацию."""
        print("\n⚙️  Конфигурация")
        print("-" * 40)
        
        llm_config = self.configure_llm()
        
        if not llm_config:
            print("❌ Конфигурация LLM не удалась")
            return
        
        language = input("\nВыберите язык документации (ru/en) [ru]: ").strip() or "ru"
        output_dir = input("Выберите директорию для выходных файлов [docs]: ").strip() or "docs"
        
        try:
            llm = get_llm_from_config(llm_config)
            self.generator = AdvancedOpenAPIDocGenerator(
                llm,
                output_dir=output_dir,
                language=language
            )
            
            print(f"\n✅ Конфигурация успешно установлена!")
            print(f"   LLM провайдер: {llm_config.provider}")
            print(f"   Модель: {llm_config.model}")
            print(f"   Язык: {language}")
            print(f"   Выходная директория: {output_dir}")
        
        except Exception as e:
            print(f"❌ Ошибка при инициализации генератора: {e}")
    
    def run(self):
        """Запустить интерактивный CLI."""
        self.print_header()
        
        # Попробуем инициализировать с конфигурацией по умолчанию
        try:
            llm_config = LLMConfig()
            llm = get_llm_from_config(llm_config)
            self.generator = AdvancedOpenAPIDocGenerator(llm)
            print("✅ Инициализирован с конфигурацией по умолчанию (Ollama)\n")
        except Exception as e:
            print(f"⚠️  Не удалось инициализировать с конфигурацией по умолчанию: {e}")
            print("   Пожалуйста, настройте конфигурацию вручную\n")
        
        while True:
            self.print_menu()
            
            choice = input("Выберите опцию (1-6): ").strip()
            
            if choice == "1":
                self.process_files()
            elif choice == "2":
                self.analyze_file()
            elif choice == "3":
                self.export_data()
            elif choice == "4":
                self.validate_file()
            elif choice == "5":
                self.configure()
            elif choice == "6":
                print("\n👋 До встречи!\n")
                sys.exit(0)
            else:
                print("❌ Неверный выбор, попробуйте снова\n")


def main():
    """Главная функция."""
    cli = OpenAPIDocCLI()
    cli.run()


if __name__ == "__main__":
    main()
