"""Утилиты для работы с OpenAPI спецификациями."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse


class OpenAPIValidator:
    """Валидирует OpenAPI спецификации."""
    
    @staticmethod
    def is_valid_openapi(spec: dict) -> Tuple[bool, List[str]]:
        """Проверяет валидность OpenAPI спецификации."""
        errors = []
        
        # Проверяем обязательные поля
        if "openapi" not in spec and "swagger" not in spec:
            errors.append("Missing 'openapi' or 'swagger' field")
        
        if "info" not in spec:
            errors.append("Missing 'info' object")
        elif not isinstance(spec["info"], dict):
            errors.append("'info' must be an object")
        else:
            info = spec["info"]
            if "title" not in info:
                errors.append("Missing 'info.title'")
            if "version" not in info:
                errors.append("Missing 'info.version'")
        
        if "paths" not in spec:
            errors.append("Missing 'paths' object")
        
        return len(errors) == 0, errors


class OpenAPIAnalyzer:
    """Анализирует OpenAPI спецификации."""
    
    def __init__(self, spec: dict):
        self.spec = spec
    
    def get_statistics(self) -> dict:
        """Возвращает статистику по спецификации."""
        paths = self.spec.get("paths", {})
        
        endpoints_count = 0
        methods_count = {}
        tags_count = {}
        
        for path, path_item in paths.items():
            for method in ["get", "post", "put", "delete", "patch", "head", "options"]:
                if method in path_item:
                    endpoints_count += 1
                    methods_count[method] = methods_count.get(method, 0) + 1
                    
                    operation = path_item[method]
                    for tag in operation.get("tags", ["untagged"]):
                        tags_count[tag] = tags_count.get(tag, 0) + 1
        
        components = self.spec.get("components", {})
        
        return {
            "title": self.spec.get("info", {}).get("title", "Unknown"),
            "version": self.spec.get("info", {}).get("version", "Unknown"),
            "total_endpoints": endpoints_count,
            "methods": methods_count,
            "tags": tags_count,
            "schemas": len(components.get("schemas", {})),
            "security_schemes": len(components.get("securitySchemes", {})),
        }
    
    def find_endpoints_by_tag(self, tag: str) -> List[Dict]:
        """Находит все эндпоинты с указанным тегом."""
        endpoints = []
        
        for path, path_item in self.spec.get("paths", {}).items():
            for method in ["get", "post", "put", "delete", "patch", "head", "options"]:
                if method in path_item:
                    operation = path_item[method]
                    if tag in operation.get("tags", []):
                        endpoints.append({
                            "method": method.upper(),
                            "path": path,
                            "summary": operation.get("summary", ""),
                            "description": operation.get("description", ""),
                        })
        
        return endpoints
    
    def find_endpoints_by_method(self, method: str) -> List[Dict]:
        """Находит все эндпоинты с указанным HTTP методом."""
        endpoints = []
        method = method.lower()
        
        for path, path_item in self.spec.get("paths", {}).items():
            if method in path_item:
                operation = path_item[method]
                endpoints.append({
                    "path": path,
                    "method": method.upper(),
                    "summary": operation.get("summary", ""),
                    "tags": operation.get("tags", []),
                })
        
        return endpoints
    
    def get_request_body_schema(self, path: str, method: str) -> Optional[dict]:
        """Получает схему Request Body для эндпоинта."""
        method = method.lower()
        
        try:
            operation = self.spec["paths"][path][method]
            request_body = operation.get("requestBody", {})
            
            content = request_body.get("content", {})
            for content_type, content_data in content.items():
                if "schema" in content_data:
                    return content_data["schema"]
            
            return None
        except (KeyError, TypeError):
            return None
    
    def get_response_schemas(self, path: str, method: str) -> Dict[str, dict]:
        """Получает схемы ответов для эндпоинта."""
        method = method.lower()
        schemas = {}
        
        try:
            operation = self.spec["paths"][path][method]
            responses = operation.get("responses", {})
            
            for status, response in responses.items():
                content = response.get("content", {})
                for content_type, content_data in content.items():
                    if "schema" in content_data:
                        schemas[status] = content_data["schema"]
            
            return schemas
        except (KeyError, TypeError):
            return {}
    
    def resolve_schema_reference(self, ref: str) -> Optional[dict]:
        """Разрешает $ref ссылку на полную схему."""
        if not ref.startswith("#/"):
            return None
        
        parts = ref[2:].split("/")
        obj = self.spec
        
        try:
            for part in parts:
                obj = obj[part]
            return obj
        except (KeyError, TypeError):
            return None
    
    def get_all_schemas(self) -> Dict[str, dict]:
        """Возвращает все определенные схемы."""
        return self.spec.get("components", {}).get("schemas", {})
    
    def get_security_schemes(self) -> Dict[str, dict]:
        """Возвращает все схемы безопасности."""
        return self.spec.get("components", {}).get("securitySchemes", {})
    
    def get_global_security(self) -> List[dict]:
        """Возвращает глобальные требования безопасности."""
        return self.spec.get("security", [])
    
    def list_all_endpoints(self) -> List[Dict]:
        """Возвращает список всех эндпоинтов."""
        endpoints = []
        
        for path, path_item in self.spec.get("paths", {}).items():
            for method in ["get", "post", "put", "delete", "patch", "head", "options"]:
                if method in path_item:
                    operation = path_item[method]
                    endpoints.append({
                        "method": method.upper(),
                        "path": path,
                        "summary": operation.get("summary", ""),
                        "tags": operation.get("tags", []),
                        "deprecated": operation.get("deprecated", False),
                    })
        
        return sorted(endpoints, key=lambda x: (x["path"], x["method"]))


class OpenAPIExporter:
    """Экспортирует информацию из OpenAPI в разные форматы."""
    
    def __init__(self, spec: dict):
        self.spec = spec
        self.analyzer = OpenAPIAnalyzer(spec)
    
    def export_endpoints_csv(self, output_path: str):
        """Экспортирует список эндпоинтов в CSV."""
        import csv
        
        endpoints = self.analyzer.list_all_endpoints()
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['Method', 'Path', 'Summary', 'Tags', 'Deprecated']
            )
            writer.writeheader()
            
            for ep in endpoints:
                writer.writerow({
                    'Method': ep['method'],
                    'Path': ep['path'],
                    'Summary': ep['summary'],
                    'Tags': ', '.join(ep['tags']),
                    'Deprecated': ep['deprecated'],
                })
    
    def export_statistics_json(self, output_path: str):
        """Экспортирует статистику в JSON."""
        stats = self.analyzer.get_statistics()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    
    def generate_postman_collection(self, output_path: str):
        """Генерирует Postman коллекцию."""
        info = self.spec.get("info", {})
        servers = self.spec.get("servers", [])
        base_url = servers[0]["url"] if servers else ""
        
        collection = {
            "info": {
                "name": info.get("title", "API"),
                "description": info.get("description", ""),
                "version": info.get("version", "1.0.0"),
            },
            "item": [],
            "variable": []
        }
        
        if base_url:
            collection["variable"].append({
                "key": "base_url",
                "value": base_url,
            })
        
        # Добавляем запросы
        for path, path_item in self.spec.get("paths", {}).items():
            for method in ["get", "post", "put", "delete", "patch"]:
                if method in path_item:
                    operation = path_item[method]
                    
                    request = {
                        "name": operation.get("summary", f"{method.upper()} {path}"),
                        "request": {
                            "method": method.upper(),
                            "url": {
                                "raw": f"{{{{base_url}}}}{path}",
                                "host": ["{{base_url}}"],
                                "path": path.split("/")[1:]
                            }
                        }
                    }
                    
                    if operation.get("parameters"):
                        request["request"]["url"]["query"] = [
                            {
                                "key": p["name"],
                                "value": "",
                                "disabled": not p.get("required", False)
                            }
                            for p in operation["parameters"]
                            if p.get("in") == "query"
                        ]
                    
                    collection["item"].append(request)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(collection, f, ensure_ascii=False, indent=2)


def load_openapi(file_path: str) -> dict:
    """Загружает OpenAPI файл (JSON или YAML)."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            import yaml
            return yaml.safe_load(f)
        else:
            return json.load(f)


def save_openapi(spec: dict, file_path: str):
    """Сохраняет OpenAPI спецификацию в файл."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
