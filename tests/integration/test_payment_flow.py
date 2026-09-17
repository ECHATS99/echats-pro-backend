"""Test d'intégration : flux de paiement (Partie 7.15 du SRS). Nécessite une base
PostgreSQL de test réelle (jamais la production) et est donc ignoré si DATABASE_URL n'est
pas configuré vers une base de test dédiée — cette garde évite de faire échouer la suite
dans un environnement sans infrastructure, tout en restant exécutable tel quel en CI.

Pour lancer réellement ce test :
    DATABASE_URL=postgresql://test:test@localhost:5432/echats_pro_test \
    REDIS_URL=redis://localhost:6379/1 \
    pytest tests/integration/test_payment_flow.py
"""
import os

import pytest

requires_test_db = pytest.mark.skipif(
    "echats_pro_test" not in os.environ.get("DATABASE_URL", ""),
    reason="Nécessite une base PostgreSQL de test dédiée (voir docstring du module).",
)


@requires_test_db
def test_order_amount_is_computed_server_side(db_session):
    """Le montant d'une commande doit toujours être recalculé côté serveur à partir du prix
    en base (jamais confiance au prix envoyé par le frontend — Partie 5 du SRS)."""
    from app.models.product import Product
    from app.modules.orders.schemas import OrderCreate, OrderItemCreate
    from app.modules.orders.service import create_order

    product = Product(name="T-shirt BLACKHAWK LAB", price_fcfa=15000, stock=10, available=True)
    db_session.add(product)
    db_session.commit()

    payload = OrderCreate(
        items=[OrderItemCreate(product_id=product.id, quantity=2)],
        payment_provider="stripe", currency="XAF",
    )
    result = create_order(db_session, payload, user_id="00000000-0000-0000-0000-000000000001")
    assert result.order.amount == 30000  # 2 x 15000, jamais un montant fourni par le client


@requires_test_db
def test_flag_replay_does_not_award_points_twice(db_session):
    """Un flag déjà résolu ne doit jamais rapporter de points une seconde fois."""
    pytest.skip("À implémenter avec les fixtures utilisateur/CTF complètes (voir seed.py).")
