# Jinja2 — Template Patterns for Server-Rendered UI

## Core Concept

Jinja2 templates render HTML server-side. Combined with HTMX, they power a server-driven UI where the server returns HTML fragments. Templates use inheritance, macros, and includes for DRY composition.

## Template Inheritance

```html
{# base.html — master layout #}
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>{% block title %}App{% endblock %}</title>
    {% block head %}{% endblock %}
  </head>
  <body>
    {% include "partials/nav.html" %}
    <main>{% block content %}{% endblock %}</main>
    {% include "partials/footer.html" %} {% block scripts %}{% endblock %}
  </body>
</html>

{# pages/dashboard.html — extends base #} {% extends "base.html" %} {% block
title %}Dashboard{% endblock %} {% block content %}
<h1>Dashboard</h1>
{% include "partials/metrics.html" %} {% endblock %}
```

## Macros (Reusable Components)

```html
{# macros/forms.html #} {% macro input(name, label, type="text", required=true,
value="") %}
<div class="form-group">
  <label for="{{ name }}">{{ label }}</label>
  <input
    type="{{ type }}"
    id="{{ name }}"
    name="{{ name }}"
    value="{{ value }}"
    {%
    if
    required
    %}required{%
    endif
    %}
    class="form-input"
  />
</div>
{% endmacro %} {% macro select(name, label, options, selected="") %}
<div class="form-group">
  <label for="{{ name }}">{{ label }}</label>
  <select id="{{ name }}" name="{{ name }}" class="form-select">
    {% for value, text in options %}
    <option
      value="{{ value }}"
      {%
      if
      value=""
      ="selected"
      %}selected{%
      endif
      %}
    >
      {{ text }}
    </option>
    {% endfor %}
  </select>
</div>
{% endmacro %} {# Usage #} {% from "macros/forms.html" import input, select %}
{{ input("email", "Email Address", type="email") }} {{ select("role", "Role",
[("admin", "Admin"), ("user", "User")]) }}
```

## Partial Templates for HTMX

```html
{# partials/item-row.html — single table row (HTMX fragment) #}
<tr id="item-{{ item.id }}">
  <td>{{ item.name }}</td>
  <td>{{ item.status }}</td>
  <td>
    <button
      hx-get="/items/{{ item.id }}/edit"
      hx-target="#item-{{ item.id }}"
      hx-swap="outerHTML"
    >
      Edit
    </button>
    <button
      hx-delete="/items/{{ item.id }}"
      hx-target="#item-{{ item.id }}"
      hx-swap="outerHTML swap:1s"
      hx-confirm="Delete {{ item.name }}?"
    >
      Delete
    </button>
  </td>
</tr>
```

## Filters and Formatting

```html
{{ amount | format_currency }} {# Custom filter #} {{ date |
strftime("%Y-%m-%d") }} {# Date formatting #} {{ description | truncate(100) }}
{# Text truncation #} {{ content | markdown }} {# Markdown rendering #} {{ items
| length }} {# Count #} {{ name | title }} {# Capitalize words #}
```

## FastAPI Integration

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Register custom filters
templates.env.filters["format_currency"] = lambda v: f"€{v:,.2f}"

@app.get("/items", response_class=HTMLResponse)
async def list_items(request: Request):
    items = await get_items()
    template = "partials/item-list.html" if request.headers.get("HX-Request") else "pages/items.html"
    return templates.TemplateResponse(template, {"request": request, "items": items})
```

## Template Organization

```
templates/
├── base.html              # Master layout (nav, footer, scripts)
├── macros/
│   ├── forms.html         # Form field macros
│   ├── tables.html        # Table/pagination macros
│   └── ui.html            # UI component macros (cards, badges, alerts)
├── pages/
│   ├── dashboard.html     # Full pages (extend base.html)
│   ├── items.html
│   └── settings.html
├── partials/
│   ├── nav.html           # Navigation bar
│   ├── footer.html        # Footer
│   ├── item-list.html     # HTMX fragments
│   ├── item-row.html
│   └── item-form.html
└── emails/                # Email templates (if needed)
```

## Best Practices

- **Partials for HTMX**: Every HTMX endpoint returns a partial template
- **Macros for DRY**: Reusable form fields, table rows, UI components
- **Inheritance for layout**: `base.html` → `pages/*.html` → `partials/*.html`
- **Context processors**: Inject common data (user, nav items) globally
- **Escape by default**: Jinja2 auto-escapes — use `|safe` only when you control the content
- **Keep logic minimal**: Complex logic belongs in Python, not templates
