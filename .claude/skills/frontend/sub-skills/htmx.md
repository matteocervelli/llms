# HTMX — Server-Driven UI Patterns

## Core Concept

HTMX extends HTML with `hx-*` attributes for server-driven interactivity. The server returns HTML fragments, not JSON. Combined with Jinja2 templates for server rendering and hyperscript for client-side logic.

## Key Attributes

| Attribute      | Purpose                  | Example                      |
| -------------- | ------------------------ | ---------------------------- |
| `hx-get`       | GET request on trigger   | `hx-get="/api/items"`        |
| `hx-post`      | POST with form data      | `hx-post="/api/items"`       |
| `hx-put`       | Full update              | `hx-put="/api/items/1"`      |
| `hx-patch`     | Partial update           | `hx-patch="/api/items/1"`    |
| `hx-delete`    | Delete resource          | `hx-delete="/api/items/1"`   |
| `hx-trigger`   | Event to trigger request | `hx-trigger="click"`         |
| `hx-target`    | Where to put response    | `hx-target="#results"`       |
| `hx-swap`      | How to insert response   | `hx-swap="innerHTML"`        |
| `hx-indicator` | Loading indicator        | `hx-indicator="#spinner"`    |
| `hx-confirm`   | Confirmation dialog      | `hx-confirm="Are you sure?"` |

## Swap Strategies

```
innerHTML    — Replace inner content (default)
outerHTML    — Replace entire element
afterbegin   — Insert before first child
beforeend    — Insert after last child
afterend     — Insert after element
beforebegin  — Insert before element
delete       — Remove target
none         — No swap (fire-and-forget)
```

## Common Patterns

### Inline Editing

```html
<div hx-get="/edit/{{ item.id }}" hx-trigger="dblclick" hx-swap="outerHTML">
  {{ item.name }}
</div>
```

Server returns edit form; form submits via `hx-put`, returns view template.

### Infinite Scroll

```html
<div
  hx-get="/items?page={{ next_page }}"
  hx-trigger="revealed"
  hx-swap="afterend"
>
  Loading more...
</div>
```

### Active Search

```html
<input
  type="search"
  name="q"
  hx-get="/search"
  hx-trigger="input changed delay:300ms"
  hx-target="#results"
  hx-indicator="#search-spinner"
/>
```

### Form Validation (Server-Side)

```html
<input
  name="email"
  hx-post="/validate/email"
  hx-trigger="blur"
  hx-target="next .error"
  hx-swap="innerHTML"
/>
<span class="error"></span>
```

### Bulk Operations

```html
<form hx-post="/bulk-action" hx-target="#table-body">
  <input type="checkbox" name="ids" value="{{ item.id }}" />
  <button hx-vals='{"action": "delete"}'>Delete Selected</button>
</form>
```

## HTMX + Jinja2 Integration

### Partial Templates

```python
# FastAPI route returning partial HTML
@app.get("/items", response_class=HTMLResponse)
async def list_items(request: Request):
    items = await get_items()
    # Return full page or partial based on HTMX header
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("partials/item-list.html", {"items": items})
    return templates.TemplateResponse("pages/items.html", {"items": items})
```

### Template Structure

```
templates/
├── base.html              # Full page layout
├── pages/
│   └── items.html         # Full page (extends base)
├── partials/
│   ├── item-list.html     # Table body fragment
│   ├── item-row.html      # Single row fragment
│   └── item-form.html     # Edit form fragment
└── components/
    ├── pagination.html    # Reusable pagination
    └── toast.html         # Notification toast
```

## HTMX + hyperscript

For client-side logic that doesn't need a server round-trip:

```html
<button _="on click toggle .hidden on #menu">Toggle Menu</button>
<div
  _="on htmx:afterSwap add .fade-in to me then wait 300ms then remove .fade-in"
></div>
```

## Design Dimension Integration

- **Typography**: Server-rendered — no FOUT issues, fonts load with page
- **Color**: CSS custom properties for theming, toggled via hyperscript
- **Motion**: CSS transitions on swap (`hx-swap="innerHTML transition:true"`)
- **Spatial**: Server controls layout, HTMX swaps content within containers
- **Backgrounds**: Static assets, no client-side rendering needed

## Anti-Patterns

- Don't use HTMX for purely client-side interactions (use hyperscript)
- Don't return JSON from HTMX endpoints (return HTML fragments)
- Don't nest `hx-*` targets inside other `hx-*` targets without care
- Don't forget `hx-indicator` for slow operations
- Don't use `hx-boost` on forms that upload files (use standard form submission)
