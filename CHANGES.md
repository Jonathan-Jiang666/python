# CHANGES — Refactor (commit ba3a8b5)

Short summary
- Centralized configuration into `app/config.py` and introduced `.env.example` for environment secrets.
- Replaced many `print` statements with structured logging and added `init_logging()`.
- Refactored iCloud calendar handling and Gmail/DB modules to read credentials from config.
- Moved `DATABASE_URL` handling into `app/database/db.py` (supports SQLite default).
- Added `requirements.txt` listing runtime dependencies.

Key files modified/added
- `app/config.py` (new) — centralized settings, path helpers, logging init
- `.env.example` (new) — env var template (no secrets checked in)
- `app/business/calendar_event_data_fatory.py` — rewritten and type-hinted
- `app/main/icould_cal_dav.py` — recreated clean iCloud calendar logic
- `app/database/db.py` — read `DATABASE_URL` from config, engine creation
- `app/database/ai_emails_dp.py` — uses config paths, added close() helper
- `app/business/my_task_list.py` — scheduler fixes, uses config/timezone
- `requirements.txt` (new)

Notes & next steps
- Copy `CHANGES.md` contents into PR description if you open one.
- Create a local `.env` from `.env.example` and fill `ICLOUD_USER`/`ICLOUD_PASSWORD` (do NOT commit secrets).
- Consider enabling `APSCHEDULER_JOBSTORE_URL` for persistent jobs in production.
- Optional improvements: add `tenacity` retries on external calls and run full lint/tests.

If you want, I can open a PR with this description or expand the change list with per-file diffs.
