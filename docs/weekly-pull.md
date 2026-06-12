# Weekly Source Pull

## What it does

`tools/pull_all_sources.py` iterates over every entry in
`tools/investor_memos_registry.yaml`, calls the fetcher for each publisher,
downloads up to 5 new posts/memos per source, and writes wiki source cards to
`wiki/sources/`. It then regenerates both index files:

- `docs/markdowns-index.md` — index of all raw source markdowns in `markdowns/`
- `docs/investment-memos-index.md` — index of all ingested investor memos

The pull is **idempotent**: any slug whose card already exists in `wiki/sources/`
is silently skipped; only genuinely new content is fetched.

## Schedule

A cron job runs the pull automatically every **Monday at 07:00** (machine local time):

```
0 7 * * 1 cd /media/ak/d1c5342e-77c5-411d-a9ac-03660a90ce7d/home/ak/Gitrepos/creditmacro && /usr/bin/python3 tools/pull_all_sources.py >> /tmp/creditmacro_weekly_pull.log 2>&1
```

## Log location

Output (stdout + stderr) is appended to:

```
/tmp/creditmacro_weekly_pull.log
```

Note: `/tmp` is cleared on reboot. If you need persistent logs, change the path
in the cron line (edit via `crontab -e`).

## How to run manually

```bash
cd /media/ak/d1c5342e-77c5-411d-a9ac-03660a90ce7d/home/ak/Gitrepos/creditmacro
python3 tools/pull_all_sources.py
```

## How to disable the cron job

Open the user crontab:

```bash
crontab -e
```

Remove (or comment out) the line starting with `0 7 * * 1 cd ...creditmacro`.

To remove all cron jobs entirely:

```bash
crontab -r
```

## How to add a new publisher

1. Edit `tools/investor_memos_registry.yaml` and add a new entry following the
   existing patterns (use `substack:` for Substack-hosted publications, or
   `index_urls:` + `link_selector:` for custom CMS sites).
2. Run `python3 tools/pull_all_sources.py` to test the new entry.
3. The next scheduled Monday run will include it automatically.
