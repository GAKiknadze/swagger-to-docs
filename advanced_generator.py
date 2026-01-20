"""Альтернативная реализация с использованием LangChain Expression Language."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, List
from collections import defaultdict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.base import BaseLanguageModel


class AdvancedOpenAPIDocGenerator:
    """Продвинутый генератор документации с использованием LCEL."""
    
    def __init__(self, llm: BaseLanguageModel, output_dir: str = "docs", language: str = "ru"):
        """
        Args:
            llm: Language model для генерации
            output_dir: Директория для сохранения
            language: Язык документации (ru/en)
        """
        self.llm = llm
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.language = language
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Настраивает промпты для LCEL цепочек."""
        
        if self.language == "ru":
            endpoint_template = """Создай детальную документацию на русском языке для REST API эндпоинта:

Путь: {path}
Метод: {method}
Тег: {tags}

Информация об операции:
{operation_details}

Авторизация: {security}

Документация ДОЛЖНА включать:
1. Краткое описание эндпоинта
2. Параметры запроса с типами и описаниями
3. Тело запроса (если требуется) с примером
4. Все возможные ответы с кодами статуса и схемами
5. 2-3 примера curl запроса с реальными данными
6. Коды ошибок и их смысл

Формат: Markdown с правильной иерархией заголовков"""

            tag_template = """Создай подробную документацию для группы API эндпоинтов на русском:

Название: {tag}
Описание: {description}

Список эндпоинтов в этой группе:
{endpoints_list}

Документация должна включать:
1. Общее описание функциональности группы
2. Требования к авторизации (если есть)
3. Таблица со всеми эндпоинтами (метод, путь, описание)
4. Общие параметры и заголовки
5. Типичные сценарии использования
6. Ошибки и их обработка

Формат: Markdown"""

            overview_template = """Создай полный обзор API документации на русском:

Название API: {api_title}
Версия: {api_version}
Описание: {api_description}

Статистика:
- Всего эндпоинтов: {total_endpoints}
- Групп (тегов): {total_tags}
- Основные компоненты: {components}

Документация должна включать:
1. Краткое описание API
2. Информацию об авторизации
3. Базовый URL и версия
4. Список всех доступных групп эндпоинтов со ссылками
5. Общие заголовки запроса
6. Коды ошибок
7. Рекомендации по использованию

Формат: Markdown"""
        else:
            endpoint_template = """Create detailed documentation for a REST API endpoint:

Path: {path}
Method: {method}
Tag: {tags}

Operation Details:
{operation_details}

Security: {security}

Documentation MUST include:
1. Brief endpoint description
2. Request parameters with types
3. Request body (if required) with example
4. All possible responses with status codes
5. 2-3 curl examples
6. Error codes and meanings

Format: Markdown"""

            tag_template = """Create comprehensive documentation for a group of API endpoints:

Name: {tag}
Description: {description}

Endpoints in this group:
{endpoints_list}

Documentation must include:
1. Group functionality overview
2. Authorization requirements
3. Endpoints table
4. Common parameters
5. Usage scenarios
6. Error handling

Format: Markdown"""

            overview_template = """Create a complete API documentation overview:

API Name: {api_title}
Version: {api_version}
Description: {api_description}

Statistics:
- Total endpoints: {total_endpoints}
- Groups (tags): {total_tags}
- Key components: {components}

Format: Markdown"""
        
        self.endpoint_prompt = ChatPromptTemplate.from_template(endpoint_template)
        self.tag_prompt = ChatPromptTemplate.from_template(tag_template)
        self.overview_prompt = ChatPromptTemplate.from_template(overview_template)
        
        # Создаем LCEL цепочки
        self.endpoint_chain = (
            self.endpoint_prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        self.tag_chain = (
            self.tag_prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        self.overview_chain = (
            self.overview_prompt 
            | self.llm 
            | StrOutputParser()
        )
    
    def load_spec(self, file_path: str) -> dict:
        """Загружает OpenAPI спецификацию."""
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                import yaml
                return yaml.safe_load(f)
            return json.load(f)
    
    def extract_endpoints(self, spec: dict) -> Dict[str, dict]:
        """Извлекает информацию об эндпоинтах."""
        endpoints = {}
        
        for path, path_item in spec.get("paths", {}).items():
            for method in ["get", "post", "put", "delete", "patch", "head", "options"]:
                if method in path_item:
                    operation = path_item[method]
                    key = f"{method.upper()} {path}"
                    endpoints[key] = {
                        "path": path,
                        "method": method.upper(),
                        "operation": operation,
                        "tags": operation.get("tags", ["Other"])
                    }
        
        return endpoints
    
    def format_operation(self, op: dict) -> str:
        """Форматирует операцию в читаемый вид."""
        parts = []
        
        if "summary" in op:
            parts.append(f"**Summary:** {op['summary']}")
        if "description" in op:
            parts.append(f"**Description:** {op['description']}")
        
        # Параметры
        if "parameters" in op:
            parts.append("\n**Parameters:**")
            for p in op["parameters"]:
                req = "required" if p.get("required") else "optional"
                parts.append(
                    f"- `{p['name']}` ({p.get('in')}, {req}): {p.get('description', '')}"
                )
        
        # Request body
        if "requestBody" in op:
            parts.append("\n**Request Body:**")
            rb = op["requestBody"]
            parts.append(f"- Required: {rb.get('required', False)}")
            parts.append(f"- Content Type: {', '.join(rb.get('content', {}).keys())}")
        
        # Responses
        if "responses" in op:
            parts.append("\n**Responses:**")
            for status, resp in op["responses"].items():
                parts.append(f"- `{status}`: {resp.get('description', '')}")
        
        return "\n".join(parts)
    
    def get_components_summary(self, spec: dict) -> str:
        """Получает сводку по компонентам."""
        components = spec.get("components", {})
        if not components:
            return "No components"
        
        summary = []
        if "schemas" in components:
            summary.append(f"Schemas: {len(components['schemas'])}")
        if "securitySchemes" in components:
            summary.append(f"Security schemes: {len(components['securitySchemes'])}")
        
        return ", ".join(summary) if summary else "No components"
    
    def get_security_info(self, operation: dict, spec: dict) -> str:
        """Получает информацию о безопасности эндпоинта."""
        security = operation.get("security", spec.get("security", []))
        if not security:
            return "No authentication required"
        
        schemes = []
        for sec in security:
            schemes.extend(sec.keys())
        return ", ".join(schemes) if schemes else "No authentication"
    
    def sanitize_filename(self, text: str) -> str:
        """Создает безопасное имя файла."""
        import re
        text = text.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
        text = re.sub(r'[^a-z0-9_]', '', text)
        return text[:100]  # Ограничиваем длину
    
    def create_directory_structure(self, spec: dict) -> Path:
        """Создает структуру директорий."""
        spec_name = spec.get("info", {}).get("title", "api")
        spec_dir = self.output_dir / self.sanitize_filename(spec_name)
        
        (spec_dir / "tags").mkdir(parents=True, exist_ok=True)
        (spec_dir / "endpoints").mkdir(parents=True, exist_ok=True)
        
        return spec_dir
    
    def process_openapi_file(self, file_path: str):
        """Обрабатывает один OpenAPI файл."""
        print(f"\n📄 Processing: {file_path}")
        
        spec = self.load_spec(file_path)
        info = spec.get("info", {})
        spec_name = info.get("title", "API")
        
        # Создаем структуру
        spec_dir = self.create_directory_structure(spec)
        
        # Извлекаем эндпоинты
        endpoints = self.extract_endpoints(spec)
        grouped = defaultdict(list)
        
        for key, ep in endpoints.items():
            for tag in ep["tags"]:
                grouped[tag].append({**ep, "key": key})
        
        print(f"📊 Found {len(endpoints)} endpoints in {len(grouped)} tags\n")
        
        # Обрабатываем каждый тег
        for tag in sorted(grouped.keys()):
            tag_endpoints = grouped[tag]
            print(f"  🏷️  Processing tag: {tag}")
            
            # Генерируем обзор тега
            try:
                endpoints_str = "\n".join([
                    f"- **{ep['method']}** {ep['path']}: {ep['operation'].get('summary', '')}"
                    for ep in tag_endpoints
                ])
                
                # Получаем описание тега
                tags_info = spec.get("tags", [])
                tag_desc = next(
                    (t.get("description", "") for t in tags_info if t.get("name") == tag),
                    ""
                )
                
                tag_doc = self.tag_chain.invoke({
                    "tag": tag,
                    "description": tag_desc,
                    "endpoints_list": endpoints_str
                })
                
                tag_file = spec_dir / "tags" / f"{self.sanitize_filename(tag)}.md"
                with open(tag_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {tag}\n\n")
                    f.write(tag_doc)
                
                print(f"    ✅ Created: {tag_file.name}")
            
            except Exception as e:
                print(f"    ❌ Error: {e}")
            
            # Генерируем для каждого эндпоинта
            for ep in tag_endpoints:
                try:
                    op_details = self.format_operation(ep["operation"])
                    security = self.get_security_info(ep["operation"], spec)
                    
                    doc = self.endpoint_chain.invoke({
                        "path": ep["path"],
                        "method": ep["method"],
                        "tags": tag,
                        "operation_details": op_details,
                        "security": security
                    })
                    
                    # Сохраняем файл
                    filename = f"{ep['method'].lower()}_{self.sanitize_filename(ep['path'])}"
                    ep_file = spec_dir / "endpoints" / f"{filename}.md"
                    
                    with open(ep_file, 'w', encoding='utf-8') as f:
                        f.write(f"# {ep['method']} {ep['path']}\n\n")
                        f.write(f"**Tag:** {tag}\n\n")
                        f.write(doc)
                    
                    print(f"    ✅ Endpoint: {filename}.md")
                
                except Exception as e:
                    print(f"    ❌ Endpoint error: {e}")
        
        # Создаем README с оглавлением
        self._create_index(spec_dir, spec, grouped)
        
        print(f"\n✨ Documentation created in: {spec_dir}")
    
    def _create_index(self, spec_dir: Path, spec: dict, grouped: dict):
        """Создает файл с оглавлением."""
        info = spec.get("info", {})
        readme = spec_dir / "README.md"
        
        with open(readme, 'w', encoding='utf-8') as f:
            f.write(f"# {info.get('title', 'API')}\n\n")
            f.write(f"**Version:** {info.get('version', 'N/A')}\n\n")
            
            if info.get('description'):
                f.write(f"{info['description']}\n\n")
            
            f.write("## 📑 Table of Contents\n\n")
            
            for tag in sorted(grouped.keys()):
                tag_file = self.sanitize_filename(tag)
                f.write(f"- [{tag}](tags/{tag_file}.md)\n")
            
            f.write("\n## 🔌 All Endpoints\n\n")
            
            for tag in sorted(grouped.keys()):
                f.write(f"\n### {tag}\n\n")
                
                for ep in grouped[tag]:
                    method = ep["method"].lower()
                    path = self.sanitize_filename(ep["path"])
                    filename = f"{method}_{path}"
                    summary = ep["operation"].get("summary", "")
                    
                    f.write(f"- [`{ep['method']}`](endpoints/{filename}.md) ")
                    f.write(f"{ep['path']} - {summary}\n")
    
    def process_directory(self, directory: str):
        """Обрабатывает все файлы в директории."""
        dir_path = Path(directory)
        files = list(dir_path.glob("*.json")) + list(dir_path.glob("*.yaml")) + list(dir_path.glob("*.yml"))
        
        print(f"🚀 Found {len(files)} OpenAPI files\n")
        
        for file_path in files:
            try:
                self.process_openapi_file(str(file_path))
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}\n")
