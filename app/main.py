def build_cors_list():
    """
    Monta dinamicamente a lista de origens permitidas.
    Suporta:
    - URL principal do FRONTEND (produção)
    - URL adicional (preview do Vercel)
    - versões com/sem www
    - versões http/https
    """

    origins = set()

    # ================================
    # ORIGEM PRINCIPAL DO FRONTEND
    # ================================
    if settings.FRONTEND_URL:
        origins.add(settings.FRONTEND_URL.strip())

    # ================================
    # ORIGEM ADICIONAL (PREVIEW VERCEL)
    # ================================
    if hasattr(settings, "CORS_ADDITIONAL_ORIGIN") and settings.CORS_ADDITIONAL_ORIGIN:
        origins.add(settings.CORS_ADDITIONAL_ORIGIN.strip())

    # ================================
    # Gerar variações com/sem www e http/https
    # ================================
    generated = set()

    for origin in origins:
        if origin.startswith("https://"):
            generated.add(origin.replace("https://", "http://"))
        if origin.startswith("http://"):
            generated.add(origin.replace("http://", "https://"))

        # adicionar versão www
        if "://www." not in origin:
            generated.add(origin.replace("://", "://www."))
        # versão sem www
        if "://www." in origin:
            generated.add(origin.replace("://www.", "://"))

    origins = origins.union(generated)

    # ================================
    # URLs usadas em desenvolvimento
    # ================================
    dev_allowed = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    origins.update(dev_allowed)

    # ================================
    # Ambiente de dev pode permitir tudo
    # ================================
    if settings.ENVIRONMENT == "development":
        origins.add("*")

    return list(origins)
