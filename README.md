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
├── css/               base.css (layout, tokens) + components.css
├── js/components/     modal.js, form-validation.js, char-count.js
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
