"""Headers de sécurité HTTP : HSTS, CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy."""
SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    "Content-Security-Policy": (
        "default-src 'self'; img-src 'self' https://res.cloudinary.com data:; "
        "script-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'"
    ),
}
