"""Parsing horaire des flux RSS cybersécurité, catégorisation, mise en cache."""
import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree

import httpx
from sqlalchemy.orm import Session

from app.models.news import NewsArticle

logger = logging.getLogger("echats.rss")

# Sources RSS (Partie 11 du SRS)
RSS_FEEDS: dict[str, str] = {
    # === Sources internationales (références mondiales) ===
    "TheHackersNews": "https://thehackernews.com/feeds/posts/default",
    "CERT-FR": "https://www.cert.ssi.gouv.fr/feed/",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
    "Bleeping Computer": "https://www.bleepingcomputer.com/feed/",
    
    # === Sources africaines (souveraineté) ===
    "AfricaCERT": "https://www.africacert.org/feed/",
    "AFRINIC": "https://www.afrinic.net/rss/news.xml",
    
    # === Sources spécialisées ===
    "Google Security Blog": "https://security.googleblog.com/feeds/posts/default",
    "Microsoft Security": "https://www.microsoft.com/en-us/security/blog/feed/",
}

CATEGORY_KEYWORDS = {
    "malware": ["malware", "ransomware", "trojan", "virus", "worm", "spyware", "rootkit"],
    "vulnerability": ["cve", "vulnerability", "exploit", "patch", "0day", "0-day", "zero-day"],
    "data_breach": ["breach", "leak", "data exposed", "exfiltration", "stolen data"],
    "phishing": ["phishing", "smishing", "vishing", "social engineering"],
    "cloud": ["aws", "azure", "gcp", "cloud", "kubernetes", "docker", "container"],
    "apt": ["apt", "state-sponsored", "nation-state", "cyber espionage", "threat actor"],
    "ransomware": ["ransomware", "double extortion", "encryption attack"],
    "ai_security": ["ai security", "llm", "prompt injection", "ai model", "deepfake"],
    "iot": ["iot", "internet of things", "smart device", "firmware"],
    "politics": ["regulation", "gdpr", "law", "government", "policy", "compliance"],
    "africa": ["africa", "african", "afrique", "congo", "nigeria", "kenya", "cemac"],
}


def _categorize(title: str, summary: str) -> str:
    text = f"{title} {summary}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return category
    return "general"


def _parse_rss_item(item: ElementTree.Element, source: str) -> dict | None:
    def _text(tag: str) -> str | None:
        el = item.find(tag)
        return el.text.strip() if el is not None and el.text else None

    title = _text("title")
    link = _text("link")
    if not title or not link:
        return None

    summary = _text("description") or ""
    pub_date_raw = _text("pubDate")
    try:
        published_at = parsedate_to_datetime(pub_date_raw) if pub_date_raw else datetime.now(timezone.utc)
    except (TypeError, ValueError):
        published_at = datetime.now(timezone.utc)

    return {
        "title": title[:300],
        "summary": summary[:1000] if summary else None,
        "url": link,
        "source": source,
        "category": _categorize(title, summary),
        "published_at": published_at,
    }


def fetch_feed(url: str, source: str) -> list[dict]:
    try:
        response = httpx.get(url, timeout=10.0, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (compatible; EchatsPro/1.0; +https://echats-projets.web.app)"})
        response.raise_for_status()
        root = ElementTree.fromstring(response.content)
        items = root.findall(".//item")
        parsed = [_parse_rss_item(item, source) for item in items]
        return [p for p in parsed if p is not None]
    except Exception:
        logger.exception("Échec du parsing du flux RSS %s (%s)", source, url)
        return []


def refresh_all_feeds(db: Session) -> int:
    """Parse tous les flux RSS configurés et insère les nouveaux articles (dédoublonnés par URL)."""
    inserted = 0
    for source, url in RSS_FEEDS.items():
        for entry in fetch_feed(url, source):
            exists = db.query(NewsArticle).filter(NewsArticle.url == entry["url"]).first()
            if exists:
                continue
            db.add(NewsArticle(**entry))
            inserted += 1
    if inserted:
        db.commit()
    return inserted
