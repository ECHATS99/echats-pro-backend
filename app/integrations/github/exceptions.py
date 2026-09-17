"""Exceptions spécifiques au fournisseur github."""


class GitHubCodespacesError(Exception):
    """Levée en cas d'échec de création/destruction d'une session Codespaces."""
