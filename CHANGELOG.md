# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-01-20

### Added
- ✨ Initial release of OpenAPI to Markdown Documentation Generator
- 🤖 LangChain integration for AI-powered documentation generation
- 📚 Support for multiple LLM providers:
  - Ollama (local, free)
  - OpenAI (GPT-3.5, GPT-4)
  - Anthropic (Claude)
  - HuggingFace
- 🏗️ Two implementation approaches:
  - Basic: Using LangChain Chains (main.py)
  - Advanced: Using LangChain Expression Language (advanced_generator.py)
- 🖥️ Interactive CLI interface (cli.py)
- 📊 OpenAPI specification analysis tools:
  - Validation
  - Statistics generation
  - Tag-based searching
  - Method-based filtering
- 💾 Multiple export formats:
  - CSV (endpoints list)
  - JSON (statistics)
  - Postman collection
- 🌐 Multi-language support:
  - Russian (default)
  - English
- 📖 Comprehensive documentation:
  - README.md (overview and features)
  - USAGE.md (detailed guide)
  - QUICKSTART.md (quick reference)
  - STRUCTURE.md (project architecture)
- 🧪 Unit tests for core functionality
- 📦 PyPI package configuration
- 🎯 Example OpenAPI specifications included

### Features
- Automatic endpoint extraction from OpenAPI specs
- Grouping documentation by tags
- Individual markdown files per endpoint
- Table of contents generation
- Security scheme documentation
- Parameter documentation with types
- Request/Response schema documentation
- Schema reference resolution
- Support for both OpenAPI 3.0 and Swagger 2.0 (limited)

### Documentation
- Installation guide
- Usage examples
- API documentation
- Configuration guide
- Troubleshooting section
- Best practices

### Tools Included
- `OpenAPIDocumentationGenerator` - basic generator
- `AdvancedOpenAPIDocGenerator` - advanced generator with LCEL
- `OpenAPIValidator` - specification validation
- `OpenAPIAnalyzer` - specification analysis
- `OpenAPIExporter` - data export functionality
- `OpenAPIDocCLI` - interactive command-line interface

### Configuration
- Support for environment variables (.env)
- Flexible LLM provider configuration
- Customizable output directories
- Language selection
- Temperature and max_tokens settings

### Examples
- 5 ready-to-use example OpenAPI files
- 5 different usage examples
- CLI menu with guided options
- Interactive configuration

## Future Roadmap

### v0.2.0 (Planned)
- HTML output generation
- Diagram generation (PlantUML, Mermaid)
- Real-time streaming for long generations
- Batch processing optimization
- Rate limiting for API calls
- Caching layer for repeated processing
- Web UI dashboard

### v0.3.0 (Planned)
- GraphQL support
- gRPC documentation
- API diff generation
- Version comparison
- Interactive API explorer generation
- OpenAI plugins support

### v0.4.0 (Planned)
- Database schema documentation
- API contract testing
- Performance profiling tools
- Integration with CI/CD pipelines
- GitHub Actions support
- Slack notifications

### v1.0.0 (Planned)
- Stable API
- Full test coverage
- Performance optimizations
- Extended language support
- Enterprise features
- Commercial support option

## Known Issues

None reported yet.

## Migration Guide

### From v0.0.x to v0.1.0

This is the first stable release. No migration needed.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

BSD 3-Clause License - See LICENSE file for details

## Credits

- Built with [LangChain](https://python.langchain.com/)
- Inspired by OpenAPI best practices
- Community feedback and contributions

---

**Last Updated:** 2026-01-20
