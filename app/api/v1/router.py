"""Assemble tous les routers de domaine sous /api/v1. Point d'entrée unique référencé
par app/main.py.
"""
from fastapi import APIRouter

from app.api.v1 import (
    admin, analytics, auth, badges, certificates, classroom, course_modules, ctf,
    exercises, forum, health, ia, labs, leaderboard, lessons, media, mentoring, news,
    notifications, orders, organizations, paraben, payments, products, quizzes, search,
    subscriptions, tracks, users, writeups,
)

api_router = APIRouter()

# Publiques / santé
api_router.include_router(health.router)
api_router.include_router(auth.router)

# Cœur utilisateur
api_router.include_router(users.router)
api_router.include_router(notifications.router)
api_router.include_router(subscriptions.router)

# Contenu pédagogique
api_router.include_router(tracks.router)
api_router.include_router(course_modules.router)
api_router.include_router(lessons.router)
api_router.include_router(quizzes.router)
api_router.include_router(exercises.router)

# CTF & Labs
api_router.include_router(ctf.router)
api_router.include_router(labs.router)

# Classroom & Mentorat
api_router.include_router(classroom.router)
api_router.include_router(mentoring.router)

# Gamification
api_router.include_router(badges.router)
api_router.include_router(certificates.router)
api_router.include_router(leaderboard.router)

# Communauté
api_router.include_router(writeups.router)
api_router.include_router(forum.router)

# Commerce
api_router.include_router(products.router)
api_router.include_router(orders.router)
api_router.include_router(payments.router)

# Contenu & recherche
api_router.include_router(news.router)
api_router.include_router(search.router)
api_router.include_router(media.router)

# IA (proxy sécurisé vers api.echats.ai)
api_router.include_router(ia.router)

# Paraben / Chambre Close / Institutions
api_router.include_router(paraben.router)
api_router.include_router(organizations.router)

# Administration
api_router.include_router(analytics.router)
api_router.include_router(admin.router)
