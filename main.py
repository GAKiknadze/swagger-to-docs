import json
import os
from pathlib import Path
from typing import Optional
from collections import defaultdict

from langchain_core.language_models.llm import LLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama  # или другой LLM провайдер


class OpenAPIDocumentationGenerator:
    """Генератор документации из OpenAPI спецификаций с использованием LangChain."""
    
    def __init__(self, llm: LLM, output_dir: str = "docs"):
        """
        Args:
            llm: Language model для генерации документации
            output_dir: Директория для сохранения документации
        """
        self.llm = llm
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Промпт для генерации документации по эндпоинту
        self.endpoint_prompt = PromptTemplate(
            input_variables=["path", "method", "operation", "components"],
            template="""Создай детальную документацию на русском языке для REST API эндпоинта:

Путь: {path}
Метод: {method}

Информация об операции:
{operation}

Доступные компоненты (схемы):
{components}

Документация должна включать:
1. Описание эндпоинта
2. Параметры (path, query, header)
3. Request body (если требуется)
4. Возможные ответы с кодами статуса
5. Примеры использования curl

Формат: Markdown"""
        )
        
        # Промпт для создания обзора по тегу
        self.tag_prompt = PromptTemplate(
            input_variables=["tag", "endpoints", "description"],
            template="""Создай обзорную документацию для группы API эндпоинтов:

Тег/категория: {tag}
Описание: {description}

Эндпоинты в этой группе:
{endpoints}

Создай структурированный обзор включающий:
1. Общее описание функциональности
2. Краткий список всех эндпоинтов
3. Рекомендации по использованию
4. Аутентификация (если требуется)

Формат: Markdown"""
        )
        
        self.endpoint_chain = LLMChain(llm=self.llm, prompt=self.endpoint_prompt)
        self.tag_chain = LLMChain(llm=self.llm, prompt=self.tag_prompt)
    
    def load_openapi_spec(self, file_path: str) -> dict:
        """Загружает OpenAPI спецификацию из JSON файла."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_endpoints(self, spec: dict) -> dict:
        """Извлекает информацию об эндпоинтах из спецификации."""
        endpoints = {}
        paths = spec.get("paths", {})
        
        for path, path_item in paths.items():
            if isinstance(path_item, dict):
                for method, operation in path_item.items():
                    if method in ["get", "post", "put", "delete", "patch", "head", "options"]:
                        key = f"{method.upper()} {path}"
                        endpoints[key] = {
                            "path": path,
                            "method": method.upper(),
                            "operation": operation,
                            "tags": operation.get("tags", ["Другое"])
                        }
        
        return endpoints
    
    def group_by_tags(self, endpoints: dict) -> dict:
        """Группирует эндпоинты по тегам."""
        grouped = defaultdict(list)
        for key, endpoint in endpoints.items():
            for tag in endpoint.get("tags", ["Другое"]):
                grouped[tag].append({
                    "key": key,
                    "path": endpoint["path"],
                    "method": endpoint["method"],
                    "operation": endpoint["operation"]
                })
        return dict(grouped)
    
    def format_operation(self, operation: dict) -> str:
        """Форматирует информацию об операции в читаемый вид."""
        lines = []
        
        if "summary" in operation:
            lines.append(f"**Описание:** {operation['summary']}")
        if "description" in operation:
            lines.append(f"**Подробно:** {operation['description']}")
        
        if "parameters" in operation:
            lines.append("\n**Параметры:**")
            for param in operation["parameters"]:
                param_type = param.get("in", "")
                required = "✓" if param.get("required", False) else "✗"
                lines.append(f"- {param['name']} ({param_type}) [{required}]: {param.get('description', '')}")
        
        if "requestBody" in operation:
            lines.append("\n**Request Body:**")
            lines.append(json.dumps(operation["requestBody"], indent=2, ensure_ascii=False))
        
        if "responses" in operation:
            lines.append("\n**Responses:**")
            for status, response in operation["responses"].items():
                lines.append(f"- {status}: {response.get('description', '')}")
        
        return "\n".join(lines)
    
    def format_components(self, spec: dict) -> str:
        """Форматирует компоненты/схемы из спецификации."""
        components = spec.get("components", {})
        if not components:
            return "Нет определенных компонентов"
        
        lines = []
        if "schemas" in components:
            lines.append("**Схемы:**")
            for schema_name in list(components["schemas"].keys())[:10]:  # Первые 10
                lines.append(f"- {schema_name}")
        
        return "\n".join(lines) if lines else "Нет определенных компонентов"
    
    def generate_endpoint_doc(self, key: str, endpoint: dict, spec: dict) -> str:
        """Генерирует документацию для одного эндпоинта с помощью LLM."""
        operation = endpoint["operation"]
        
        doc = self.endpoint_chain.run(
            path=endpoint["path"],
            method=endpoint["method"],
            operation=json.dumps(operation, indent=2, ensure_ascii=False),
            components=self.format_components(spec)
        )
        
        return doc
    
    def generate_tag_overview(self, tag: str, endpoints: list, spec: dict) -> str:
        """Генерирует обзорную документацию по тегу."""
        endpoints_list = "\n".join([
            f"- **{ep['method']}** {ep['path']}: {ep['operation'].get('summary', 'No summary')}"
            for ep in endpoints
        ])
        
        # Получаем описание тега из спецификации, если есть
        tags_info = spec.get("tags", [])
        tag_description = next(
            (t.get("description", "") for t in tags_info if t.get("name") == tag),
            ""
        )
        
        doc = self.tag_chain.run(
            tag=tag,
            endpoints=endpoints_list,
            description=tag_description or "Нет описания"
        )
        
        return doc
    
    def create_directory_structure(self, spec: dict) -> Path:
        """Создает структуру директорий для документации."""
        spec_name = spec.get("info", {}).get("title", "api").lower().replace(" ", "_")
        spec_dir = self.output_dir / spec_name
        spec_dir.mkdir(exist_ok=True)
        
        tags_dir = spec_dir / "tags"
        tags_dir.mkdir(exist_ok=True)
        
        endpoints_dir = spec_dir / "endpoints"
        endpoints_dir.mkdir(exist_ok=True)
        
        return spec_dir
    
    def sanitize_filename(self, text: str) -> str:
        """Преобразует текст в безопасное имя файла."""
        import re
        text = text.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
        text = re.sub(r'[^a-z0-9_]', '', text)
        return text
    
    def process_openapi_file(self, file_path: str):
        """Обрабатывает один OpenAPI файл и создает документацию."""
        print(f"Обработка файла: {file_path}")
        
        # Загружаем спецификацию
        spec = self.load_openapi_spec(file_path)
        spec_name = spec.get("info", {}).get("title", "API")
        
        # Создаем структуру директорий
        spec_dir = self.create_directory_structure(spec)
        
        # Извлекаем эндпоинты
        endpoints = self.extract_endpoints(spec)
        grouped = self.group_by_tags(endpoints)
        
        print(f"Найдено {len(endpoints)} эндпоинтов в {len(grouped)} тегах")
        
        # Генерируем документацию для каждого тега
        for tag, tag_endpoints in grouped.items():
            print(f"  Обработка тега: {tag}")
            
            # Генерируем обзор по тегу
            try:
                tag_doc = self.generate_tag_overview(tag, tag_endpoints, spec)
                tag_filename = self.sanitize_filename(tag)
                tag_file = spec_dir / "tags" / f"{tag_filename}.md"
                
                with open(tag_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {tag}\n\n")
                    f.write(tag_doc)
                
                print(f"    ✓ Создан: {tag_file.relative_to(Path.cwd())}")
            except Exception as e:
                print(f"    ✗ Ошибка при обработке тега: {e}")
            
            # Генерируем документацию для каждого эндпоинта в теге
            for endpoint_info in tag_endpoints:
                try:
                    endpoint_doc = self.generate_endpoint_doc(
                        endpoint_info["key"],
                        endpoint_info,
                        spec
                    )
                    
                    # Создаем имя файла из метода и пути
                    method = endpoint_info["method"].lower()
                    path_part = self.sanitize_filename(endpoint_info["path"])
                    endpoint_filename = f"{method}_{path_part}"
                    
                    endpoint_file = spec_dir / "endpoints" / f"{endpoint_filename}.md"
                    
                    with open(endpoint_file, 'w', encoding='utf-8') as f:
                        f.write(f"# {endpoint_info['method']} {endpoint_info['path']}\n\n")
                        f.write(f"**Тег:** {tag}\n\n")
                        f.write(endpoint_doc)
                    
                    print(f"    ✓ Эндпоинт: {endpoint_filename}.md")
                
                except Exception as e:
                    print(f"    ✗ Ошибка при обработке эндпоинта: {e}")
        
        # Создаем главный файл с оглавлением
        self.create_index_file(spec_dir, spec_name, grouped)
        
        print(f"✓ Документация для '{spec_name}' создана в {spec_dir}\n")
    
    def create_index_file(self, spec_dir: Path, spec_name: str, grouped: dict):
        """Создает главный файл с оглавлением."""
        index_file = spec_dir / "README.md"
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(f"# Документация API: {spec_name}\n\n")
            f.write("## Структура документации\n\n")
            f.write("### По тегам (категориям)\n\n")
            
            for tag in sorted(grouped.keys()):
                tag_filename = self.sanitize_filename(tag)
                f.write(f"- [{tag}](tags/{tag_filename}.md)\n")
            
            f.write("\n### Все эндпоинты\n\n")
            
            for tag in sorted(grouped.keys()):
                f.write(f"\n#### {tag}\n\n")
                for endpoint in grouped[tag]:
                    method = endpoint["method"].lower()
                    path_part = self.sanitize_filename(endpoint["path"])
                    endpoint_filename = f"{method}_{path_part}"
                    f.write(f"- **{endpoint['method']}** {endpoint['path']} ")
                    f.write(f"[→](endpoints/{endpoint_filename}.md)\n")
    
    def process_directory(self, directory: str):
        """Обрабатывает все OpenAPI файлы в директории."""
        directory_path = Path(directory)
        
        json_files = list(directory_path.glob("*.json")) + list(directory_path.glob("*.yaml"))
        
        if not json_files:
            print(f"Не найдены OpenAPI файлы в {directory}")
            return
        
        print(f"Найдено {len(json_files)} файлов для обработки\n")
        
        for file_path in json_files:
            try:
                self.process_openapi_file(str(file_path))
            except Exception as e:
                print(f"✗ Ошибка при обработке {file_path}: {e}\n")


def main():
    """Главная функция для запуска генератора документации."""
    
    # Инициализируем LLM (используем Ollama как пример, можно заменить на другой)
    # Убедитесь, что Ollama запущена и модель доступна
    try:
        llm = Ollama(model="mistral")  # или "llama2", "neural-chat", etc.
    except Exception as e:
        print(f"Ошибка при инициализации Ollama: {e}")
        print("Убедитесь, что Ollama запущена: ollama serve")
        print("И скачана модель: ollama pull mistral")
        return
    
    # Инициализируем генератор
    generator = OpenAPIDocumentationGenerator(llm=llm, output_dir="docs")
    
    # Обрабатываем все OpenAPI файлы в директории examples/
    examples_dir = Path(__file__).parent / "examples"
    
    if examples_dir.exists():
        generator.process_directory(str(examples_dir))
    else:
        print(f"Директория {examples_dir} не найдена")


if __name__ == "__main__":
    main()
