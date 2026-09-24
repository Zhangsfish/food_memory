# Experience schema v1

Each eating experience is one Markdown file under:

```text
data/<year>/<experience-id>.md
```

The file contains YAML front matter followed by free-form first-person experience text.

## Minimal example

```markdown
---
schema_version: 1
id: exp_20260924_zhangsfish_example-noodles_01
author: github:Zhangsfish
date: "2026-09-24"

place:
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

local_relation: visitor
commercial_relationship: none_declared
---

牛肉面28元。肉挺软，汤对我来说有点甜，下次可能还会点。

凉菜18元，一般，不太想再点。

我一个人一共花了46元。
```

The example above documents the format only. It is not a real experience record.

## Required fields

### `schema_version`

Must be:

```yaml
schema_version: 1
```

### `id`

A stable unique ID beginning with `exp_`.

Recommended pattern:

```text
exp_<date>_<author>_<short-place-slug>_<sequence>
```

The ID is identity, not a description. Do not change it merely because a restaurant changes name.

### `author`

Globally understandable contributor identifier.

For GitHub contributions, use:

```yaml
author: github:USERNAME
```

The field is a claim carried by the record; Git history provides additional provenance. Future trust systems may verify stronger identity properties separately.

### `date`

Historical visit date as known by the contributor.

Accepted precision:

```text
YYYY-MM-DD
YYYY-MM
YYYY
```

Do not fabricate missing precision.

### `place`

Required:

```yaml
place:
  name: Human-readable place name
  area: CN/石家庄
```

Optional:

```yaml
  hint: 某商场二楼 / 火车站东门店 / other branch clue
```

#### `place.area`

A coarse retrieval path, not a postal address.

Use a two-letter uppercase country code followed by the locality needed for retrieval:

```text
CN/石家庄
NZ/Auckland
JP/Tokyo
```

If a locality is ambiguous, add only the region required to disambiguate:

```text
US/Illinois/Springfield
```

Do not add district/street/coordinates merely for completeness. Current geospatial details belong to map/place services.

### `dishes`

A non-empty list of what the contributor consumed or meaningfully evaluated.

```yaml
dishes:
  - 牛肉面
  - 凉菜
```

Use the contributor's recognizable names. Do not force a global cuisine taxonomy.

## Optional fields

### `cost`

Only store a number whose meaning is actually known.

```yaml
cost:
  amount: 46
  currency: CNY
  basis: bill_total
```

Allowed `basis` values:

- `bill_total` — total bill for the visit
- `my_share` — amount paid/borne by the contributor
- `per_person` — explicitly reported per-person amount
- `itemized` — amount refers to itemized prices described in the body
- `unknown` — amount is known but its basis is not

Do not compute and store redundant per-person figures from a total bill. AI or software can calculate them later.

### `local_relation`

Optional self-reported relationship to the place area:

- `resident`
- `former_resident`
- `frequent_visitor`
- `visitor`
- `unknown`

Do not infer this field from where the meal occurred.

### `commercial_relationship`

Optional self-declared relationship relevant to bias/provenance:

- `none_declared`
- `invited`
- `discounted`
- `sponsored`
- `employee`
- `owner`
- `other`
- `not_provided`

`none_declared` means the contributor explicitly declares none; absence does not mean none.

### `attachments`

Optional list of repository-relative files:

```yaml
attachments:
  - media/exp_xxx/photo-01.jpg
  - media/exp_xxx/receipt.jpg
```

Attachments are supporting material, not mandatory proof.

## Body: the actual experience

The Markdown body is the highest-information part of the record.

Prefer concrete first-person observations:

> 肉特别嫩，炭火味很重，我喜欢。但是酱对我来说偏甜，下次会让他少刷一点。

Avoid replacing observations with compressed scores:

> 口味 8.2/10，环境 7.5/10。

The database should preserve observations as late as possible and let AI perform interpretation at query time.

## Intentionally not in schema

Do not maintain these as canonical experience fields:

- latitude/longitude
- canonical street address
- opening hours
- current open/closed status
- route or distance
- global restaurant score
- cuisine ontology
- sentiment score
- recommendation score
- contributor taste profile
- AI summary of the experience

They are either volatile, derivable, or interpretive.
