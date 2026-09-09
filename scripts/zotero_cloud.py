"""Zotero Cloud PDF download fallback for LitEngram.
Downloads missing PDFs from Zotero Web API when local copy is absent.

PDF inbox: files land in LITENGRAM_PDF_INBOX if set, else ~/Zotero/pdf-inbox/.
"""

import os, shutil, requests
from pathlib import Path

# No personal-account fallback — see zotero_upload.py's USER_ID comment.
# Left at 0 (invalid) until _require_user_id() is called at actual use.
USER_ID = int(os.environ.get("ZOTERO_USER_ID", "0"))
API_KEY = os.environ.get("ZOTERO_API_KEY", "")


def _require_user_id():
    if not os.environ.get("ZOTERO_USER_ID"):
        raise RuntimeError("ZOTERO_USER_ID 未设置：请显式设置该环境变量，不要依赖默认账号")

# Download landing dir: user override wins, else default under Zotero data dir.
PDF_INBOX = Path(os.environ.get("LITENGRAM_PDF_INBOX", "~/Zotero/pdf-inbox")).expanduser().resolve()


def _inbox_message(pdf_path):
    """Human-readable next-step hints after a download."""
    return (
        f"PDF 已下载到:\n"
        f"  {pdf_path}\n"
        f"打开目录:  open {pdf_path.parent}\n"
        f"手动挂载: 拖入 Zotero 对应条目，或 右键→添加附件→附加文件的副本"
    )


def download_pdf(item_key, target_dir=None, filename=None):
    """Download PDF attachment from Zotero cloud to local storage.

    Args:
        item_key: Zotero attachment item key (e.g., '5PUXID52')
        target_dir: Directory to save the PDF. Defaults to PDF_INBOX
            (LITENGRAM_PDF_INBOX or ~/Zotero/pdf-inbox/).
        filename: Optional filename override

    Returns:
        Path to downloaded file, or None on failure.
    """
    if not API_KEY:
        print("✗ 无法下载: ZOTERO_API_KEY 未设置")
        return None
    _require_user_id()

    target_dir = Path(target_dir or PDF_INBOX).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    url = f"https://api.zotero.org/users/{USER_ID}/items/{item_key}/file"
    headers = {
        "Zotero-API-Key": API_KEY,
        "Zotero-API-Version": "3",
    }

    try:
        # First, get attachment metadata to learn filename
        meta_url = f"https://api.zotero.org/users/{USER_ID}/items/{item_key}"
        meta_resp = requests.get(meta_url, headers=headers, timeout=10)
        if meta_resp.status_code == 200:
            meta = meta_resp.json()["data"]
            filename = filename or meta.get("filename", f"{item_key}.pdf")

        # Download the file
        resp = requests.get(url, headers=headers, timeout=60, stream=True)
        if resp.status_code == 200:
            target_path = target_dir / (filename or f"{item_key}.pdf")
            with open(target_path, "wb") as f:
                shutil.copyfileobj(resp.raw, f)
            print(_inbox_message(target_path))
            return target_path
        elif resp.status_code == 404:
            print(f"✗ 下载失败 404: 云端无此附件文件 (attachment {item_key})")
            return None
        else:
            print(f"✗ 下载失败 {resp.status_code}: attachment {item_key}")
            return None
    except Exception as e:
        # Previously silent: a network error / timeout here returned None
        # with no message at all, unlike every other failure path in this
        # function, making it indistinguishable from "file just doesn't
        # exist" during debugging.
        print(f"✗ 下载出错: {e}")
        return None


def ensure_local_pdf(attachment_key, storage_dir, attachment_info=None):
    """Ensure PDF exists locally. Try cloud download if missing.

    Args:
        attachment_key: Zotero attachment item key
        storage_dir: Zotero storage directory path (e.g., ~/Zotero/storage/5PUXID52)
        attachment_info: Optional dict with cached API metadata

    Returns:
        (pdf_path: Path or None, status: str)
        status: 'available' / 'downloaded' / 'unavailable'
    """
    storage_path = Path(storage_dir).expanduser().resolve()

    # Check if PDF already exists locally
    if storage_path.exists():
        pdfs = list(storage_path.glob("*.pdf"))
        if pdfs:
            return pdfs[0], "available"

    # Try cloud download
    if API_KEY:
        pdf = download_pdf(attachment_key, storage_path)
        if pdf and pdf.exists():
            return pdf, "downloaded"

    return None, "unavailable"
