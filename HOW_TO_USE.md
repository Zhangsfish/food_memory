# How to use Larry.food

The repository is public. An AI client that can read GitHub pages/files can use it directly.

## 1. Visitor: decide whether Larry is useful to you

Copy this:

    Read the public repository Zhangsfish/food_memory.
    Start with indexes/catalog.json and AGENTS.md.
    I will tell you my food preferences and current need.
    First decide which parts of Larry's history are relevant to me.
    Then retrieve only the relevant records, not the whole repository.
    Separate Larry's explicit words, stored facts, and your inference.
    Do not invent facts that are not in the repository.

## 2. Visitor: use Larry's experience in a place

Example:

    Read Zhangsfish/food_memory.
    I am looking for food in Beijing. I do not eat meat and I do not want something very oily.
    Find Larry's relevant Beijing experiences.
    Use his original first-person records as evidence.
    Tell me where his experience is useful and where it may not transfer to me.
    For current opening hours, routes, or whether a restaurant still exists, use current external sources separately.

## 3. Larry: recall my own history

Example:

    Read my food memory repository Zhangsfish/food_memory.
    Have I eaten at this place before?
    If yes, retrieve every relevant visit in time order and explain whether my opinion changed.
    Quote or point back to the original experience records when useful.

## 4. Larry: make a decision

Example:

    Read my food memory.
    I want dinner tonight, under 50 CNY, not very oily, and I want some exploration rather than repeating my recent meals.
    First inspect my recent history and any relevant long-term patterns.
    Then give me options.
    Keep historical evidence separate from your own recommendation.

## 5. Larry: record a meal

For an authorized agent with GitHub write access:

    Record this meal in Zhangsfish/food_memory according to AGENTS.md and SCHEMA.md.
    Create one new canonical experience file only.
    Preserve my first-person wording.
    Do not manually edit indexes or any derived profile.
    Let repository automation rebuild generated indexes.

Input can be as little as:
- a food photo or order screenshot;
- one short first-person reaction.

Unknown metadata should remain unknown rather than being guessed.

## 6. Explicit self-declaration

Only use this when Larry is intentionally stating a general preference or correction, not merely reacting to one meal.

Example:

    Record this as an explicit self-declaration, separate from meal history:
    "I do not actually enjoy desserts. Photos often make me want to buy them, but post-consumption satisfaction is usually low."

See self/README.md.

## What not to do

- Do not scan the whole repository when an index can narrow the search.
- Do not overwrite an older meal because Larry changed his mind later.
- Do not convert subjective experience into a universal restaurant score.
- Do not treat an AI-generated profile as canonical truth.
