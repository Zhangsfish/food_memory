# Experience schema v1

Each eating experience is one self-contained Markdown file under data/<year>/.

The repository intentionally keeps historical experience records simple. A repeated visit to the same restaurant is a new experience file, not an edit to an old one.

## Minimal example

    ---
    schema_version: 1
    id: exp_20260924_zhangsfish_example-noodles_01
    author: github:Zhangsfish
    date: "2026-09-24"

    place:
      id: place_example_noodles_shijiazhuang_mall
      name: 示例面馆（某商场店）
      area: CN/石家庄
      hint: 某商场二楼

    dishes:
      - 牛肉面
      - 凉菜

    cost:
      amount: 46
      currency: CNY
      basis: bill_total

    commercial_relationship: none_declared
    ---

    牛肉面28元。肉挺软，汤对我来说有点甜，下次可能还会点。

## Required fields

### schema_version

Must be 1.

### id

Stable unique ID beginning with exp_.

The ID identifies one eating event. Do not change it because Larry later revisits the same place or changes his opinion.

### author

For this repository, normal records use:

    author: github:Zhangsfish

Forks may use their own globally understandable identifier.

### date

Accepted values:
- YYYY-MM-DD
- YYYY-MM
- YYYY
- unknown

Do not fabricate missing precision.

### place

Required:
- name — human-readable historical place name
- area — coarse retrieval area such as CN/北京 or JP/Tokyo

Optional:
- id — stable repository-local place identity beginning with place_
- hint — branch/disambiguation clue when needed

place.id exists only to connect repeated visits to the same real place. It is not a live business database ID.

If place.id is absent, generated indexes derive a fallback place key from area + name. This keeps writing easy while still allowing repeated identical place names to group automatically.

Do not store live opening hours, current route, or other volatile map facts here.

### dishes

Non-empty list of what Larry consumed or meaningfully evaluated.

## Optional fields

### cost

    cost:
      amount: 46
      currency: CNY
      basis: bill_total

Allowed basis values:
- bill_total
- my_share
- per_person
- itemized
- unknown

### local_relation

Optional self-reported relation to the area:
- resident
- former_resident
- frequent_visitor
- visitor
- unknown

### commercial_relationship

Optional disclosure:
- none_declared
- invited
- discounted
- sponsored
- employee
- owner
- other
- not_provided

### attachments

Repository-relative files under media/.

## Body: the actual memory

The body is the highest-information part of the record.

Prefer concrete first-person observations.

Do not compress the experience into a universal score.

## Repeated visits

Suppose Larry visits the same restaurant three times:

- 2026-09: curry felt very oily;
- 2027-01: a different dish was good;
- 2027-08: curry still felt very oily.

Store three experience files.

The place index may group them, but the raw memories stay separate. This lets an AI distinguish "I dislike this restaurant" from "I repeatedly dislike this particular kind of dish here."

## Intentionally not canonical

Do not store these as historical truth:
- universal restaurant score
- global cuisine ontology
- sentiment score
- recommendation score
- inferred taste profile
- AI summary of Larry
- current opening hours or routes

Self-declarations and AI-derived profiles live in separate layers; see self/README.md and derived/README.md.
