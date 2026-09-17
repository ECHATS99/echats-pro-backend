"""Import en masse : curriculum/echats-coursera/ -> PostgreSQL (Track/CourseModule/Lesson).

Contexte
--------
Le dossier `echats-coursera/` contient ~900 fichiers Markdown/texte répartis en 4
catégories (_CYBER, _PROGRAMMATION, _CLOUD, _NOTES), chacune regroupant plusieurs
dépôts clonés (Dojo-101, Blue-Team-Roadmap, Pentest-References, etc.).

Ce script est DISTINCT de `scripts/import_lessons_to_postgres.py` : ce dernier exige
un manifeste JSON curé à la main (enrichissement + quiz 10-15 questions par leçon),
ce qui est adapté aux 11 leçons "Expertise fédérale" mais pas réaliste pour ~900
fichiers bruts. Ce script-ci fait un mapping direct et automatique :

    _CYBER/                        -> Track "Cybersécurité" (slug: coursera-cyber)
      Dojo-101/                    -> CourseModule "Dojo 101"
        Dojo-101-RF/RFID.md        -> Lesson "Dojo 101 RF — RFID"
      Blue-Team-Roadmap/           -> CourseModule "Blue Team Roadmap"
        README.md                 -> Lesson "Vue d'ensemble" (ou 1er titre # du fichier)

Sécurité (même contrat que import_lessons_to_postgres.py) :
- `--dry-run` par défaut, aucune écriture.
- `--apply` explicite, une seule transaction, rollback si erreur.
- Idempotent : une leçon déjà importée (même module + même titre) est réutilisée,
  jamais réécrite. Relancer le script après avoir ajouté de nouveaux fichiers au
  dossier ne duplique rien et n'écrase rien.
- Les leçons sont importées en `published=False` par défaut (brouillon) : à valider
  et publier depuis l'admin avant d'être visibles publiquement. Utiliser
  --publish pour les publier directement si vous faites confiance au contenu source.

Usage :
    # Aperçu sans écrire (toujours commencer par ça)
    python -m scripts.import_coursera_bulk --dry-run

    # Import réel
    python -m scripts.import_coursera_bulk --apply

    # Import réel + publication immédiate de tout
    python -m scripts.import_coursera_bulk --apply --publish
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DEFAULT_ROOT = REPO_ROOT / "curriculum" / "echats-coursera"

# Extensions traitées comme contenu de leçon (le reste, ex: .png/.py/.tf, est ignoré).
LESSON_EXTENSIONS = {".md", ".txt"}

# Fichiers "boilerplate" de dépôts GitHub : pas de valeur pédagogique propre.
SKIP_FILENAMES = {
    "license", "license.md", "license.txt", "code_of_conduct.md",
    "contributing.md", "issue_template.md", "pull_request_template.md",
    "security.md", "changelog.md", "codeowners", ".gitattributes", ".gitignore",
}

# Catégories -> métadonnées de Track.
CATEGORY_MAP = {
    "_CYBER": {"title": "Cybersécurité (ressources Coursera)", "domain": "cybersecurity", "difficulty": "intermediate"},
    "_PROGRAMMATION": {"title": "Programmation (ressources Coursera)", "domain": "programming", "difficulty": "beginner"},
    "_CLOUD": {"title": "Cloud (ressources Coursera)", "domain": "cloud", "difficulty": "intermediate"},
    "_NOTES": {"title": "Notes & Références (ressources Coursera)", "domain": "reference", "difficulty": "beginner"},
}

WORDS_PER_MINUTE = 200
MIN_WORDS = 30  # fichiers plus courts que ça = pas assez de contenu pour une leçon


class ImportInputError(RuntimeError):
    pass


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return normalized or "item"


def humanize(name: str) -> str:
    name = re.sub(r"\.(md|txt)$", "", name, flags=re.IGNORECASE)
    name = name.replace("_", " ").replace("-", " ")
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)  # camelCase -> mots séparés
    words = [w for w in name.split() if w]
    return " ".join(w if w.isupper() and len(w) <= 5 else w.capitalize() for w in words) or name


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            candidate = stripped.lstrip("#").strip()
            if candidate:
                return candidate[:200]
    return fallback[:200]


@dataclass
class LessonPlan:
    track_slug: str
    track_title: str
    track_domain: str
    track_difficulty: str
    module_title: str
    module_order: int
    lesson_title: str
    lesson_order: int
    content: str
    duration_minutes: int
    source_path: str


@dataclass
class ImportPlan:
    lessons: list[LessonPlan] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def build_plan(root: Path) -> ImportPlan:
    if not root.is_dir():
        raise ImportInputError(f"Dossier introuvable: {root}")
    plan = ImportPlan()
    module_orders: dict[tuple[str, str], int] = {}
    lesson_orders: dict[tuple[str, str], int] = {}
    seen_titles: dict[tuple[str, str], set[str]] = {}

    for category_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        category = category_dir.name
        meta = CATEGORY_MAP.get(category)
        if meta is None:
            plan.skipped.append(f"{category}: catégorie non reconnue, ignorée")
            continue
        track_slug = f"coursera-{slugify(category)}"

        for repo_dir in sorted(p for p in category_dir.iterdir() if p.is_dir()):
            module_title = humanize(repo_dir.name)
            module_key = (track_slug, module_title)
            module_order = module_orders.setdefault(module_key, len(module_orders) + 1)

            files = sorted(
                p for p in repo_dir.rglob("*")
                if p.is_file() and p.suffix.lower() in LESSON_EXTENSIONS
            )
            for file_path in files:
                if file_path.name.lower() in SKIP_FILENAMES:
                    plan.skipped.append(f"{file_path.relative_to(root)}: fichier boilerplate")
                    continue
                try:
                    text = file_path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    plan.skipped.append(f"{file_path.relative_to(root)}: encodage non-UTF-8")
                    continue
                word_count = len(text.split())
                if word_count < MIN_WORDS:
                    plan.skipped.append(f"{file_path.relative_to(root)}: trop court ({word_count} mots)")
                    continue

                breadcrumb_parts = file_path.relative_to(repo_dir).parts[:-1]
                fallback_title = humanize(file_path.stem)
                if breadcrumb_parts:
                    fallback_title = f"{humanize(breadcrumb_parts[-1])} — {fallback_title}"
                lesson_title = extract_title(text, fallback_title)[:200]

                titles_in_module = seen_titles.setdefault(module_key, set())
                base_title = lesson_title
                suffix = 2
                while lesson_title in titles_in_module:
                    lesson_title = f"{base_title} ({suffix})"[:200]
                    suffix += 1
                titles_in_module.add(lesson_title)

                lesson_key = module_key
                lesson_order = lesson_orders.get(lesson_key, 0) + 1
                lesson_orders[lesson_key] = lesson_order

                content = (
                    f"> Source : `{file_path.relative_to(root)}`\n\n" + text.strip()
                )
                plan.lessons.append(LessonPlan(
                    track_slug=track_slug,
                    track_title=meta["title"],
                    track_domain=meta["domain"],
                    track_difficulty=meta["difficulty"],
                    module_title=module_title,
                    module_order=module_order,
                    lesson_title=lesson_title,
                    lesson_order=lesson_order,
                    content=content,
                    duration_minutes=max(5, word_count // WORDS_PER_MINUTE),
                    source_path=str(file_path.relative_to(root)),
                ))
    return plan


def dry_run_payload(plan: ImportPlan) -> dict[str, Any]:
    by_track: dict[str, dict[str, Any]] = {}
    for lesson in plan.lessons:
        track = by_track.setdefault(lesson.track_slug, {"title": lesson.track_title, "modules": {}})
        module = track["modules"].setdefault(lesson.module_title, {"lesson_count": 0})
        module["lesson_count"] += 1
    return {
        "mode": "dry-run",
        "writes_performed": False,
        "totals": {
            "tracks": len(by_track),
            "modules": sum(len(t["modules"]) for t in by_track.values()),
            "lessons": len(plan.lessons),
            "skipped_files": len(plan.skipped),
        },
        "tracks": {
            slug: {"title": t["title"], "modules": {m: v["lesson_count"] for m, v in t["modules"].items()}}
            for slug, t in by_track.items()
        },
        "skipped_sample": plan.skipped[:30],
    }


def apply_plan(plan: ImportPlan, publish: bool) -> dict[str, Any]:
    from sqlalchemy import select

    from app.core.database import SessionLocal
    from app.models.course_module import CourseModule
    from app.models.lesson import Lesson
    from app.models.track import Track

    db = SessionLocal()
    created = {"tracks": 0, "modules": 0, "lessons": 0}
    reused = {"tracks": 0, "modules": 0, "lessons": 0}
    try:
        with db.begin():
            track_cache: dict[str, Track] = {}
            module_cache: dict[tuple[str, str], CourseModule] = {}

            for lesson_plan in plan.lessons:
                track = track_cache.get(lesson_plan.track_slug)
                if track is None:
                    track = db.execute(
                        select(Track).where(Track.slug == lesson_plan.track_slug)
                    ).scalar_one_or_none()
                    if track is None:
                        track = Track(
                            title=lesson_plan.track_title,
                            slug=lesson_plan.track_slug,
                            description="Ressources pédagogiques importées automatiquement depuis echats-coursera.",
                            difficulty=lesson_plan.track_difficulty,
                            domain=lesson_plan.track_domain,
                            published=publish,
                        )
                        db.add(track)
                        db.flush()
                        created["tracks"] += 1
                    else:
                        reused["tracks"] += 1
                    track_cache[lesson_plan.track_slug] = track

                module_key = (lesson_plan.track_slug, lesson_plan.module_title)
                module = module_cache.get(module_key)
                if module is None:
                    module = db.execute(
                        select(CourseModule).where(
                            CourseModule.track_id == track.id,
                            CourseModule.title == lesson_plan.module_title,
                        )
                    ).scalar_one_or_none()
                    if module is None:
                        module = CourseModule(
                            track_id=track.id,
                            title=lesson_plan.module_title,
                            order=lesson_plan.module_order,
                            published=publish,
                        )
                        db.add(module)
                        db.flush()
                        created["modules"] += 1
                    else:
                        reused["modules"] += 1
                    module_cache[module_key] = module

                existing_lesson = db.execute(
                    select(Lesson).where(
                        Lesson.module_id == module.id,
                        Lesson.title == lesson_plan.lesson_title,
                    )
                ).scalar_one_or_none()
                if existing_lesson is None:
                    db.add(Lesson(
                        module_id=module.id,
                        title=lesson_plan.lesson_title,
                        content=lesson_plan.content,
                        duration_minutes=lesson_plan.duration_minutes,
                        order=lesson_plan.lesson_order,
                        published=publish,
                    ))
                    created["lessons"] += 1
                else:
                    reused["lessons"] += 1
        return {"mode": "apply", "writes_performed": True, "created": created, "reused": reused}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Aperçu sans écrire (par défaut).")
    mode.add_argument("--apply", action="store_true", help="Écrit réellement en base.")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="Chemin vers echats-coursera/.")
    parser.add_argument("--publish", action="store_true", help="Marque tracks/modules/leçons créés comme publiés.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = "apply" if args.apply else "dry-run"
    try:
        plan = build_plan(Path(args.root))
        if args.apply:
            result = apply_plan(plan, publish=args.publish)
        else:
            result = dry_run_payload(plan)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except ImportInputError as exc:
        print(json.dumps({"mode": mode, "writes_performed": False, "status": "blocked", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"mode": mode, "writes_performed": False, "status": "failed", "error_type": type(exc).__name__, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
