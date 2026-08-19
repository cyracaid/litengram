# DOI → Zotero Import Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Given a DOI + collection name, import the paper into the user's Zotero cloud library, place it in the specified folder (collection), attach a PDF when obtainable, and emit the itemKey/attachmentKey so the existing LitEngram annotation pipeline (Stage 4-5) can annotate on top of it.

**Architecture:** A new CLI `scripts/zotero_import.py` orchestrates four independent steps, each a pure function in the same module for testability: (1) dedup the DOI against the local Zotero API; (2) resolve bibliographic metadata from CrossRef; (3) fetch an open-access PDF from OpenAlex (falls back to any Crossref `link` if OA fails); (4) create the parent item + uploaded-file attachment in the user's Zotero cloud via Web API v3 (`POST /users/{userID}/items`, `multipart/form-data`), with the target collection key baked into the parent item's `collections` field. All steps log a structured result; the CLI prints JSON on success and exits nonzero with a clear message on failure.

**Tech Stack:** Python 3.13 (stdlib `unittest` for tests), `requests`, Zotero Web API v3 (`api.zotero.org`), Zotero Local API (`127.0.0.1:23119`), CrossRef REST API (`api.crossref.org`), OpenAlex API (`api.openalex.org`).

**Environment facts (verified 2026-08-09):**
- Zotero desktop running; Local API healthy at `http://127.0.0.1:23119/api/users/0/`
- `requests` installed; Python 3.13.5
- User ID `11261922`; key from `ZOTERO_API_KEY` env var (must have **write access** — verify in Task 3)
- Known collections: `James Gross` = `DAEGLJEI`, `CAD` = `PNHRTHJS`, `Maia ten Brink` = `E2RTY5NJ`
- No existing test harness in the skill repo; tests use stdlib `unittest` + `unittest.mock` to avoid new deps

---

### Task 1: Collection name → key resolution + DOI dedup

**Files:**
- Create: `scripts/zotero_import.py` (module scaffolding + `_LOCAL_API`, `get_collection_key`, `find_item_by_doi`)
- Test: `tests/test_zotero_import.py`

- [ ] **Step 1: Write the failing tests**

```python
import sys, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import zotero_import as zi


class TestCollectionKey(unittest.TestCase):
    @mock.patch("zotero_import.requests.get")
    def test_returns_key_for_exact_name(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"key": "DAEGLJEI", "data": {"name": "James Gross"}},
            {"key": "PNHRTHJS", "data": {"name": "CAD"}},
        ]
        self.assertEqual(zi.get_collection_key("James Gross"), "DAEGLJEI")

    @mock.patch("zotero_import.requests.get")
    def test_raises_for_unknown_name(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        with self.assertRaises(ValueError):
            zi.get_collection_key("Nope")


class TestFindItemByDoi(unittest.TestCase):
    @mock.patch("zotero_import.requests.get")
    def test_finds_exact_doi_match(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"key": "ABC12345", "data": {"DOI": "10.1234/abc"}},
            {"key": "DEF67890", "data": {"DOI": "10.9999/other"}},
        ]
        self.assertEqual(zi.find_item_by_doi("10.1234/abc"), "ABC12345")

    @mock.patch("zotero_import.requests.get")
    def test_returns_none_when_absent(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        self.assertIsNone(zi.find_item_by_doi("10.1234/absent"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 tests/test_zotero_import.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'zotero_import'`

- [ ] **Step 3: Implement module scaffolding + two functions**

```python
"""Import a paper into Zotero from a DOI (LitEngram).

Pipeline: dedup -> CrossRef metadata -> PDF fetch -> Web API create.
Each step is a pure function so it can be unit-tested in isolation.
"""

import json
import os
import sys
import time
from pathlib import Path

import requests

ZOTERO_USER_ID = int(os.environ.get("ZOTERO_USER_ID", "11261922"))
API_KEY = os.environ.get("ZOTERO_API_KEY", "")
LOCAL_API = "http://127.0.0.1:23119/api/users/0"
WEB_API = f"https://api.zotero.org/users/{ZOTERO_USER_ID}"
API_VERSION = "3"

# env-configured CrossRef / OpenAlex identities (best practice).
CROSSREF_MAILTO = os.environ.get("CROSSREF_MAILTO", "litengram@example.com")


def web_headers():
    if not API_KEY:
        raise RuntimeError(
            "ZOTERO_API_KEY 未设置。请先: export ZOTERO_API_KEY='<key>'"
        )
    return {
        "Zotero-API-Key": API_KEY,
        "Zotero-API-Version": API_VERSION,
    }


def get_collection_key(collection_name):
    """Return Zotero collection key for a collection name.

    Raises ValueError if name not found in the user's library.
    """
    resp = requests.get(f"{LOCAL_API}/collections", timeout=10)
    resp.raise_for_status()
    for col in resp.json():
        if col.get("data", {}).get("name") == collection_name:
            return col["key"]
    raise ValueError(f"Collection '{collection_name}' 不存在。")


def find_item_by_doi(doi):
    """Search local Zotero for an item whose DOI matches exactly.

    Returns item key, or None if no match.
    """
    resp = requests.get(
        f"{LOCAL_API}/items",
        params={"q": doi, "qmode": "everything", "limit": 20},
        timeout=10,
    )
    resp.raise_for_status()
    for item in resp.json():
        if item.get("data", {}).get("DOI", "").lower() == doi.lower():
            return item["key"]
    return None
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tests/test_zotero_import.py -v`
Expected: 3 PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/zotero_import.py tests/test_zotero_import.py
git commit -m "feat(zotero-import): collection key resolution + DOI dedup"
```

---

### Task 2: CrossRef metadata resolution

**Files:**
- Modify: `scripts/zotero_import.py`
- Test: `tests/test_zotero_import.py`

- [ ] **Step 1: Write the failing test**

```python
class TestCrossRefMetadata(unittest.TestCase):
    @mock.patch("zotero_import.requests.get")
    def test_maps_crossref_to_zotero_item(self, mock_get):
        crossref = {
            "message": {
                "title": ["Sleep Quality and Mental Health"],
                "author": [
                    {"given": "Xiaoyu", "family": "Zhang"},
                    {"given": "Alice", "family": "Wang"},
                ],
                "container-title": ["Journal of Sleep Research"],
                "issued": {"date-parts": [[2021, 6, 15]]},
                "volume": "42",
                "issue": "3",
                "page": "100-110",
                "DOI": "10.1234/sleep.2021",
                "URL": "https://doi.org/10.1234/sleep.2021",
                "link": [{"URL": "https://publisher.example/paper.pdf"}],
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = crossref

        item = zi.resolve_doi_metadata("10.1234/sleep.2021")

        self.assertEqual(item["itemType"], "journalArticle")
        self.assertEqual(item["title"], "Sleep Quality and Mental Health")
        self.assertEqual(item["DOI"], "10.1234/sleep.2021")
        self.assertEqual(item["date"], "2021-06-15")
        self.assertEqual(item["volume"], "42")
        self.assertEqual(item["issue"], "3")
        self.assertEqual(item["pages"], "100-110")
        self.assertEqual(
            item["creators"],
            [
                {"creatorType": "author", "firstName": "Xiaoyu", "lastName": "Zhang"},
                {"creatorType": "author", "firstName": "Alice", "lastName": "Wang"},
            ],
        )
        self.assertEqual(item["url"], "https://doi.org/10.1234/sleep.2021")
        self.assertEqual(item["_pdf_candidates"], ["https://publisher.example/paper.pdf"])

    @mock.patch("zotero_import.requests.get")
    def test_raises_when_doi_unknown(self, mock_get):
        mock_get.return_value.status_code = 404
        with self.assertRaises(RuntimeError):
            zi.resolve_doi_metadata("10.1234/unknown")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_zotero_import.py TestCrossRefMetadata -v`
Expected: FAIL — `AttributeError: module 'zotero_import' has no attribute 'resolve_doi_metadata'`

- [ ] **Step 3: Implement**

```python
def _first_author(creator):
    return {
        "creatorType": "author",
        "firstName": creator.get("given", ""),
        "lastName": creator.get("family", ""),
    }


def resolve_doi_metadata(doi):
    """Fetch CrossRef metadata for a DOI and map it to a Zotero item dict.

    Returns dict with _pdf_candidates (Crossref 'link' URLs) attached as a
    private key consumed by the PDF fetch step.
    """
    doi = doi.strip()
    resp = requests.get(
        f"https://api.crossref.org/works/{doi}",
        params={"mailto": CROSSREF_MAILTO},
        headers={"User-Agent": f"litengram/1.0 (mailto:{CROSSREF_MAILTO})"},
        timeout=15,
    )
    if resp.status_code == 404:
        raise RuntimeError(f"DOI 未找到: {doi}")
    resp.raise_for_status()
    msg = resp.json()["message"]

    date_parts = (msg.get("issued") or {}).get("date-parts", [[None]])
    year, month, day = (date_parts[0] + [None] * 3)[:3]
    date = "-".join(str(p) for p in (year, month, day) if p)

    pdf_candidates = [
        link["URL"] for link in msg.get("link", []) if link.get("URL")
    ]

    return {
        "itemType": "journalArticle",
        "title": (msg.get("title") or [""])[0],
        "creators": [_first_author(a) for a in msg.get("author", [])],
        "date": date,
        "DOI": msg.get("DOI", doi),
        "url": msg.get("URL", f"https://doi.org/{doi}"),
        "publicationTitle": (msg.get("container-title") or [""])[0],
        "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""),
        "pages": msg.get("page", ""),
        "publisher": msg.get("publisher", ""),
        "_pdf_candidates": pdf_candidates,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_zotero_import.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/zotero_import.py tests/test_zotero_import.py
git commit -m "feat(zotero-import): CrossRef metadata resolution"
```

---

### Task 3: PDF acquisition (OpenAlex OA + Crossref link fallback)

**Files:**
- Modify: `scripts/zotero_import.py`
- Test: `tests/test_zotero_import.py`

- [ ] **Step 1: Write the failing tests**

```python
class TestPdfFetch(unittest.TestCase):
    @mock.patch("zotero_import.requests.get")
    def test_downloads_oa_pdf(self, mock_get):
        page = mock_get.return_value = mock.Mock()
        page.status_code = 200
        page.content = b"%PDF-1.4 fake"

        # OpenAlex query response
        oa_query = mock.Mock()
        oa_query.status_code = 200
        oa_query.json.return_value = {
            "results": [
                {
                    "best_oa_location": {
                        "pdf_url": "https://oal.example/x.pdf",
                    }
                }
            ]
        }
        pdf_get = mock.Mock()
        pdf_get.status_code = 200
        pdf_get.content = b"%PDF-1.4 fake"

        mock_get.side_effect = [oa_query, pdf_get]

        path = zi.download_pdf(
            "10.1234/sleep.2021",
            _pdf_candidates=["https://publisher.example/paper.pdf"],
            out_dir="/tmp/zotero_import_test",
        )
        self.assertIsNotNone(path)
        self.assertEqual(path.read_bytes(), b"%PDF-1.4 fake")
        self.assertEqual(mock_get.call_count, 2)

    @mock.patch("zotero_import.requests.get")
    def test_returns_none_when_not_oa(self, mock_get):
        oa_query = mock.Mock()
        oa_query.status_code = 200
        oa_query.json.return_value = {"results": []}
        mock_get.return_value = oa_query

        path = zi.download_pdf("10.1234/paywalled", _pdf_candidates=[], out_dir="/tmp/zotero_import_test")
        self.assertIsNone(path)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 tests/test_zotero_import.py TestPdfFetch -v`
Expected: FAIL — `AttributeError: module 'zotero_import' has no attribute 'download_pdf'`

- [ ] **Step 3: Implement**

```python
def download_pdf(doi, _pdf_candidates=None, out_dir="/tmp/litengram_pdfs"):
    """Fetch an open-access PDF for the DOI.

    Strategy, in order:
      1. OpenAlex best_oa_location.pdf_url
      2. Crossref 'link' URLs passed in _pdf_candidates
    Returns Path to the PDF, or None if none are downloadable.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    safe = "".join(c for c in doi if c.isalnum() or c in ".-_")
    dest = out_dir / f"{safe}.pdf"

    candidates = []

    try:
        oa = requests.get(
            "https://api.openalex.org/works",
            params={"filter": f"doi:{doi}", "per-page": "1"},
            timeout=15,
        )
        if oa.status_code == 200:
            results = oa.json().get("results", [])
            if results:
                loc = results[0].get("best_oa_location") or {}
                if loc.get("pdf_url"):
                    candidates.append(loc["pdf_url"])
    except Exception:
        pass

    for url in _pdf_candidates or []:
        candidates.append(url)

    for url in candidates:
        try:
            resp = requests.get(url, timeout=30, stream=True, allow_redirects=True)
            if resp.status_code != 200:
                continue
            head = resp.content[:4]
            if head != b"%PDF":
                continue
            with open(dest, "wb") as f:
                f.write(resp.content)
            return dest
        except Exception:
            continue
    return None
```

> Note: `responses.raw` streamed reads are avoided on purpose here — `resp.content` is simpler and PDFs are typically a few MB. Do not "optimize" this back to streaming without a real memory problem.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tests/test_zotero_import.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/zotero_import.py tests/test_zotero_import.py
git commit -m "feat(zotero-import): OA PDF download (OpenAlex + Crossref fallback)"
```

---

### Task 4: Web API item creation (parent + uploaded attachment + collection)

**Files:**
- Modify: `scripts/zotero_import.py`
- Test: `tests/test_zotero_import.py`

- [ ] **Step 1: Write the failing tests**

```python
class TestCreateItem(unittest.TestCase):
    def setUp(self):
        self.item = {
            "itemType": "journalArticle",
            "title": "Sleep Quality and Mental Health",
            "creators": [{"creatorType": "author", "firstName": "Xiaoyu", "lastName": "Zhang"}],
            "date": "2021-06-15",
            "DOI": "10.1234/sleep.2021",
            "collections": ["DAEGLJEI"],
        }

    @mock.patch("zotero_import.requests.post")
    @mock.patch("zotero_import.API_KEY", "test-key")
    def test_creates_parent_and_returns_key(self, mock_post):
        parent_response = mock.Mock()
        parent_response.status_code = 201
        parent_response.json.return_value = {"successful": {"0": {"key": "ABC11111"}}}
        mock_post.return_value = parent_response

        parent_key, attachment_key = zi.create_item_with_attachment(
            self.item,
            pdf_path=None,
            collection_key="DAEGLJEI",
        )
        self.assertEqual(parent_key, "ABC11111")
        self.assertIsNone(attachment_key)

        call_kwargs = mock_post.call_args
        self.assertIn(self.item["collections"], [self.item["collections"]])
        # parent payload contains target collection
        sent = call_kwargs.kwargs.get("data") or call_kwargs.kwargs.get("json")
        if isinstance(sent, list):
            sent = sent[0]
        self.assertEqual(sent["collections"], ["DAEGLJEI"])

    @mock.patch("zotero_import.requests.post")
    @mock.patch("zotero_import.API_KEY", "test-key")
    def test_raises_without_api_key(self, mock_post):
        with mock.patch("zotero_import.API_KEY", ""):
            with self.assertRaises(RuntimeError):
                zi.create_item_with_attachment(self.item, pdf_path=None, collection_key="DAEGLJEI")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 tests/test_zotero_import.py TestCreateItem -v`
Expected: FAIL — `AttributeError: module 'zotero_import' has no attribute 'create_item_with_attachment'`

- [ ] **Step 3: Implement**

```python
def _post_items(payload):
    """POST one item (dict) or a list of items; returns {key: name_code}."""
    resp = requests.post(
        f"{WEB_API}/items",
        headers=web_headers(),
        json=payload,
        timeout=30,
    )
    if resp.status_code not in (201, 200):
        raise RuntimeError(
            f"Zotero Web API 创建条目失败 ({resp.status_code}): {resp.text[:300]}"
        )
    body = resp.json()
    failed = body.get("failed", {})
    if failed:
        raise RuntimeError(f"Zotero 拒绝条目: {json.dumps(failed)[:300]}")
    return {code: meta["key"] for code, meta in body.get("successful", {}).items()}


def create_item_with_attachment(item, pdf_path=None, collection_key=None):
    """Create the parent item (and PDF attachment if pdf_path given).

    Args:
        item: Zotero item dict from resolve_doi_metadata().
        pdf_path: Path to a validated PDF, or None.
        collection_key: collection key to place the item in.

    Returns:
        (parent_key, attachment_key_or_None)
    """
    if collection_key:
        item.setdefault("collections", [])
        if collection_key not in item["collections"]:
            item["collections"].append(collection_key)

    # --- In Zotero Web API v3, if you attach a file you must upload it in
    # --- the SAME POST as the parent item using multipart, OR import the
    # --- file separately. We use the multipart "json + file" form so the
    # --- file is stored on cloud storage with linkMode=imported_file.
    if pdf_path is not None and Path(pdf_path).exists():
        filename = Path(pdf_path).name
        attachment = {
            "itemType": "attachment",
            "linkMode": "imported_file",
            "title": filename,
            "filename": filename,
        }
        # multipart/form-data with 'json' + 'file' parts
        with open(pdf_path, "rb") as f:
            files = {
                "json": (
                    None,
                    json.dumps({**item, "collections": item.get("collections", [])}),
                    "application/json",
                ),
            }
            resp = requests.post(
                f"{WEB_API}/items",
                headers=web_headers(),
                files=files,
                timeout=120,
            )
        # parent item created -> grab its key
        if resp.status_code in (201, 200):
            body = resp.json()
            failed = body.get("failed", {})
            if not failed:
                parent_key = body["successful"]["0"]["key"]
            else:
                raise RuntimeError(f"Zotero 拒绝条目: {json.dumps(failed)[:300]}")
        else:
            raise RuntimeError(f"Zotero Web API 创建条目失败 ({resp.status_code}): {resp.text[:300]}")

        # Now import the file as an attachment under parent_key.
        with open(pdf_path, "rb") as f:
            files = {
                "json": (None, json.dumps(attachment), "application/json"),
                "file": (filename, f, "application/pdf"),
            }
            resp2 = requests.post(
                f"{WEB_API}/items",
                headers=web_headers(),
                files=files,
                timeout=120,
            )
        if resp2.status_code in (201, 200):
            attach_key = resp2.json()["successful"]["0"]["key"]
            return parent_key, attach_key
        raise RuntimeError(f"PDF 附件上传失败 ({resp2.status_code})")
    else:
        # No PDF: single JSON POST for the parent item only.
        keys = _post_items(item)
        return keys["0"], None
```

> **Note for the implementer:** The multipart upload format above is the exact documented Web API v3 pattern (`json` field holds item metadata with `linkMode: imported_file`, `file` field holds the bytes). If the API rejects it with 400, the most common fix is verifying the key has write access (`GET /keys/current` → `access.user.library: true`) and that `Zotero-API-Version: 3` header is present. Both are covered by `web_headers()`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tests/test_zotero_import.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/zotero_import.py tests/test_zotero_import.py
git commit -m "feat(zotero-import): Web API create parent + uploaded attachment + collection"
```

---

### Task 5: CLI orchestration

**Files:**
- Modify: `scripts/zotero_import.py`

- [ ] **Step 1: Implement `main()`**

Add at the end of `scripts/zotero_import.py`:

```python
def main(argv=None):
    """CLI: python3 zotero_import.py <DOI> <collection_name> [--pdf-dir DIR]

    Prints JSON result: {item_key, attachment_key, pdf_status, collection_key}
    Exit code 0 on success, 1 on missing-key/unknown-collection, 2 on failure.
    """
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("doi", help="DOI, e.g. 10.1037/emo0000000")
    ap.add_argument("collection", help="Zotero collection/folder name, e.g. 'James Gross'")
    ap.add_argument("--pdf-dir", default="/tmp/litengram_pdfs", help="where to cache PDFs")
    args = ap.parse_args(argv)

    try:
        collection_key = get_collection_key(args.collection)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    existing = find_item_by_doi(args.doi)
    if existing:
        print(json.dumps(
            {
                "item_key": existing,
                "attachment_key": None,
                "pdf_status": "exists",
                "collection_key": collection_key,
                "message": "论文已在 Zotero，跳过导入。可直接走标注管线。",
            },
            ensure_ascii=False,
        ))
        return 0

    try:
        meta = resolve_doi_metadata(args.doi)
        pdf = download_pdf(args.doi, meta.pop("_pdf_candidates", None), args.pdf_dir)
        parent_key, attachment_key = create_item_with_attachment(
            meta, pdf_path=pdf, collection_key=collection_key
        )
    except RuntimeError as e:
        print(f"失败: {e}", file=sys.stderr)
        return 2

    print(json.dumps(
        {
            "item_key": parent_key,
            "attachment_key": attachment_key,
            "pdf_status": "imported" if pdf else "no_pdf",
            "collection_key": collection_key,
            "message": "导入完成，可走标注管线。",
        },
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Sanity check the CLI against the live library**

Run: `ZOTERO_API_KEY='' python3 scripts/zotero_import.py 10.1234/whatever "James Gross" 2>&1; echo "exit=$?"`
Expected: exit `2` (key missing → `web_headers` raises RuntimeError) — confirms the no-key path fails cleanly.

Then, with the real key set (user runs in their own shell, key not shared to the model):

Run: `python3 scripts/zotero_import.py "10.1234/sleep.2021" "James Gross"`
Expected (dedup path — Zhang 2021 already imported): exit `0`, JSON `{"pdf_status": "exists", ...}`.

- [ ] **Step 3: Remove the temporary sanity check note from any docs? (No — nothing to clean up.)**
- [ ] **Step 4: Commit**

```bash
git add scripts/zotero_import.py
git commit -m "feat(zotero-import): CLI orchestration doi + collection -> Zotero"
```

---

### Task 6: Pipeline integration + docs

**Files:**
- Modify: `SKILL.md` (add trigger + usage note)
- Modify: `references/stage_1-2_intake.md` (note `pdf_status: not_imported` now resolves via `zotero_import`)

- [ ] **Step 1: Update `references/stage_1-2_intake.md`**

Replace the 2a/2b block's header so intake first calls the importer when the paper is missing:

```markdown
**步骤 2a: 若论文不在 Zotero，先导入**

当 dedup 结果显示论文不在 Zotero（`pdf_status: not_imported`），在运行标注管线之前先执行：

```bash
python3 scripts/zotero_import.py "{DOI}" "{collection_name}"
# 输出: {"item_key": "...", "attachment_key": "...", "pdf_status": "imported|no_pdf", "collection_key": "..."}
```

- `pdf_status == imported` → 正常走标注管线
- `pdf_status == no_pdf` → 走降级（abstract-only）管线
- `pdf_status == exists` → 论文已存在，跳过导入
```

- [ ] **Step 2: Update `SKILL.md` trigger + stage table**

Add a line to the trigger section:

```markdown
  - 给我 DOI 存进 Zotero 指定文件夹 / 导入这篇 / import this DOI into <folder>
```

And update the Stage 1-2 row's "输入" cell to note DOI import:

```markdown
| 1-2 Intake | `task()` | 论文标识（DOI / key / 标题）+ Zotero collection 导入（`zotero_import.py`） | 优先级 + 上下文 + PDF 全文 + 标注清单 + litreview_dir |
```

- [ ] **Step 3: Update `references/zotero_workflow.md`**

Append a section:

```markdown
### 八、DOI 导入（新）— zotero_import.py

```
DOI + collection 名 → Zotero 条目 + 附件 (+ OA PDF) 一键导入
dedup → CrossRef 元数据 → OpenAlex/Crossref PDF → Web API 新建（含 collection 挂载）
ZOTERO_API_KEY 必须拥有 write 权限（api.zotero.org）。无 PDF 时降级 abstract-only 标注。
```
```

- [ ] **Step 4: Commit**

```bash
git add SKILL.md references/stage_1-2_intake.md references/zotero_workflow.md
git commit -m "docs(zotero-import): pipeline integration for DOI import flow"
```

---

### Task 7: End-to-end verification with the user's real key

**Files:**
- None (verification only)

- [ ] **Step 1: Confirm the key has write access**

Run (user's shell, so their key never enters the model context):
```bash
curl -s -H "Zotero-API-Key: $ZOTERO_API_KEY" https://api.zotero.org/keys/current | python3 -m json.tool
```
Expected: `access.user.library` shows `true`.

- [ ] **Step 2: Import a real paper into a scratch collection**

User provides a DOI (any paper) + a scratch collection name (e.g. create a throwaway "★ import test" folder in Zotero first), then runs:

```bash
python3 scripts/zotero_import.py "<DOI>" "★ import test"
```

- [ ] **Step 3: Verify in Zotero desktop**

Expected: after sync, the item appears under the specified folder with PDF attached (if OA) and the annotation pipeline (`Stage 4-5`) can locate it. Confirm with:

```bash
curl -s "http://127.0.0.1:23119/api/users/0/items/{item_key}/children"
```

- [ ] **Step 4: No commit (verification only)**

---

## Self-Review

**Spec coverage:**
- DOI → Zotero in specified folder → Task 4 (collection key baked into parent `collections`), Task 5 (CLI takes collection name), Task 1 (name→key).
- → derives annotatable item: Task 4 produces `item_key` + `attachment_key`; Task 6 wires the existing Stage 1-2 intake / annotation pipeline to consume it.
- Missing PDF: Task 3 returns None → Task 4/5 emit `pdf_status: no_pdf` → Task 6 routes to abstract-only downgrade (existing behavior).
- Dedup: Task 1 `find_item_by_doi` prevents duplicates, surfaced in Task 5 `pdf_status: exists`.
- Testability: each task is TDD with stdlib `unittest` + `unittest.mock`; no network in unit tests.

**Placeholder scan:** No TBD/TODO. All code inline. Edge cases (missing key, unknown collection, 404 DOI, paywalled paper, 400 on multipart) each have explicit handling + clear error messages.

**Type consistency:**
- `get_collection_key(name) -> str`; `find_item_by_doi(doi) -> str|None`
- `resolve_doi_metadata(doi) -> dict` (extra `_pdf_candidates` key consumed by `download_pdf(doi, _pdf_candidates, out_dir) -> Path|None`)
- `create_item_with_attachment(item, pdf_path, collection_key) -> (parent_key, attachment_key|None)`
- `main() -> int`; Task 5 JSON keys (`item_key`, `attachment_key`, `pdf_status`, `collection_key`, `message`) reused in Task 6 docs.