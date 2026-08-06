"""Zotero Cloud PDF download fallback for LitEngram.
Downloads missing PDFs from Zotero Web API when local copy is absent.
"""

import os, shutil, requests
from pathlib import Path

USER_ID = int(os.environ.get("ZOTERO_USER_ID", "11261922"))
API_KEY = os.environ.get("ZOTERO_API_KEY", "")


def download_pdf(item_key, target_dir, filename=None):
    """Download PDF attachment from Zotero cloud to local storage.

    Args:
        item_key: Zotero attachment item key (e.g., '5PUXID52')
        target_dir: Directory to save the PDF (typically storage dir)
        filename: Optional filename override

    Returns:
        Path to downloaded file, or None on failure.
    """
    if not API_KEY:
        return None

    target_dir = Path(target_dir).expanduser().resolve()
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
            return target_path
        elif resp.status_code == 404:
            return None
        else:
            return None
    except Exception:
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
