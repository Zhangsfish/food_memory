# food_memory

An open, AI-readable record of first-person eating experiences.

This repository is a **data layer**, not a restaurant-ranking app. It stores what people actually ate, where, when, what they paid, and what they thought in their own words. AI clients can retrieve those records and decide what is relevant for a particular question or person.

## Two primary use cases

1. **Recall my own food history**  
   Example: “What noodles have I eaten before?” or “What patterns do you see in what I tend to like?”  
   Retrieval axis: `author`.

2. **Read human traces from a place**  
   Example: “I’m visiting Shijiazhuang. What have people recorded eating there?”  
   Retrieval axis: `place.area`.

A personalized destination query can combine both: read a user’s own history, read records from the destination, then let the AI reason across the two.

## Core boundary

The repository stores **historical experience data**:

- author
- date
- restaurant/place name
- coarse area used for retrieval
- enough optional place hint to distinguish branches when necessary
- dishes
- the price actually reported and its meaning
- first-person experience text
- optional contributor/place relationship, commercial disclosure, and attachments

The repository does **not** try to maintain information that can be obtained or recomputed later:

- exact coordinates
- canonical street address
- current opening hours
- whether a restaurant is still open
- current route, walking time, or distance
- restaurant rankings or universal scores
- inferred taste profiles
- AI-generated recommendations

Those belong to external place/route services or to the AI at query time.

## Source of truth

`data/` is the only canonical human-maintained dataset.

Each meal/visit is one self-contained Markdown file. Generated indexes under `indexes/` are derived views and can always be rebuilt.

Humans and agents should **never manually maintain duplicated restaurant, contributor, dish, or taste-profile databases**.

## Repository layout

```text
food_memory/
├── README.md
├── AGENTS.md
├── SCHEMA.md
├── CONTRIBUTING.md
├── data/                         # canonical experience records
├── media/                        # optional attachments
├── indexes/                      # generated, not hand-edited
│   ├── catalog.json
│   ├── by-author/
│   └── by-place/
├── scripts/
│   ├── validate.py
│   └── build_indexes.py
├── tests/
│   └── test_contract.py
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── validate-and-index.yml
```

## For AI clients

Read `AGENTS.md` first. It defines retrieval order, write rules, safety boundaries, and when reasoning or external tools should take over.

## For contributors

Read `SCHEMA.md` and `CONTRIBUTING.md`.

For now, this repository is being tested with the owner's own records. The contribution structure is already designed for multiple authors; before broad public contribution opens, the repository should select an explicit data/content license.
