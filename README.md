# Larry.food / Food Memory

A public, AI-readable memory of one person's real eating life.

This repository is Larry's canonical food-memory layer. It is designed so that an AI can answer two kinds of questions without rereading the whole history:

1. Owner questions: "What have I eaten before?", "How has my taste changed?", "What should I avoid repeating?"
2. Visitor questions: "Is Larry's experience useful for me?", "What did Larry eat in this place?", "Which of his records match my needs?"

The key idea is simple:

- experiences are evidence;
- Larry's own declarations are self-reports;
- AI profiles are derived interpretations;
- indexes are generated retrieval views.

Never collapse those four things into one "true profile".

## Daily write path

Normal use should be low-friction:

1. Larry gives an authorized AI a photo/order screenshot plus a short first-person reaction.
2. The AI creates exactly one new Markdown experience under data/.
3. GitHub Actions validates the record and rebuilds indexes.
4. Nothing else needs to be hand-maintained for that meal.

A meal entry never overwrites an older opinion. Repeated visits to the same place create repeated experiences.

## Canonical vs generated

Human/authorized-agent maintained:
- data/ — first-person eating experiences
- self/events/ — explicit self-declarations, only when Larry intentionally makes one
- media/ — optional public attachments

Generated or replaceable:
- indexes/ — deterministic retrieval views
- derived/ — optional AI-generated food-profile snapshots; never canonical truth

## Retrieval layers

An AI should not scan every record.

Use this order:

1. indexes/catalog.json — discover what exists.
2. Relevant index:
   - by-time — recent/history questions
   - by-area — city/locality questions
   - by-place — repeated visits to the same place
   - by-author — compatibility/general tooling
3. Open only the relevant canonical source files under data/ when exact wording or evidence matters.
4. If a derived profile exists, treat it as a cache and verify important claims against evidence.

## Repository layout

    food_memory/
    ├── README.md
    ├── AGENTS.md
    ├── SCHEMA.md
    ├── HOW_TO_USE.md
    ├── CONTRIBUTING.md
    ├── data/                 # canonical experience records
    ├── self/
    │   └── README.md         # self-declaration protocol
    ├── derived/
    │   └── README.md         # optional AI profile snapshots
    ├── media/                # optional public attachments
    ├── indexes/              # generated retrieval views
    ├── scripts/
    ├── tests/
    └── .github/workflows/

## Scope

This repository is currently Larry's personal food memory, not a shared multi-user database.

If you want your own callable food memory, fork the repository or copy the protocol and keep your own canonical history. A future network can connect independent people without mixing ownership of their raw memories.

## Important boundary

Food Memory does not maintain volatile real-world business facts such as current opening hours, routes, live availability, or rankings. Use map/business services for those at query time.

Read HOW_TO_USE.md for copy-paste prompts and AGENTS.md for the machine protocol.
