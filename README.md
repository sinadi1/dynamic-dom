# Semantic HTML5 & Accessible Component Architecture

A four-page enterprise dashboard foundation built with strict HTML5 semantics
and WCAG 2.1 AA practices. No framework, no build dependency: open
`index.html` in a browser.

**W3C validation:** all pages and both stylesheets pass the official Nu HTML
Checker with **0 errors and 0 warnings** (`npm run validate`).

## Pages

| Page | Demonstrates |
|---|---|
| `index.html` | Landmarks, KPI `<article>` cards, data table, activity feed, `<aside>` |
| `products.html` | **Store**: live REST API client (search, categories, sorting, cart, skeletons, error banners) |
| `users.html` | Searchable data table, row actions, modal dialogs (form + alert dialog) |
| `settings.html` | Full form: fieldsets, labels, hints, validation, radios, checkboxes, select/optgroup, textarea counter |
| `accessibility.html` | Article with sectioned headings |

## Structure

```
├── index.html, users.html, settings.html, accessibility.html   (generated, committed)
├── components/        reusable markup partials
│   ├── header.html, sidebar.html, footer.html
│   ├── dialog-add-user.html, dialog-confirm-delete.html
├── src/               page-specific <main> content
├── css/style.css      design tokens + mobile-first layout + components
├── js/                ES modules for the Store page
│   ├── app.js         entry point: wires everything together
│   ├── api.js         REST client (async/await, timeout, ApiError, cache)
│   ├── state.js       localStorage store: cart + preferences
│   ├── filters.js     pure search / category / sort functions
│   └── ui.js          DOM rendering (skeletons, banners, grid, cart)
├── js/components/     modal.js, form-validation.js, char-count.js, theme-toggle.js
├── build.py           stitches components + src into the final pages
└── docs/screenshots/
```

Shared markup lives once in `components/`; `python3 build.py` regenerates the
pages. The generated HTML is committed so the site works with no build step.

## Semantics and accessibility checklist

- **Landmarks:** `header`, `nav` (Primary, Breadcrumb, Sidebar, Footer, Pagination), `aside`, one `main`, `footer`; each repeated landmark has a unique `aria-label`.
- **Headings:** one `h1` per page, no skipped levels; every `section`/`article` has a heading.
- **Skip link** to `#main-content`; `aria-current="page"` on current nav item and breadcrumb.
- **Tables:** `caption`, `scope="col"`/`scope="row"`, action buttons carry visually hidden row names ("Edit Priya Shah").
- **Dialogs:** native `<dialog>` + `showModal()` (focus trap, Esc, inert background); focus returns to the opener; destructive dialog uses `role="alertdialog"` with focus on Cancel.
- **Forms:** every control has a `<label>`; related controls grouped in `fieldset`/`legend`; hints and errors linked with `aria-describedby`; `required`, `pattern`, `minlength`, `min`/`max`, `type`, and `autocomplete` tokens; errors set `aria-invalid`, focus moves to the first invalid field, a `role="status"` region announces the summary.
- **Visual:** visible focus ring, AA colour contrast, reduced-motion support, responsive layout.

## Run and validate

```bash
npm start              # http://localhost:8080
npm install && npm run validate   # needs Java; runs the W3C Nu validator
```

## Design note

Validation runs on submit rather than on blur. Showing an error on blur
shifts the layout mid-click and can swallow the Submit click, and it is
noisier for screen reader users.

## Responsive design tokens & mobile-first CSS (`css/style.css`)

One stylesheet, organised as: tokens, base, layout, components, utilities.

- **Design tokens in `:root`:** brand colours, a fluid type scale (`clamp()`), spacing scale (`--space-1` to `--space-6`), radii, shadows, blur and transition tokens.
- **Mobile-first breakpoints** (`min-width`): base = 320px (single column, sidebar becomes a row of pills), **768px** (2-column cards, 2-column forms), **1024px** (sidebar column, 4-column cards, 2fr/1fr content), **1440px** (wider sidebar, 3-column forms, capped content width).
- **Modern styling:** glassmorphism (`backdrop-filter` blur on header, sidebar, cards, tables, fieldsets), soft shadows, hover transitions (cards lift, buttons, rows, links) that switch off under `prefers-reduced-motion`.
- **Light/dark themes** through CSS variables: follows the OS setting by default, and the header toggle overrides and remembers the choice (`data-theme` on `<html>`, saved in `localStorage`).
- **No horizontal page scroll:** grids use `minmax(0, 1fr)`, long content wraps, and data tables scroll inside their own `.table-wrap` box.

**Tested:** all 4 pages x 4 widths (320, 768, 1024, 1440px) x light and dark = 32 combinations, with `scrollWidth <= clientWidth` on every one. Screenshots are in `docs/screenshots/` (`index-320px.png` ... `index-1440px.png`, `users-*`, dark theme and mobile form errors).

## Dynamic JavaScript & REST API client (`products.html`)

Data comes from the public [FakeStoreAPI](https://fakestoreapi.com) (`/products`, `/products/categories`).

| Requirement | Where |
|---|---|
| `async/await` fetch calls | `js/api.js` (`request`, `cachedGet`), `js/app.js` (`load`, `Promise.all`) |
| Live search, category buttons, sorting without reload | `js/filters.js` + `js/app.js`; search is debounced (200 ms) |
| `localStorage` state | `js/state.js`: cart, search/category/sort preferences, and a 5-minute API response cache |
| Error handling | `ApiError` with friendly messages (HTTP error, timeout, offline, unreadable data); `role="alert"` banner with **Try again**; falls back to stale cached data with a warning banner |
| Loading skeletons | `renderSkeleton()` while fetching, with `aria-busy` on the grid |

Design choices:
- **No `innerHTML` with API data**: nodes are built with `createElement`/`textContent`, so remote content cannot inject markup.
- **Corrupted storage is harmless**: stored values are sanitised on read, and every storage call is wrapped in `try/catch`.
- **Keyboard focus is preserved** when the cart and category buttons re-render.

Because the page uses ES modules, open it through a web server (Live Server or `npm start`), not by double-clicking the file.
