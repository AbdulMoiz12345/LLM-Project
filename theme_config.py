# theme_config.py
# ─────────────────────────────────────────────────────────────────────────────
# Centralized theme configuration.
# Switch between "light" (Curated Manuscript) and "dark" (Nocturnal Architect)
# by changing a single value or toggling via session state.
# ─────────────────────────────────────────────────────────────────────────────

THEMES = {
    "light": {
        # ── Identity ──────────────────────────────────────────────────────────
        "name": "Curated Manuscript",
        "label": "🌙 Dark Mode",

        # ── Surface hierarchy ─────────────────────────────────────────────────
        "surface":                  "#fcf9f0",
        "surface_container_low":    "#f6f3ea",
        "surface_container":        "#e9e5da",
        "surface_container_high":   "#e2ddd2",
        "surface_container_highest":"#dbd6cb",
        "surface_bright":           "#ffffff",

        # ── Brand / accent ────────────────────────────────────────────────────
        "primary":                  "#9c4321",
        "primary_container":        "#e37953",
        "secondary":                "#b08800",
        "secondary_container":      "#ffdf9f",
        "secondary_fixed":          "#ffdf9f",

        # ── Text ──────────────────────────────────────────────────────────────
        "on_surface":               "#1c1c17",
        "on_surface_variant":       "#5c5a52",
        "on_primary":               "#ffffff",

        # ── Utility ───────────────────────────────────────────────────────────
        "outline_variant":          "#b8b4a8",
        "error":                    "#b91c1c",
        "error_container":          "#fee2e2",

        # ── Typography ────────────────────────────────────────────────────────
        "font_display":   "'Noto Serif', Georgia, serif",
        "font_body":      "'Newsreader', 'Georgia', serif",
        "font_label":     "'Work Sans', sans-serif",

        # ── Shadow & glass ────────────────────────────────────────────────────
        "shadow_float":   "0 20px 40px rgba(28,28,23,0.08)",
        "backdrop_blur":  "20px",
        "glass_opacity":  "0.80",

        # ── Misc ──────────────────────────────────────────────────────────────
        "border_radius_btn":  "0.375rem",
        "border_radius_card": "0.5rem",
        "input_focus_color":  "#b08800",
    },

    "dark": {
        # ── Identity ──────────────────────────────────────────────────────────
        "name": "Nocturnal Architect",
        "label": "☀️ Light Mode",

        # ── Surface hierarchy ─────────────────────────────────────────────────
        "surface":                  "#060e1d",
        "surface_container_low":    "#0a1324",
        "surface_container":        "#0f192c",
        "surface_container_high":   "#14203a",
        "surface_container_highest":"#1a263c",
        "surface_bright":           "#1f2c44",

        # ── Brand / accent ────────────────────────────────────────────────────
        "primary":                  "#45a6b8",
        "primary_container":        "#007683",
        "secondary":                "#b8d1ff",
        "secondary_container":      "#1f477b",
        "secondary_fixed":          "#1f477b",

        # ── Text (FIXED FOR VISIBILITY) ───────────────────────────────────────
        "on_surface":               "#f3f6ff",   # brighter main text
        "on_surface_variant":       "#c7d2f3",   # much clearer secondary text
        "on_primary":               "#060e1d",

        # ── Utility ───────────────────────────────────────────────────────────
        "outline_variant":          "#5a6478",
        "error":                    "#ff716c",
        "error_container":          "#9f0519",

        # ── Typography ────────────────────────────────────────────────────────
        "font_display":   "'Space Grotesk', 'Helvetica Neue', sans-serif",
        "font_body":      "'Inter', system-ui, sans-serif",
        "font_label":     "'Space Grotesk', sans-serif",

        # ── Shadow & glass ────────────────────────────────────────────────────
        "shadow_float":   "0 20px 40px rgba(0,0,0,0.40)",
        "backdrop_blur":  "20px",
        "glass_opacity":  "0.80",

        # ── Misc ──────────────────────────────────────────────────────────────
        "border_radius_btn":  "0.375rem",
        "border_radius_card": "0.75rem",
        "input_focus_color":  "#81ecff",
    },
}


def get_theme(dark_mode: bool) -> dict:
    """Return the active theme dict."""
    return THEMES["dark"] if dark_mode else THEMES["light"]