# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-03-19

### Added
- Initial release
- 14 built-in tools:
  - File operations: `read_file`, `write_file`, `list_directory`, `search_files`, `grep`
  - Web tools: `web_search`, `web_fetch`
  - Git tools: `git_clone`, `git_pull`
  - System tools: `run_command`, `python_eval`, `get_system_info`, `get_time`, `calculate`
- Dynamic tool discovery from `./workspace/tools/`
- HTTP transport with streamable-http
- JSON response mode for broad compatibility
- Persistent workspace volume
- Docker and Docker Compose setup

### Custom Tools Included
- `greeting` - Generate personalized greetings (formal, casual, funny)
- `add_numbers` - Add two numbers
- `word_reverser` - Reverse words in a sentence

## [Unreleased]

### Known Issues
- Custom tools may require LLM to refresh tool list on first load

### Planned
- Security-hardened `run_command` with blacklist/whitelist
- Additional web research tools
- MCP registry integration for easy tool discovery
