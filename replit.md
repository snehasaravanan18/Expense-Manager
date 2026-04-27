# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.
Also contains a standalone Python Flask expense tracker app.

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.

## Expense Tracker (Python Flask)

Located in `expense-tracker/`. A standalone Flask web app.

### Stack
- **Framework**: Python Flask
- **Database**: SQLite (`expense-tracker/expenses.db`)
- **Frontend**: HTML + CSS (custom, no framework) + Chart.js (CDN)

### Structure
```
expense-tracker/
├── app.py               # Flask routes + SQLite init
├── templates/
│   └── index.html       # Main page (Jinja2 template)
├── static/
│   └── style.css        # All styles
└── expenses.db          # SQLite DB (auto-created)
```

### Features
- Landing page with total spending badge
- Add expense form (name, amount, category dropdown)
- Styled data table with color-coded category badges
- Per-row delete buttons
- Bar chart of spending by category (Chart.js)
- Pre-loaded with 10 sample expenses

### Running
The "Start application" workflow runs: `cd expense-tracker && python app.py`
App listens on `PORT` env var (default 5000).
