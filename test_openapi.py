"""Тесты для OpenAPI Documentation Generator."""

import json
from pathlib import Path
import pytest

from utils import (
    load_openapi,
    OpenAPIValidator,
    OpenAPIAnalyzer,
    OpenAPIExporter
)


# Фикстура для загрузки примера спецификации
@pytest.fixture
def petstore_spec():
    """Загружает petstore спецификацию для тестов."""
    spec_path = Path(__file__).parent / "examples" / "petstore.json"
    if spec_path.exists():
        return load_openapi(str(spec_path))
    return None


class TestOpenAPIValidator:
    """Тесты для OpenAPIValidator."""
    
    def test_valid_spec(self, petstore_spec):
        """Тест валидной спецификации."""
        if petstore_spec:
            is_valid, errors = OpenAPIValidator.is_valid_openapi(petstore_spec)
            assert is_valid, f"Spec should be valid. Errors: {errors}"
    
    def test_missing_openapi_field(self):
        """Тест отсутствия openapi поля."""
        spec = {"info": {"title": "Test", "version": "1.0"}, "paths": {}}
        is_valid, errors = OpenAPIValidator.is_valid_openapi(spec)
        assert not is_valid
        assert any("openapi" in str(e).lower() or "swagger" in str(e).lower() for e in errors)
    
    def test_missing_info(self):
        """Тест отсутствия info объекта."""
        spec = {"openapi": "3.0.0", "paths": {}}
        is_valid, errors = OpenAPIValidator.is_valid_openapi(spec)
        assert not is_valid
        assert any("info" in str(e).lower() for e in errors)
    
    def test_missing_paths(self):
        """Тест отсутствия paths."""
        spec = {"openapi": "3.0.0", "info": {"title": "Test", "version": "1.0"}}
        is_valid, errors = OpenAPIValidator.is_valid_openapi(spec)
        assert not is_valid
        assert any("paths" in str(e).lower() for e in errors)


class TestOpenAPIAnalyzer:
    """Тесты для OpenAPIAnalyzer."""
    
    def test_get_statistics(self, petstore_spec):
        """Тест получения статистики."""
        if petstore_spec:
            analyzer = OpenAPIAnalyzer(petstore_spec)
            stats = analyzer.get_statistics()
            
            assert "title" in stats
            assert "version" in stats
            assert "total_endpoints" in stats
            assert "methods" in stats
            assert "tags" in stats
    
    def test_find_endpoints_by_tag(self, petstore_spec):
        """Тест поиска эндпоинтов по тегу."""
        if petstore_spec:
            analyzer = OpenAPIAnalyzer(petstore_spec)
            
            # Petstore имеет тег "pets"
            pets_endpoints = analyzer.find_endpoints_by_tag("pets")
            assert len(pets_endpoints) > 0
            
            for ep in pets_endpoints:
                assert "method" in ep
                assert "path" in ep
                assert ep["method"] in ["GET", "POST", "PUT", "DELETE", "PATCH"]
    
    def test_find_endpoints_by_method(self, petstore_spec):
        """Тест поиска эндпоинтов по методу."""
        if petstore_spec:
            analyzer = OpenAPIAnalyzer(petstore_spec)
            
            get_endpoints = analyzer.find_endpoints_by_method("GET")
            assert len(get_endpoints) > 0
            
            for ep in get_endpoints:
                assert ep["method"] == "GET"
    
    def test_list_all_endpoints(self, petstore_spec):
        """Тест получения списка всех эндпоинтов."""
        if petstore_spec:
            analyzer = OpenAPIAnalyzer(petstore_spec)
            endpoints = analyzer.list_all_endpoints()
            
            assert len(endpoints) > 0
            
            for ep in endpoints:
                assert "method" in ep
                assert "path" in ep
                assert "summary" in ep
                assert "tags" in ep
    
    def test_get_all_schemas(self, petstore_spec):
        """Тест получения всех схем."""
        if petstore_spec:
            analyzer = OpenAPIAnalyzer(petstore_spec)
            schemas = analyzer.get_all_schemas()
            
            # Petstore должна иметь схемы
            assert isinstance(schemas, dict)
    
    def test_get_security_schemes(self, petstore_spec):
        """Тест получения схем безопасности."""
        if petstore_spec:
            analyzer = OpenAPIAnalyzer(petstore_spec)
            schemes = analyzer.get_security_schemes()
            
            assert isinstance(schemes, dict)


class TestOpenAPIExporter:
    """Тесты для OpenAPIExporter."""
    
    def test_export_endpoints_csv(self, petstore_spec, tmp_path):
        """Тест экспорта в CSV."""
        if petstore_spec:
            exporter = OpenAPIExporter(petstore_spec)
            csv_file = tmp_path / "endpoints.csv"
            
            exporter.export_endpoints_csv(str(csv_file))
            
            assert csv_file.exists()
            assert csv_file.stat().st_size > 0
            
            # Проверяем содержание
            with open(csv_file) as f:
                content = f.read()
                assert "Method" in content
                assert "Path" in content
    
    def test_export_statistics_json(self, petstore_spec, tmp_path):
        """Тест экспорта статистики в JSON."""
        if petstore_spec:
            exporter = OpenAPIExporter(petstore_spec)
            json_file = tmp_path / "stats.json"
            
            exporter.export_statistics_json(str(json_file))
            
            assert json_file.exists()
            
            with open(json_file) as f:
                stats = json.load(f)
                assert "title" in stats
                assert "version" in stats
                assert "total_endpoints" in stats
    
    def test_generate_postman_collection(self, petstore_spec, tmp_path):
        """Тест генерирования Postman коллекции."""
        if petstore_spec:
            exporter = OpenAPIExporter(petstore_spec)
            postman_file = tmp_path / "postman.json"
            
            exporter.generate_postman_collection(str(postman_file))
            
            assert postman_file.exists()
            
            with open(postman_file) as f:
                collection = json.load(f)
                assert "info" in collection
                assert "item" in collection


class TestIntegration:
    """Интеграционные тесты."""
    
    def test_load_and_analyze_petstore(self, petstore_spec):
        """Тест полного цикла: загрузка и анализ."""
        if petstore_spec:
            # Валидация
            is_valid, _ = OpenAPIValidator.is_valid_openapi(petstore_spec)
            assert is_valid
            
            # Анализ
            analyzer = OpenAPIAnalyzer(petstore_spec)
            stats = analyzer.get_statistics()
            
            assert stats["total_endpoints"] > 0
            assert len(stats["tags"]) > 0
            assert "pets" in stats["tags"]
    
    def test_endpoints_consistency(self, petstore_spec):
        """Тест консистентности эндпоинтов."""
        if petstore_spec:
            analyzer = OpenAPIAnalyzer(petstore_spec)
            
            all_endpoints = analyzer.list_all_endpoints()
            pets_endpoints = analyzer.find_endpoints_by_tag("pets")
            
            # Все pets эндпоинты должны быть в общем списке
            assert len(pets_endpoints) <= len(all_endpoints)
    
    def test_get_request_body_schema(self, petstore_spec):
        """Тест получения схемы request body."""
        if petstore_spec:
            analyzer = OpenAPIAnalyzer(petstore_spec)
            
            # Petstore имеет POST /pets с request body
            schema = analyzer.get_request_body_schema("/pets", "post")
            
            # Может быть None или dict
            if schema is not None:
                assert isinstance(schema, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
