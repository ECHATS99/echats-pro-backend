"""Import v2 : curriculum/echats-coursera/ -> PostgreSQL.

Gère :
- ECHATS PRO (dossiers 01-*, 02-*, etc.) avec frontmatter YAML
- Open Source (datacarpentry, _CYBER, etc.) avec attribution
- Quiz .quiz.json fusionnés
- Images Cloudinary automatiques
- Idempotent (relançable sans doublons)

Usage :
    python -m scripts.import_curriculum_v2 --dry-run
    python -m scripts.import_curriculum_v2 --apply
    python -m scripts.import_curriculum_v2 --apply --publish
"""
from __future__ import annotations

import argparse
import json
import os
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

# ═══════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════

CLOUDINARY_BASE = "https://res.cloudinary.com/zvx1tzl3/image/upload"

# Dossiers ECHATS PRO (ton contenu)
ECHATS_PREFIXES = ("01-", "02-", "03-", "05-", "06-", "07-", "09-")

# Open Source : attribution par dossier
OPENSOURCE_ATTRIBUTION = {
    "datacarpentry": {
        "author": "Data Carpentry",
        "license": "CC-BY-4.0",
        "source_url": "https://datacarpentry.org/",
    },
    "git-novice": {
        "author": "Software Carpentry",
        "license": "CC-BY-4.0",
        "source_url": "https://swcarpentry.github.io/git-novice/",
    },
    "python-novice-inflammation": {
        "author": "Software Carpentry",
        "license": "CC-BY-4.0",
        "source_url": "https://swcarpentry.github.io/python-novice-inflammation/",
    },
    "shell-novice": {
        "author": "Software Carpentry",
        "license": "CC-BY-4.0",
        "source_url": "https://swcarpentry.github.io/shell-novice/",
    },
    "missing-semester": {
        "author": "MIT",
        "license": "CC-BY-NC-SA",
        "source_url": "https://missing.csail.mit.edu/",
    },
    "fullstack-hy2020": {
        "author": "University of Helsinki",
        "license": "CC-BY-NC-SA",
        "source_url": "https://fullstackopen.com/",
    },
    "_CYBER": {
        "author": "Communauté Cyber",
        "license": "MIT",
        "source_url": "https://github.com/SecurityTalent/Dojo-101",
    },
    "content": {
        "author": "ECHATS PRO",
        "license": "Tous droits réservés",
        "source_url": None,
    },
}

# Extensions
LESSON_EXTENSIONS = {".md"}
SKIP_FILENAMES = {
    "license", "license.md", "code_of_conduct.md", "contributing.md",
    "issue_template.md", "pull_request_template.md", "security.md",
    "changelog.md", "codeowners", ".gitattributes", ".gitignore",
    "readme.md", "index.md",
}

WORDS_PER_MINUTE = 200
MIN_WORDS = 30


class ImportInputError(RuntimeError):
    pass


# ═══════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════

def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return normalized or "item"


def humanize(name: str) -> str:
    name = re.sub(r"\.(md|txt)$", "", name, flags=re.IGNORECASE)
    name = name.replace("_", " ").replace("-", " ")
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)
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


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extrait le frontmatter YAML (sans dépendance pyyaml)."""
    if not content.startswith("---"):
        return {}, content

    lines = content.split("\n")
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, content

    end_idx = None
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}, content

    fm_text = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1:]).strip()

    # Parse simple (clé: valeur) sans pyyaml
    fm = {}
    current_key = None
    for line in fm_text.split("\n"):
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith("  - "):
            if current_key:
                fm.setdefault(current_key, []).append(line[4:].strip().strip('"'))
            continue
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if value == "":
                current_key = key
                fm[key] = []
            elif value.startswith("[") and value.endswith("]"):
                items = [x.strip().strip('"').strip("'") for x in value[1:-1].split(",") if x.strip()]
                fm[key] = items
                current_key = None
            else:
                # Essayer de parser en int/bool
                if value.lower() == "true":
                    fm[key] = True
                elif value.lower() == "false":
                    fm[key] = False
                elif value.isdigit():
                    fm[key] = int(value)
                else:
                    fm[key] = value
                current_key = None

    return fm, body


def replace_images_cloudinary(body: str) -> str:
    """Remplace ![](img/xxx.png) par l'URL Cloudinary."""
    def replacer(match):
        alt = match.group(1)
        img_path = match.group(2)
        img_name = img_path.split("/")[-1]
        new_url = f"{CLOUDINARY_BASE}/{img_name}"
        return f"![{alt}]({new_url})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replacer, body)


def build_attribution_header(info: dict) -> str:
    """Construit l'en-tête d'attribution pour les contenus open source."""
    lines = ["---", ""]
    if info.get("author"):
        lines.append(f"> 📖 **Source** : {info['author']}")
    if info.get("license"):
        lines.append(f"> 📜 **Licence** : {info['license']}")
    if info.get("source_url"):
        lines.append(f"> 🔗 **Original** : {info['source_url']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def parse_quiz(quiz_data: dict) -> dict:
    """Parse le format quiz .quiz.json → format interne."""
    questions = []
    for q in quiz_data.get("questions", []):
        question_text = q.get("question", "")
        q_type = q.get("type", "single_choice")
        options = q.get("options", [])
        correct_key = q.get("correct", "")
        explanation = q.get("explanation", "")

        if not question_text or not options:
            continue

        answers = []
        if isinstance(correct_key, str):
            correct_keys = [correct_key]
        elif isinstance(correct_key, list):
            correct_keys = correct_key
        else:
            correct_keys = []

        for opt in options:
            key = opt.get("key", "")
            text = opt.get("text", "")
            answers.append({
                "answer": text,
                "correct": key in correct_keys,
            })

        questions.append({
            "question": question_text,
            "type": q_type if q_type in ("single_choice", "multi_choice", "true_false") else "single_choice",
            "answers": answers,
            "explanation": explanation,
        })

    return {
        "title": quiz_data.get("title", "Quiz"),
        "passing_score": 70,
        "questions": questions,
    }


# ═══════════════════════════════════════════════════
# DATACLASSES
# ═══════════════════════════════════════════════════

@dataclass
class LessonPlan:
    module_slug: str
    module_title: str
    track_slug: str
    track_title: str
    lesson_title: str
    lesson_order: int
    content: str
    duration_minutes: int
    source_path: str
    quiz: dict | None = None
    is_echats: bool = True


@dataclass
class ImportPlan:
    lessons: list[LessonPlan] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    tracks: dict = field(default_factory=dict)


# ═══════════════════════════════════════════════════
# BUILD PLAN
# ═══════════════════════════════════════════════════

def build_plan(root: Path) -> ImportPlan:
    if not root.is_dir():
        raise ImportInputError(f"Dossier introuvable: {root}")

    plan = ImportPlan()
    lesson_orders: dict[str, int] = {}

    for dossier in sorted(p for p in root.iterdir() if p.is_dir()):
        name = dossier.name
        if name == "img":
            continue

        is_echats = any(name.startswith(p) for p in ECHATS_PREFIXES)
        is_opensource = name in OPENSOURCE_ATTRIBUTION

        if not is_echats and not is_opensource:
            plan.skipped.append(f"{name}: dossier non reconnu")
            continue

        # Déterminer track + module
        if is_echats:
            track_slug = "echats-cybersecurite"
            track_title = "Cybersécurité ECHATS PRO"
            module_title = humanize(name)
            module_slug = slugify(module_title)
        else:
            track_slug = "open-source-cybersecurity"
            track_title = "Ressources Open Source"
            attribution = OPENSOURCE_ATTRIBUTION[name]
            module_title = humanize(name)
            module_slug = slugify(module_title)

        # Parcourir les .md
        files = sorted(p for p in dossier.rglob("*") if p.is_file() and p.suffix.lower() in LESSON_EXTENSIONS)

        for file_path in files:
            if file_path.name.lower() in SKIP_FILENAMES:
                plan.skipped.append(f"{file_path.relative_to(root)}: boilerplate")
                continue

            try:
                text = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                plan.skipped.append(f"{file_path.relative_to(root)}: non-UTF-8")
                continue

            word_count = len(text.split())
            if word_count < MIN_WORDS:
                plan.skipped.append(f"{file_path.relative_to(root)}: trop court")
                continue

            # Parse frontmatter
            fm, body = parse_frontmatter(text)

            # Titre
            fallback_title = humanize(file_path.stem)
            lesson_title = fm.get("title") or extract_title(body, fallback_title)

            # Attribution
            if is_opensource:
                info = OPENSOURCE_ATTRIBUTION[name]
                header = build_attribution_header(info)
                content = header + body
            else:
                content = body

            # Images Cloudinary
            content = replace_images_cloudinary(content)

            # Quiz associé
            quiz_path = file_path.with_suffix(".quiz.json")
            quiz = None
            if quiz_path.exists():
                try:
                    quiz_raw = json.loads(quiz_path.read_text(encoding="utf-8"))
                    quiz = parse_quiz(quiz_raw)
                except Exception as e:
                    plan.skipped.append(f"{quiz_path.name}: quiz invalide ({e})")

            # Order
            order_key = f"{track_slug}/{module_slug}"
            lesson_order = lesson_orders.get(order_key, 0) + 1
            lesson_orders[order_key] = lesson_order

            plan.lessons.append(LessonPlan(
                module_slug=module_slug,
                module_title=module_title,
                track_slug=track_slug,
                track_title=track_title,
                lesson_title=lesson_title[:200],
                lesson_order=lesson_order,
                content=content,
                duration_minutes=max(5, word_count // WORDS_PER_MINUTE),
                source_path=str(file_path.relative_to(root)),
                quiz=quiz,
                is_echats=is_echats,
            ))

    return plan


# ═══════════════════════════════════════════════════
# DRY RUN
# ═══════════════════════════════════════════════════

def dry_run_payload(plan: ImportPlan) -> dict:
    by_track = {}
    for lesson in plan.lessons:
        by_track.setdefault(lesson.track_slug, {
            "title": lesson.track_title,
            "modules": {},
            "lessons": 0,
            "quizzes": 0,
        })
        t = by_track[lesson.track_slug]
        t["modules"].setdefault(lesson.module_title, 0)
        t["modules"][lesson.module_title] += 1
        t["lessons"] += 1
        if lesson.quiz:
            t["quizzes"] += 1

    return {
        "mode": "dry-run",
        "writes_performed": False,
        "totals": {
            "tracks": len(by_track),
            "modules": sum(len(t["modules"]) for t in by_track.values()),
            "lessons": len(plan.lessons),
            "quizzes": sum(t["quizzes"] for t in by_track.values()),
            "skipped": len(plan.skipped),
        },
        "tracks": {
            slug: {
                "title": t["title"],
                "modules": t["modules"],
                "lessons": t["lessons"],
            }
            for slug, t in by_track.items()
        },
        "skipped_sample": plan.skipped[:20],
    }


# ═══════════════════════════════════════════════════
# APPLY
# ═══════════════════════════════════════════════════

def apply_plan(plan: ImportPlan, publish: bool) -> dict:
    from sqlalchemy import select
    from app.core.database import SessionLocal
    from app.models.course_module import CourseModule
    from app.models.lesson import Lesson
    from app.models.quiz import Answer, Question, Quiz
    from app.models.track import Track

    db = SessionLocal()
    created = {"tracks": 0, "modules": 0, "lessons": 0, "quizzes": 0, "questions": 0, "answers": 0}
    reused = {"tracks": 0, "modules": 0, "lessons": 0, "quizzes": 0}

    try:
        with db.begin():
            track_cache = {}
            module_cache = {}
            lesson_cache = {}

            # Créer les tracks
            for slug, title in [("echats-cybersecurite", "Cybersécurité ECHATS PRO"),
                                 ("open-source-cybersecurity", "Ressources Open Source")]:
                track = db.execute(select(Track).where(Track.slug == slug)).scalar_one_or_none()
                if track is None:
                    track = Track(
                        title=title,
                        slug=slug,
                        description=f"Contenu pédagogique — {title}",
                        difficulty="intermediate",
                        domain="cybersecurity",
                        published=publish,
                    )
                    db.add(track)
                    db.flush()
                    created["tracks"] += 1
                else:
                    reused["tracks"] += 1
                track_cache[slug] = track

            # Créer les modules
            for lesson in plan.lessons:
                module_key = (lesson.track_slug, lesson.module_slug)
                if module_key in module_cache:
                    continue
                track = track_cache[lesson.track_slug]
                module = db.execute(
                    select(CourseModule).where(
                        CourseModule.track_id == track.id,
                        CourseModule.title == lesson.module_title,
                    )
                ).scalar_one_or_none()
                if module is None:
                    module = CourseModule(
                        track_id=track.id,
                        title=lesson.module_title,
                        description=f"Module {lesson.module_title}",
                        order=len([m for m in module_cache if m[0] == lesson.track_slug]) + 1,
                        published=publish,
                    )
                    db.add(module)
                    db.flush()
                    created["modules"] += 1
                else:
                    reused["modules"] += 1
                module_cache[module_key] = module

            # Créer les leçons + quiz
            for lesson in plan.lessons:
                module = module_cache[(lesson.track_slug, lesson.module_slug)]
                existing = db.execute(
                    select(Lesson).where(
                        Lesson.module_id == module.id,
                        Lesson.title == lesson.lesson_title,
                    )
                ).scalar_one_or_none()

                if existing is not None:
                    reused["lessons"] += 1
                    continue

                new_lesson = Lesson(
                    module_id=module.id,
                    title=lesson.lesson_title,
                    content=lesson.content,
                    duration_minutes=lesson.duration_minutes,
                    order=lesson.lesson_order,
                    published=publish,
                )
                db.add(new_lesson)
                db.flush()
                created["lessons"] += 1

                # Quiz
                if lesson.quiz and lesson.quiz.get("questions"):
                    quiz = Quiz(
                        lesson_id=new_lesson.id,
                        title=lesson.quiz["title"],
                        passing_score=lesson.quiz.get("passing_score", 70),
                    )
                    for q_data in lesson.quiz["questions"]:
                        question = Question(
                            question=q_data["question"][:1000],
                            type=q_data["type"],
                        )
                        for a_data in q_data["answers"]:
                            question.answers.append(Answer(
                                answer=a_data["answer"][:500],
                                correct=a_data["correct"],
                            ))
                            created["answers"] += 1
                        quiz.questions.append(question)
                        created["questions"] += 1
                    db.add(quiz)
                    db.flush()
                    created["quizzes"] += 1

        return {
            "mode": "apply",
            "writes_performed": True,
            "created": created,
            "reused": reused,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ═══════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--publish", action="store_true")
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
        print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"status": "failed", "error_type": type(exc).__name__, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
