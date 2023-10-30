# Keep documentation with the code

* Status: accepted
* Deciders: @fyliu
* Date: 2023-01-01

Technical Story: We would like to make it easy for developers to contribute documentation.

## Context and Problem Statement

There's a chicken and egg problem where committed code and PR is not synchronized with the wiki documentation. It's also more complicated to have to use 2 tools to implement the same feature and add documentation for it, potentially leading to developers to skip the documentation step, since the documentation step is separate from the PR. Once the PR is approved, it signals that the issue is done.

## Decision Drivers

* Documentation is a good thing for both the project to have and a good practice for the developers to develop.
* Many developers are already used to the wiki.
* The tech lead @fyliu would like to improve the process and encourage more documentation writing, because it's extra important for a backend-only project like PeopleDepot.

## Considered Options

* Documentation as code (DAC)
* Documentation in the wiki

## Decision Outcome

Chosen option: "Documentation as code", because it provides more value in the long run to both the project and to the developers

### Positive Consequences

* encourages good documentation practice in developers
* better process that encourages more documentation to be written
* makes it easier for developers to write documentation (familiar editor, write docs for current feature)

### Negative Consequences

* developers need to switch from the familiar wiki
* extra work reviewing documentation in PRs
* extra PR process when making simple documentation-only changes

## Pros and Cons of the Options

### Documentation as code

Keep the documentation with the code in the code repository

* Good, because it codifies documentation into the development process.
* Good, because developers can work on documentation with the same tools they use to write code
* Good, because it's easier to write documentation while the issue being worked on is fresh in mind.
* Good, because both code and docs can be part of the same PR to b e reviewed.
* Good, because it encourages developers to work on documentation, with the PR process as a potential enforcement mechanism.
* Good, because developers can develop good documentation habits that will be valuable in their career.
* Good, because documentation can be versioned with the code. Documentation in `main`, `dev`, or any given feature branch corresponds to that version of the code.
* Bad, because documentation changes require PRs, which can be a hassle for simple fixes.(updated Dec. 2022 after Ethan pointed out this drawback)
* Bad, because it's a different process than what many developers currently follow.

### Documentation in the wiki

Keep documentation in the wiki

* Good, because it's already familiar to developers.
* Good, because its history can be tracked, since it's a git repository.
* Bad, because its history cannot be tracked alongside the code, since it's a separate git repository from the code.
* Bad, because it forces an unnatural workflow by separating the work of a single issue into the code and PR phase, and the documentation phase. Do developers wait for the PR to be approved before writing the documentation for a feature? Should they draft the documentation in a local wiki repository and then push the changes as soon as the PR is approved, so that the feature is documented?
* Bad, because it relies on developers to be disciplined enough to write documentation. There's no built-in incentive or even the suggestion to write documentation. Once the PR is approved, the issue is done. Documentation is a separate task.
