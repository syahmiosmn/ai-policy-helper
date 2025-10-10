import os, re, hashlib
from typing import List, Dict, Tuple
from .settings import settings

def _read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def _md_sections(text: str) -> List[Tuple[str, str]]:
    # Very simple section splitter by Markdown headings
    parts = re.split(r"\n(?=#+\s)", text)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        lines = p.splitlines()
        title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("#") else "Body"
        out.append((title, p))
    return out or [("Body", text)]

def clean_text_for_embedding(text: str) -> str:
    # Remove markdown bold, italics, links
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    # Optionally prepend section type for context
    return text

def infer_type_from_section(title: str) -> str:
    title = title.lower().strip()
    title = re.sub(r"[^a-z0-9]+", "_", title)  # replace spaces/punctuation with underscore
    return title or "body"

def chunk_text(text: str, chunk_size=50, overlap=10):
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = tokens[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        if i + chunk_size >= len(tokens):
            break
        i += chunk_size - overlap
    return chunks

def load_documents(data_dir: str) -> List[dict]:
    docs = []
    for fname in sorted(os.listdir(data_dir)):
        if not fname.lower().endswith((".md", ".txt")):
            continue
        path = os.path.join(data_dir, fname)
        text = _read_text_file(path)
        for section, body in _md_sections(text):
            t = infer_type_from_section(section)  # e.g., "sla"
            clean_body = clean_text_for_embedding(body)
            text_to_embed = f"[{type}] {clean_body}"
            
            docs.append({
                "title": fname,
                "section": section,
                "text": text_to_embed,
                "type": t
            })
    return docs


def doc_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
