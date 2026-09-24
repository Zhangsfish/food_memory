# Contributing

The long-term goal is to let many people contribute their own eating experiences while keeping the database simple enough for humans and AI to read.

The project is currently in a pilot phase with the owner's records. The contribution interface is already stable, but broad public contribution should wait until an explicit data/content license is selected.

## Contribution unit

**One real eating experience = one Markdown file.**

Do not submit:
- restaurant advertisements
- scraped reviews
- summaries of what other people said
- synthetic/AI-invented experiences
- rankings compiled from external platforms

You may use AI to structure your own experience, but the underlying observations must be yours.

## How to add an experience

1. Read `SCHEMA.md`.
2. Add one file under `data/<year>/` (or `data/undated/` if the visit date is genuinely unknown).
3. Keep the record self-contained.
4. Add optional photos/receipts under `media/<experience-id>/`.
5. Do **not** edit `indexes/`; they are generated.
6. Open a pull request.

## External PR scope

For ordinary external contributors, pull requests may change only:

- `data/**`
- `media/**`

The repository automatically rejects external PRs that modify maintainer-owned paths such as:

- `AGENTS.md`
- `SCHEMA.md`
- `README.md`
- `CONTRIBUTING.md`
- `scripts/**`
- `tests/**`
- `.github/**`
- `indexes/**`

Repository owners and collaborators may make repository-wide maintenance changes.

If you want to propose a schema, documentation, validation, workflow, or indexing change, open an Issue and explain the proposal instead of bundling it into a food-data PR.

## Writing principles

- Preserve first-person wording and concrete reasons.
- Disagreement is allowed. “Too sweet for me” can coexist with “I loved the sweetness.”
- Do not convert subjective experience into an objective claim about the restaurant.
- Do not add fake precision.
- Do not infer another person's identity, residence, or commercial relationship.
- If you have a commercial relationship relevant to the record, disclose it.

## Corrections

If you later realize a historical fact was wrong (for example, the wrong branch or wrong price), correct the canonical file and explain the correction in the commit/PR.

Do not rewrite an old opinion merely because your taste changed. A later visit should normally be a new experience file.

## Generated data

`indexes/` is a read-optimized projection of `data/`.

It is rebuilt mechanically and contains no AI summaries. If an index conflicts with a canonical record, the canonical record wins.
