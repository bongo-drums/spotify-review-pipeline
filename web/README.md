# Dashboard (Next.js backend + Supabase Postgres)

The backend is the set of API routes under `app/api/` (`/api/overview`, `/api/issues`, `/api/issues/<id>`,
`/api/reviews/<id>`, `/api/memo`). They read the pipeline's saved outputs from the database and serve them
to the single-page dashboard in `components/Dashboard.tsx`. Nothing is recomputed in the browser and no model
is called at request time.

## Data

1. Create the tables once: `psql "$SUPABASE_DB_URL" -f db/schema.sql` (the loader also runs it).
2. Load a finished run: `python -m pipeline.publish --run runs/full --db "$SUPABASE_DB_URL"`
   (`pip install 'psycopg[binary]'`). Tables: `runs`, `aggregates`, `issues`, `membership`, `records`, `claims`, `memo`.
3. Without a database (local development, CI): `python -m pipeline.publish --run runs/pilot10000` writes a JSON
   snapshot into `web/data/`, and the same API routes read that instead. The response's `source` field says
   which backend answered (`postgres` or `files`).

## Run

```bash
cd web && npm install
DATABASE_URL="$SUPABASE_DB_URL" npm run dev      # or omit DATABASE_URL to use web/data
```

## Deploy (Vercel)

Live: https://spotify-review-dashboard-lilac.vercel.app (Vercel project `spotify-review-dashboard`, root
directory `web`, framework Next.js). The CLI links the git root, so deploy from the repository root:

```bash
npx vercel link --yes --project spotify-review-dashboard --token "$VERCEL_TOKEN"
printf '%s' "$SUPABASE_DB_URL" | npx vercel env add DATABASE_URL production --token "$VERCEL_TOKEN"   # once
npx vercel --prod --yes --token "$VERCEL_TOKEN"
```

`DATABASE_URL` (Supabase connection string, pooled port 6543 recommended) is stored as a production secret. Vercel
rejects deploys on Next.js versions it flags as vulnerable, so keep `next` in `package.json` current.
`/api/overview` reports `source: "postgres"` once `python -m pipeline.publish --run runs/<id> --db "$SUPABASE_DB_URL"`
has loaded a run; before that it returns `relation "runs" does not exist`.
