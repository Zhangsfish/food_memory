# Self-declarations

This directory is for things Larry explicitly says about his own food preferences, constraints, or current state.

It is intentionally separate from:
- data/ — what actually happened in meals;
- derived/ — what an AI infers from evidence.

## Event model

Self-declarations should be append-only events under:

    self/events/<year>/<declaration-id>.md

Example:

    ---
    schema_version: 1
    id: self_20260927_dessert
    date: "2026-09-27"
    topic: dessert
    ---

    我其实不爱吃甜点。甜点图片很容易让我觉得可能好吃，但实际吃完通常觉得一般。

Do not create a self-declaration merely because an AI notices a pattern.

A later declaration may correct, narrow, or supersede an earlier one. Preserve history rather than silently erasing the old statement.

No self-declaration event exists yet unless Larry explicitly asks to record one.
