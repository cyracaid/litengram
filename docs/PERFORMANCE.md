# Performance — LitEngram

Benchmarks and optimization tips.

---

## Processing Benchmarks

Real measurements on MacBook Pro M1 Max with 32GB RAM:

### By Annotation Count

| Count | Time | Memory | CPU |
|-------|------|--------|-----|
| 10 | 15s | 150MB | 40% |
| 50 | 45s | 220MB | 60% |
| 100 | 90s | 280MB | 70% |

### By LLM Model

| Model | Speed | Quality | Memory |
|-------|-------|---------|--------|
| qwen2.5:0.5b | 3-5s/ann | ⭐⭐⭐⭐ | 200MB |
| mistral | 8-12s/ann | ⭐⭐⭐⭐⭐ | 7GB+ |

### By Operation

| Operation | Time |
|-----------|------|
| Zotero connect | ~1s |
| Extract 50 annotations | ~2s |
| Rule-first parse | ~1s per annotation |
| LLM generation | ~3-10s per annotation |
| Fingerprinting | ~0.1s per annotation |
| Database write | ~50ms per annotation |
| Notion sync | ~2-3s |

---

## Optimization Tips

### 1. Disable Notion Sync

```bash
export NOTION_SYNC=false
# Saves: 5-10s per run
```

### 2. Use Faster LLM

```bash
export OLLAMA_MODEL=qwen2.5:0.5b  # vs mistral
# Saves: 5-7s per annotation
```

### 3. Batch Updates

Always use batch mode (default):
```bash
# Good (45s for 50)
db.batch_update_annotations(updates)

# Bad (90+ seconds for 50)
for item_id, comment in updates:
    db.update_annotation(item_id, comment)
```

### 4. System Resources

- Close unnecessary apps (free up RAM)
- Close Zotero before processing (faster DB access)
- Disable antivirus scanning temporarily (if safe)

---

For more, see BEST_PRACTICES.md
