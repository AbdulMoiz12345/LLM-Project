def build_google_fonts_url(dark_mode: bool) -> str:
    if dark_mode:
        return (
            "https://fonts.googleapis.com/css2?"
            "family=Space+Grotesk:wght@300;400;500;600;700&"
            "family=Inter:wght@300;400;500&display=swap"
        )
    return (
        "https://fonts.googleapis.com/css2?"
        "family=Noto+Serif:wght@400;600;700&"
        "family=Newsreader:wght@400;500&"
        "family=Work+Sans:wght@300;400;500;600&display=swap"
    )


def build_css(t: dict, dark_mode: bool) -> str:

    cta_gradient = f"linear-gradient(135deg, {t['primary']}, {t['primary_container']})"
    ghost_border = f"1px solid {t['outline_variant']}29"

    return f"""
    <style>
    @import url('{build_google_fonts_url(dark_mode)}');

    :root {{
        --surface: {t['surface']};
        --surface-low: {t['surface_container_low']};
        --surface-mid: {t['surface_container']};
        --surface-high: {t['surface_container_high']};
        --surface-highest: {t['surface_container_highest']};

        --primary: {t['primary']};
        --primary-container: {t['primary_container']};

        --secondary: {t['secondary']};
        --secondary-container: {t['secondary_container']};

        --on-surface: {t['on_surface']};
        --on-surface-variant: {t['on_surface_variant']};
        --on-primary: {t['on_primary']};

        --outline-variant: {t['outline_variant']};

        --font-body: {t['font_body']};
        --font-label: {t['font_label']};

        --radius-card: {t['border_radius_card']};

        --cta-gradient: {cta_gradient};
        --ghost-border: {ghost_border};
    }}

    /* ───────── BASE ───────── */
    html, body, .stApp {{
        background-color: var(--surface, #ffffff) !important;
        color: var(--on-surface, #000000) !important;
        font-family: var(--font-body);
    }}

    #MainMenu, footer, header {{
        visibility: hidden;
    }}

    /* ───────── SIDEBAR ───────── */
    [data-testid="stSidebar"] {{
        background-color: var(--surface-low, #f5f5f5) !important;
    }}

    [data-testid="stSidebar"] button {{
        background-color: var(--surface-mid, #eeeeee) !important;
        color: var(--on-surface, #000000) !important;
        border: var(--ghost-border) !important;
        border-radius: var(--radius-card) !important;
        font-family: var(--font-label) !important;
        text-transform: uppercase;
    }}

    [data-testid="stSidebar"] button:hover {{
        background-color: var(--surface-high, #dddddd) !important;
        color: var(--primary) !important;
    }}

    /* ───────── PRIMARY BUTTON ───────── */
    .update-btn button {{
        background: var(--cta-gradient) !important;
        color: var(--on-primary) !important;
        border: none !important;
    }}

    /* ───────── CHAT INPUT (FIXED SINGLE BACKGROUND) ───────── */

    div[data-testid="stChatInput"] {{
        background-color: var(--surface-mid, #eeeeee) !important;
        border: 2px solid var(--outline-variant, #999999) !important;
        border-radius: var(--radius-card) !important;
    }}

    /* Remove all inner backgrounds */
    div[data-testid="stChatInput"] div {{
        background-color: transparent !important;
    }}

    div[data-baseweb="textarea"],
    div[data-baseweb="base-input"] {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    div[data-testid="stChatInput"] textarea {{
        background-color: transparent !important;
        color: var(--on-surface, #000000) !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }}

    div[data-testid="stChatInput"] textarea:focus {{
        background-color: transparent !important;
        outline: none !important;
        box-shadow: none !important;
    }}

    /* Send button */
    div[data-testid="stChatInput"] button {{
        background: var(--cta-gradient) !important;
        color: var(--on-primary) !important;
        border: none !important;
    }}

    /* ───────── FILE UPLOADER (FIXED SINGLE STYLE) ───────── */

    [data-testid="stFileUploader"] {{
        background-color: var(--surface-mid, #eeeeee) !important;
        border: var(--ghost-border) !important;
        border-radius: var(--radius-card) !important;
    }}

    [data-testid="stFileUploader"] > div,
    [data-testid="stFileUploaderDropzone"] {{
        background-color: var(--surface-mid, #eeeeee) !important;
        border: none !important;
    }}

    [data-testid="stFileUploader"] button {{
        background: var(--cta-gradient) !important;
        color: var(--on-primary) !important;
        border: none !important;
        border-radius: var(--radius-card) !important;
    }}

    [data-testid="stFileUploader"] button:hover {{
        background: var(--cta-gradient) !important;
        filter: brightness(1.05);
        color: var(--on-primary) !important;
    }}

    /* Prevent nested hover layers */
    [data-testid="stFileUploader"] * {{
        background-color: inherit !important;
    }}

    /* ───────── REMOVE WHITE CONTAINERS ───────── */

    .stApp,
    .main,
    .block-container {{
        background-color: var(--surface, #ffffff) !important;
    }}

    section[data-testid="stMain"] > div {{
        background-color: var(--surface, #ffffff) !important;
    }}

    div[data-testid="stVerticalBlock"],
    div[data-testid="stVerticalBlock"] > div {{
        background-color: transparent !important;
    }}

    /* ───────── FIX BOTTOM CHAT CONTAINER ───────── */

    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stBottomBlockContainer"] > div,
    div[data-testid="stBottomBlockContainer"] div {{
        background-color: var(--surface, #ffffff) !important;
    }}

    </style>
    """