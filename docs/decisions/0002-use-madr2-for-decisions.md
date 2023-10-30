# Use MADR2 for decisions

* Status: accepted
* Deciders: @fyliu
* Date: 2023-02-05

## Context and Problem Statement

We need a way to record past decisions and reasoning for new developers to understand them.

## Decision Drivers

* easy to write
* records the motivations of decisions
* alternatives and pros and cons of each
* lists the alternatives considered so future managers with fresh ideas can revisit the decisions to see if they've already been considered and why they were rejected.
* confidence to make new decisions if reasonings for old decisions are no longer relevant, or if there's better alternatives that's not considered or available before.

## Considered Options

* Wiki pages
* ADR Michael Nygard's original template
* MADR 2 - markdown
* MADR 3

## Decision Outcome

Chosen option: "MADR 2", because it's in the familiar markdown and there's a tool to help write it.

### Positive Consequences

* Improved decision capture

## Pros and Cons of the Options

### Wiki pages

Record decisions in the wiki

* Good, because it's already there
* Good, because it's easy to use
* Bad, because it's unstructured so it's harder for beginners to write a good one.

### ADR Michael Nygard's original template

The template is this:
- Title
- Context
- Decision
- Status
- Consequences

* Good, because it has structure
* Good, because it lives along side the code
* Good, because there are tools to help write it.
* Bad, because it's not explicit enough. We want to have a list of alternatives that were considered.

### MADR 2

[Markdown Any Decisions Records 2.1.2](https://github.com/adr/madr/blob/2.1.2/template/template.md)

* Good, because it has structure
* Good, because it captures the alternatives
* Good, because it lives along side the code
* Good, because there are tools available to help write it.
* Bad, because there's a newer version 3, although there's nothing preventing using that for future decisions.

### MADR 3

[Markdown Any Decisions Records 3.0.0](https://github.com/adr/madr/blob/3.0.0/template/adr-template.md)

* Good, because it captures more useful details than MADR 2
* Bad, because there's no tools to help write it.

## Links

* [MADR description](https://adr.github.io/madr/)
* [helper tools](https://adr.github.io/madr/tooling.html)
