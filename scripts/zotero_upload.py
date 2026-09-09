"""Zotero Web API upload: DOI -> top-level item -> PDF attachment.

Full flow, verified against Zotero Web API v3:
  1. Find existing item by DOI (or create via CrossRef metadata)
  2. Create child attachment (linkMode=imported_file) -- WITHOUT md5/mtime
  3. POST /items/{key}/file -> S3 upload authorization (params mode)
  4. POST file to S3 (multipart, key first, file last)
  5. POST /items/{key}/file upload=<uploadKey> -> register
  6. Verify md5 on the attachment item

Usage:
  python3 zotero_upload.py --doi 10.1093/scan/nsaf102 --pdf /tmp/paper.pdf --collection CAD
  python3 zotero_upload.py --item-key 9BKZ3QUE --pdf /tmp/paper.pdf
  # manual mode: download PDF to inbox, print drag-into-Zotero hints, upload nothing
  python3 zotero_upload.py --manual --doi 10.1093/scan/nsaf102
  python3 zotero_upload.py --manual --item-key 9BKZ3QUE

Env:
  ZOTERO_API_KEY  (required for auto upload; needed for --manual too to fetch PDF)
  ZOTERO_USER_ID  (default 11261922)
  LITENGRAM_PDF_INBOX  (download dir; default ~/Zotero/pdf-inbox/)

Notes / pitfalls learned the hard way:
  - Attachment must be created WITHOUT md5/mtime. If md5 is set at creation,
    upload auth fails with 412 "If-None-Match: * set but file exists"
    (WebDAV sync mode treats the md5 as "file already present").
  - Upload auth needs If-None-Match: * and Content-Type
    application/x-www-form-urlencoded (NOT multipart).
  - S3 POST must send the signed params as form fields; 'key' first, 'file' last.
  - mtime is in MILLISECONDS.
  - Zotero item keys are 8 chars from [2-9A-NP-Z] (no 0/1/O). The API assigns
    keys on item creation; never hand-generate keys for Web API items.

Storage protocol guard:
  Auto upload pushes files to Zotero File Storage (S3). If the client is in
  WebDAV mode (extensions.zotero.sync.storage.protocol = webdav), the file
  lands in S3 where the WebDAV client can never fetch it -> orphan attachment.
  Auto mode aborts with a hint to use --manual when WebDAV is detected.
  Use --force to override the guard.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import requests

API = "https://api.zotero.org"
# No personal-account fallback: a missing ZOTERO_USER_ID used to silently
# default to the original author's own numeric Zotero user ID, so anyone
# else running this without setting the env var would quietly operate
# against (or 403/404 against) someone else's library instead of failing
# clearly. USER_ID is 0 (invalid) until _require_user_id() is called.
USER_ID = int(os.environ.get("ZOTERO_USER_ID", "0"))
API_KEY = os.environ.get("ZOTERO_API_KEY", "")

HEADERS = {"Zotero-API-Key": API_KEY, "Zotero-API-Version": "3"}


def _require_user_id():
    if not os.environ.get("ZOTERO_USER_ID"):
        sys.exit("✗ ZOTERO_USER_ID 未设置：请显式设置该环境变量，不要依赖默认账号")


def _hdr():
    if not API_KEY:
        sys.exit("ZOTERO_API_KEY not set")
    return dict(HEADERS)


# ---------------------------------------------------------------- lookup ---

def find_item_by_doi(doi):
    """Return existing top-level item dict for DOI, or None.

    Zotero quicksearch does not index DOI reliably, so search by a
    distinctive title token (from CrossRef) and compare DOI exactly.
    """
    try:
        meta = crossref_meta(doi)
        title = meta.get("title", "") or ""
    except Exception:
        title = ""
    # distinctive first word(s) of title; drop stopwords
    tokens = [t for t in title.split() if len(t) > 3 and t.lower() not in
              ("the", "and", "for", "with", "from", "that", "this", "context")]
    if not tokens:
        tokens = [t for t in title.split() if len(t) > 3]
    queries = [" ".join(tokens[:3])] + [tokens[0]] if tokens else [doi]
    seen = set()
    for q in queries:
        if q in seen:
            continue
        seen.add(q)
        r = requests.get(
            f"{API}/users/{USER_ID}/items",
            headers=_hdr(),
            params={"q": q, "qmode": "everything", "itemType": "journalArticle", "limit": 25},
            timeout=30,
        )
        r.raise_for_status()
        for it in r.json():
            d = it.get("data", {})
            if d.get("DOI", "").lower() == doi.lower():
                return it
    return None


def resolve_collection(name):
    """Resolve collection key by name. Returns key or None."""
    r = requests.get(f"{API}/users/{USER_ID}/collections", headers=_hdr(), timeout=30)
    r.raise_for_status()
    for c in r.json():
        if c.get("data", {}).get("name") == name:
            return c["key"]
    return None


# ---------------------------------------------------------------- create ---

def crossref_meta(doi):
    """Fetch CrossRef metadata and map to a Zotero item JSON."""
    r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=30)
    r.raise_for_status()
    m = r.json()["message"]

    creators = []
    for a in m.get("author", []):
        if "family" in a:
            creators.append(
                {"creatorType": "author", "firstName": a.get("given", ""), "lastName": a.get("family", "")}
            )
        elif "name" in a:
            creators.append({"creatorType": "author", "name": a["name"]})

    date_parts = (m.get("issued", {}) or {}).get("date-parts", [[None]])[0]
    date = "-".join(str(p) for p in date_parts if p)

    container = m.get("container-title") or m.get("short-container-title") or []
    item = {
        "itemType": "journalArticle",
        "title": m.get("title", [""])[0],
        "creators": creators,
        "DOI": doi,
        "url": m.get("URL", f"https://doi.org/{doi}"),
        "publisher": m.get("publisher", ""),
        "publicationTitle": container[0] if container else "",
        "date": date,
        "volume": m.get("volume", ""),
        "issue": m.get("issue", ""),
        "pages": m.get("page", ""),
        "abstractNote": (m.get("abstract", "") or "")
        .replace("<jats:p>", "")
        .replace("</jats:p>", "")
        .replace("<jats:title>", "")
        .replace("</jats:title>", ""),
        "relations": {},
    }
    return item


def create_item(doi, collection_key=None):
    """Create top-level journalArticle from CrossRef. Returns item key."""
    item = crossref_meta(doi)
    if collection_key:
        item["collections"] = [collection_key]
    r = requests.post(f"{API}/users/{USER_ID}/items", headers=_hdr(), json=[item], timeout=30)
    if r.status_code != 200:
        sys.exit(f"create_item failed {r.status_code}: {r.text[:300]}")
    res = r.json()
    if not res.get("successful"):
        sys.exit(f"create_item rejected: {json.dumps(res, ensure_ascii=False)[:300]}")
    return res["successful"]["0"]["key"]


def create_attachment(parent_key, filename, title=None):
    """Create child attachment item. IMPORTANT: no md5/mtime fields."""
    item = {
        "itemType": "attachment",
        "parentItem": parent_key,
        "linkMode": "imported_file",
        "title": title or filename,
        "filename": filename,
        "contentType": "application/pdf",
        "collections": [],
        "relations": {},
    }
    r = requests.post(f"{API}/users/{USER_ID}/items", headers=_hdr(), json=[item], timeout=30)
    if r.status_code != 200:
        sys.exit(f"create_attachment failed {r.status_code}: {r.text[:300]}")
    res = r.json()
    if not res.get("successful"):
        sys.exit(f"create_attachment rejected: {json.dumps(res, ensure_ascii=False)[:300]}")
    return res["successful"]["0"]["key"]


# ---------------------------------------------------------------- upload ---

def upload_pdf(attachment_key, pdf_path):
    """Authorize S3 upload, POST file, register. Raises on failure."""
    data = pdf_path.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    size = len(data)
    mtime = int(pdf_path.stat().st_mtime * 1000)  # milliseconds!
    filename = pdf_path.name

    # 1. upload authorization
    auth = requests.post(
        f"{API}/users/{USER_ID}/items/{attachment_key}/file",
        headers={**_hdr(), "If-None-Match": "*"},
        data={"md5": md5, "filename": filename, "filesize": size, "mtime": mtime, "params": 1},
        timeout=30,
    )
    if auth.status_code == 412:
        sys.exit(
            "upload auth 412 'file exists': the library already has a file with "
            "this md5 (Zotero dedupes identical files) or the attachment was "
            "created with md5. Delete this empty attachment and reuse the "
            "existing one: the same-content PDF is already attached elsewhere."
        )
    if auth.status_code != 200:
        sys.exit(f"upload auth failed {auth.status_code}: {auth.text[:300]}")
    a = auth.json()
    if a.get("exists"):
        print("file already exists on server; associated with item")
        return
    params, upload_key = a["params"], a["uploadKey"]

    # 2. POST to S3. Signed fields in order: key first, ... file last.
    field_order = [
        "key", "acl", "Content-MD5", "success_action_status", "policy",
        "x-amz-algorithm", "x-amz-credential", "x-amz-date",
        "x-amz-signature", "x-amz-security-token",
    ]
    files = {"file": (filename, data, "application/pdf")}
    form = {k: params[k] for k in field_order if k in params}
    s3 = requests.post(a["url"], data=form, files=files, timeout=180)
    if s3.status_code != 201:
        sys.exit(f"S3 upload failed {s3.status_code}: {s3.text[:300]}")

    # 3. register
    reg = requests.post(
        f"{API}/users/{USER_ID}/items/{attachment_key}/file",
        headers={**_hdr(), "If-None-Match": "*"},
        data={"upload": upload_key},
        timeout=30,
    )
    if reg.status_code not in (200, 204):
        sys.exit(f"register failed {reg.status_code}: {reg.text[:300]}")


def verify_attachment(attachment_key):
    """Check attachment md5 was registered."""
    r = requests.get(f"{API}/users/{USER_ID}/items/{attachment_key}", headers=_hdr(), timeout=30)
    r.raise_for_status()
    return r.json()["data"].get("md5")


# ----------------------------------------------------------------- main ---

def detect_storage_protocol():
    """Read Zotero client file-sync protocol from prefs.js.

    Returns:
        'webdav' / 'zotero' / None (unknown or not found)
    """
    profiles = Path.home() / "Library" / "Application Support" / "Zotero" / "Profiles"
    if not profiles.exists():
        return None
    pat = re.compile(r'extensions\.zotero\.sync\.storage\.protocol",\s*"(\w+)"')
    for pref in sorted(glob.glob(str(profiles / "*" / "prefs.js"))):
        try:
            text = Path(pref).read_text()
        except OSError:
            continue
        m = pat.search(text)
        if m:
            return m.group(1)
    return None


def guard_storage_protocol(force):
    """Abort auto upload in WebDAV mode unless --force.

    WebDAV-mode clients cannot fetch files pushed to Zotero File Storage (S3),
    producing orphan attachments. Manual mode never touches S3.
    """
    if force:
        return
    proto = detect_storage_protocol()
    if proto == "webdav":
        sys.exit(
            "✗ 检测到 Zotero 客户端文件同步为 WebDAV 模式\n"
            "  Web API 自动上传会把文件放进 Zotero S3，WebDAV 客户端永远拉不到（孤儿附件）。\n"
            "  ▸ 改用手动模式: python3 zotero_upload.py --manual --doi <DOI>\n"
            "  ▸ 确认坚持自动上传: 加 --force"
        )


def main():
    ap = argparse.ArgumentParser(description="Zotero DOI -> item -> PDF upload")
    ap.add_argument("--doi", help="DOI of the paper")
    ap.add_argument("--item-key", help="Existing Zotero item key (skip DOI lookup)")
    ap.add_argument("--pdf", help="Path to the PDF file (auto mode only)")
    ap.add_argument("--collection", help="Collection name (e.g. CAD) to add item to")
    ap.add_argument("--manual", action="store_true",
                    help="Download PDF to inbox and print manual attach hints; no upload")
    ap.add_argument("--force", action="store_true",
                    help="Skip WebDAV-mode guard (auto upload anyway)")
    args = ap.parse_args()

    _require_user_id()

    if not args.item_key and not args.doi:
        sys.exit("✗ 需提供 --doi 或 --item-key")
    if args.manual:
        run_manual(args.doi, args.item_key)
        return

    guard_storage_protocol(args.force)

    if not args.pdf:
        sys.exit("✗ 自动模式需 --pdf 路径（或加 --manual 仅下载）")
    pdf = Path(args.pdf).expanduser().resolve()
    if not pdf.exists():
        sys.exit(f"✗ PDF 不存在: {pdf}")

    # parent item
    if args.item_key:
        parent_key = args.item_key
        print(f"✓ 使用已有条目 {parent_key}")
    else:
        existing = find_item_by_doi(args.doi)
        if existing:
            parent_key = existing["key"]
            print(f"✓ 条目已存在: {parent_key} ({existing['data'].get('title', '')[:50]})")
        else:
            col_key = resolve_collection(args.collection) if args.collection else None
            parent_key = create_item(args.doi, col_key)
            print(f"✓ 已建条目 {parent_key} (collection={col_key or 'none'})")

    # attachment + upload
    att_key = create_attachment(parent_key, pdf.name)
    print(f"✓ 附件 {att_key}")
    upload_pdf(att_key, pdf)
    md5 = verify_attachment(att_key)
    print(f"✓ 上传完成: attachment {att_key}, md5={md5}")

    # cleanup failed attachment
    def cleanup():
        """Best-effort delete of the orphaned attachment.

        Previously this read r.json()["version"] and fired the DELETE
        without checking either response's status. If the GET itself
        failed, "version" would just be None and the DELETE would be
        sent with an invalid If-Unmodified-Since-Version header and
        silently fail too — leaving a dangling attachment item in the
        library with no warning that cleanup didn't actually happen.
        """
        r = requests.get(f"{API}/users/{USER_ID}/items/{att_key}", headers=_hdr(), timeout=30)
        if r.status_code != 200:
            print(f"⚠ 清理失败：无法读取附件 {att_key} 的版本号 ({r.status_code})，"
                  f"请手动在 Zotero 里删除这个孤儿附件")
            return
        ver = r.json().get("version")
        d = requests.delete(
            f"{API}/users/{USER_ID}/items/{att_key}",
            headers={**_hdr(), "If-Unmodified-Since-Version": str(ver)},
            timeout=30,
        )
        if d.status_code not in (200, 204):
            print(f"⚠ 清理失败：删除附件 {att_key} 返回 {d.status_code}，"
                  f"请手动在 Zotero 里删除这个孤儿附件")

    if not md5:
        cleanup()
        sys.exit("✗ 上传不完整 (md5 未注册); 附件已删除")


def run_manual(doi, item_key):
    """Download PDF to inbox and print manual attach hints. No upload."""
    from zotero_cloud import download_pdf

    parent = None
    if item_key:
        parent = item_key
        key = find_attachment_key(parent)
        print(f"✓ 条目 {parent} 附件: {key}")
    elif doi:
        existing = find_item_by_doi(doi)
        if not existing:
            sys.exit(f"✗ 库中无此 DOI: {doi}（先跑自动模式建条目，或用 --item-key）")
        parent = existing["key"]
        key = find_attachment_key(parent)
        print(f"✓ 条目 {parent} 附件: {key}")
    else:
        sys.exit("✗ 需提供 --doi 或 --item-key")

    target = download_pdf(key)
    if not target:
        sys.exit("✗ 下载失败")
    here = Path(__file__).resolve()
    print()
    print(f"▸ 挂载: 打开 Finder 拖 {target.name} 进 Zotero 条目 {parent} "
          f"(右键→添加附件→附加文件的副本)")
    print(f"▸ 自动: python3 {here} --item-key {parent} --pdf {target}")


def find_attachment_key(parent_key):
    """Return first PDF attachment key under a top-level item."""
    r = requests.get(f"{API}/users/{USER_ID}/items/{parent_key}/children",
                     headers=_hdr(), timeout=30)
    r.raise_for_status()
    for it in r.json():
        d = it.get("data", {})
        if d.get("itemType") == "attachment" and d.get("contentType") == "application/pdf":
            return d["key"]
    sys.exit(f"✗ 条目 {parent_key} 下无 PDF 附件")


if __name__ == "__main__":
    main()
