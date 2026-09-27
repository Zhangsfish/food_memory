# Contributing

This repository is Larry's personal food memory.

## If you want to record your own food history

Do not submit your meals into Larry's data/.

Fork this repository or copy the protocol into your own repository. Your raw experiences should stay under your ownership.

## If you want to improve the project

Code, schema, documentation, validation, indexing, and workflow improvements are welcome through normal pull requests.

External pull requests must not modify Larry's personal canonical/derived data:
- data/**
- media/**
- self/**
- derived/**
- indexes/**

If a bug is found in Larry's historical record, open an Issue describing the problem rather than rewriting the record from an external account.

## Design principles

- one real eating event = one canonical experience file;
- repeated visits are separate memories;
- preserve first-person wording and concrete reasons;
- unknown stays unknown;
- self-declaration is separate from AI inference;
- generated indexes are never hand-edited;
- no universal restaurant or KOL score.
