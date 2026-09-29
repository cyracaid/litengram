# Changelog — LitEngram

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.6.0] - 2026-09-29

### Added
- ✨ **PDF 高亮合法注入**（`scripts/zotero_highlight_builder.py`）：用 PyMuPDF 字符级 core 匹配 + y 翻转
  （`zotero_y = pageH − pymupdf_y`）生成合法 `position`，批量 INSERT 高亮 + 4 层批注。
  推翻 v1.2「SQLite 不可能构造合法 position」断言。EMBA 验证：NeuroImage + Biological Psychology 两篇 41 条成功渲染。

### Fixed
- 🔧 **note 必须包 `<div class="zotero-note znv1">`**：否则 Zotero 启动时把整篇当纯文本二次转义成 `&lt;h1&gt;` 乱码
- 🔧 **annotation schema 纠正**：`itemAnnotations` 无 `annotatesItemID` 列；`parentItemID` 必须是 attachment 的 itemID；
  合法列 = type / authorName / text / comment / color / pageLabel / sortIndex(三段) / position / isExternal
- 🔧 **authorName 必须设置**（借鉴 1.3.0 的 zotero_annotation_sync 经验），否则 Zotero UI 不渲染

## [1.3.0] - 2026-09-09

### Added
- ✨ **Comprehensive documentation suite**
  - API_REFERENCE.md (detailed function documentation)
  - BEST_PRACTICES.md (7 usage strategies)
  - FAQ.md (23 common questions answered)
  - SECURITY.md (privacy model + threat analysis)
  - INTEGRATIONS.md (Obsidian, Logseq, Roam, Notion)
  - PERFORMANCE.md (benchmarks + optimization tips)
  - ROADMAP.md (v1.4 through 2027+ vision)

- 📚 **Example files**
  - docs/examples/example_workflow.md (4-week end-to-end guide)
  - docs/examples/example_python_api.py (4 code examples)

- 🏗️ **Architecture documentation**
  - docs/ARCHITECTURE.md (13KB system design)
  - Complete data flow diagrams
  - Concurrency model explanation
  - Error handling patterns
  - Extensibility points

- 📖 **README enhancement** (749 lines)
  - GitHub badges & status indicators
  - System architecture ASCII diagram
  - Quick Start section (5 minutes)
  - Advanced configuration guide
  - Performance benchmarks
  - Project structure with annotations
  - Complete working demo

- 🧪 **Annotation bug fixes**
  - Fixed: authorName = NULL preventing Zotero UI rendering
  - New: zotero_annotation_sync.py (annotation sync script)
  - Added: batch_update_annotations() with atomic transactions
  - Added: verify_annotations() for quality checks

### Fixed
- 🔧 **Critical bug**: All 52 annotations now have authorName = 'Lintengram'
  - Root cause: Zotero UI skips rendering if authorName IS NULL
  - Solution: Batch update script with proper transaction handling
  - Verified: Working in Zotero UI (comments now visible)

### Changed
- 📊 **Performance improvements**
  - Batch processing: 45s for 52 annotations (vs serial: 90s+)
  - Database transactions: BEGIN IMMEDIATE prevents race conditions
  - Ollama integration: Fallback to LLM when rule parser fails

### Documentation
- ✅ Moved from 532-line README to 749-line README + 8 detailed docs
- ✅ Added 35+ code examples across documentation
- ✅ Added real performance benchmarks (MacBook M1 Max)
- ✅ Added security checklist (8 categories)
- ✅ Added FAQ (23 Q&As with solutions)

---

## [1.2.0] - 2026-09-08

### Added
- 🔗 Knowledge fingerprinting system
  - MD5-based concept linking
  - Cross-paper concept detection
  - Soft-关联 mechanism for similar concepts

- 🎯 Hybrid annotation processing
  - Rule-first parser with regex extraction
  - LLM fallback (Ollama) when parsing fails
  - Confidence scoring (high/medium/low)

- 📱 Notion integration
  - Automatic sync of structured notes
  - Database entry creation/update
  - Metadata preservation

### Fixed
- 🐛 Database locking issues
  - Implemented BEGIN IMMEDIATE transactions
  - 30-second timeout for locked DB
  - Race condition prevention with itemID collision retries

---

## [1.1.0] - 2026-09-01

### Added
- 🧠 4-layer annotation structure
  - 【定义】(Definition with theory origin)
  - 【本文角色】(Role in this paper)
  - 【论证关联】(Connection to paper's argument)
  - 【延伸】(Your extension/thoughts)

- 📖 Literature analysis framework
  - Domain detection (neuroscience, psychology, etc)
  - Concept excavation (9-layer model)
  - Staged analysis (stages 1-6)

- 🗄️ Zotero SQLite integration
  - Direct database access (no API needed)
  - Comment field updates
  - Batch annotation processing

---

## [1.0.0] - 2026-08-15

### Added
- 🚀 Initial release
  - Basic Zotero database connection
  - Simple annotation parsing
  - JSON comment generation
  - Initial Notion sync skeleton

---

## Unreleased

### Planned for 1.4.0 (Q4 2026)
- [ ] Web UI dashboard for knowledge graph visualization
- [ ] Obsidian/Logseq/Roam direct export
- [ ] Batch paper import from BibTeX
- [ ] Custom LLM prompt templates
- [ ] FastAPI server for programmatic access
- [ ] Progress bars and better logging

### Planned for 2.0.0 (2027 H1)
- [ ] Multi-LLM support (Claude, GPT-4, Llama)
- [ ] Real-time collaborative annotations
- [ ] Automatic paper recommendations
- [ ] Citation network visualization
- [ ] Mobile companion app

### Planned for 2027+
- [ ] Cross-language support (>10 languages)
- [ ] Advanced reasoning (chain-of-thought, self-critique)
- [ ] Publication-ready formatted citations
- [ ] Full-text search across papers
- [ ] Team/lab collaboration features

---

## Version History Summary

| Version | Date | Highlights |
|---------|------|-----------|
| 1.3.0 | 2026-09-09 | Complete documentation + examples + benchmarks |
| 1.2.0 | 2026-09-08 | Fingerprinting + Hybrid processing |
| 1.1.0 | 2026-09-01 | 4-layer structure + Framework |
| 1.0.0 | 2026-08-15 | Initial release |

---

## Contribution

Contributions welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## Versioning Policy

- **Major version** (X.0.0): Breaking changes, new architecture
- **Minor version** (1.X.0): New features, backwards compatible
- **Patch version** (1.0.X): Bug fixes, no new features

See [Semantic Versioning](https://semver.org/) for details.
