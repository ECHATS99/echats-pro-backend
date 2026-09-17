"""Crée ou promeut un compte en super_admin en ligne de commande.

Usage : python -m scripts.create_admin --email admin@echatspro.com

L'utilisateur doit déjà s'être connecté au moins une fois via Firebase (pour exister en
base avec un firebase_uid) : ce script se contente d'ajouter le rôle super_admin.
"""
import argparse
import sys

from app.core.database import SessionLocal
from app.core.constants import RoleName
from app.models.role_permission import Role
from app.models.user import User


def promote_to_super_admin(email: str) -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).one_or_none()
        if user is None:
            print(f"Aucun utilisateur trouvé avec l'email {email}. "
                  f"Il doit d'abord se connecter une fois via Firebase.", file=sys.stderr)
            sys.exit(1)

        role = db.query(Role).filter(Role.name == RoleName.SUPER_ADMIN.value).one_or_none()
        if role is None:
            print("Le rôle 'super_admin' n'existe pas encore — exécutez d'abord scripts/seed.py",
                  file=sys.stderr)
            sys.exit(1)

        if role not in user.roles:
            user.roles.append(role)
            db.commit()
            print(f"{email} est maintenant super_admin. Pensez à activer le 2FA (obligatoire).")
        else:
            print(f"{email} est déjà super_admin.")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--email", required=True, help="Email du compte à promouvoir")
    args = parser.parse_args()
    promote_to_super_admin(args.email)
