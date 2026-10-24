#!/usr/bin/env python3
"""Assemble the static pages from components/ and src/.

Run:  python3 build.py
The generated .html files in the repo root are committed, so the site
works without any build step; this script just keeps shared markup
(header, sidebar, footer, dialogs) in one place.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
read = lambda p: (ROOT / p).read_text(encoding="utf-8")

PAGES = {
    "index": {
        "title": "Dashboard overview - Northwind Admin",
        "scripts": [],
        "dialogs": [],
        "sidebar": [("#metrics", "Key metrics"), ("#orders", "Latest orders"), ("#activity", "Recent activity")],
    },
    "users": {
        "title": "Users - Northwind Admin",
        "scripts": ["modal", "form-validation"],
        "dialogs": ["dialog-add-user", "dialog-confirm-delete"],
        "sidebar": [("#user-tools", "Search and actions"), ("#user-table", "User list"), ("#pagination", "Pagination")],
    },
    "settings": {
        "title": "Account settings - Northwind Admin",
        "scripts": ["form-validation", "char-count"],
        "dialogs": [],
        "sidebar": [("#profile", "Profile"), ("#security", "Security"), ("#notifications", "Notifications"), ("#about", "About you")],
    },
    "accessibility": {
        "title": "Accessibility statement - Northwind Admin",
        "scripts": [],
        "dialogs": [],
        "sidebar": [("#standards", "Standards followed"), ("#features", "Built-in features"), ("#feedback", "Report a problem")],
    },
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
{header}
{sidebar}
  <main id="main-content" class="main-content" tabindex="-1">
{main}
  </main>
{footer}
{scripts}</body>
</html>
"""

def indent(text, n=2):
    pad = " " * n
    return "\n".join(pad + line if line.strip() else line for line in text.rstrip().splitlines())

for key, cfg in PAGES.items():
    header = read("components/header.html")
    header = re.sub(r"\{\{cur:(\w+)\}\}",
                    lambda m: ' aria-current="page"' if m.group(1) == key else "", header)
    links = "\n".join(f'      <li><a href="{h}">{t}</a></li>' for h, t in cfg["sidebar"])
    sidebar = read("components/sidebar.html").replace("{{sidebar_links}}", links)
    main = read(f"src/{key}.main.html")
    dialogs = "\n".join(indent(read(f"components/{d}.html"), 4) for d in cfg["dialogs"])
    main = main.replace("    <!--DIALOGS-->", dialogs)
    scripts = "".join(f'  <script src="js/components/{s}.js" defer></script>\n' for s in cfg["scripts"] + ["theme-toggle"])
    html = TEMPLATE.format(
        title=cfg["title"],
        header=indent(header),
        sidebar=indent(sidebar),
        main=main.rstrip(),
        footer=indent(read("components/footer.html")),
        scripts=scripts,
    )
    (ROOT / f"{key}.html").write_text(html, encoding="utf-8")
    print("built", f"{key}.html")
