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
    "TheHackersNews": "https://thehackernews.com/feeds/posts/default",
    "CERT-FR": "https://www.cert.ssi.gouv.fr/feed/",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
    "Bleeping Computer": "https://www.bleepingcomputer.com/feed/",
}

CATEGORY_KEYWORDS = {
    "malware": ["malware", "ransomware", "trojan", "virus"],
    "vulnerability": ["cve", "vulnerability", "exploit", "patch"],
    "data_breach": ["breach", "leak", "data exposed"],
    "phishing": ["phishing", "smishing"],
    "cloud": ["aws", "azure", "gcp", "cloud"],
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
        response = httpx.get(url, timeout=10.0, follow_redirects=True, headers={"User-Agent": "EchatsProBot/1.0"})
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
