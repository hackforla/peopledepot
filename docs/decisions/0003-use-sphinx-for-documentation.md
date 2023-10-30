# Use sphinx for documentation

* Status: accepted
* Deciders: Fang, Nicole
* Date: 2023-01-01

Technical Story: We need to decide on a documentation system.

## Context and Problem Statement

We're trying to decide between using sphinx and mkdoc, the two most popular documentation generators.

## Decision Drivers

* We want to have sections for architecture details, tutorials, etc.
* It should show a generated table of contents for navigating long pages.
* It should look clean and professional.
* It should be easy for developers to write (ideally, in plain text or markdown)

## Considered Options

* Markdown files on Github
* Sphinx
* Mkdoc
* asciidoc

## Decision Outcome

Chosen option: "Sphinx", because it's in use by more projects, it's python specific, which suits us since we use python, and it's easy to "downgrade" to other systems if we're unhappy later on.

### Positive Consequences

* Better documentation organization and navigation
* Makes our project looks more professional
* Allows us to continue writing markdown if we choose
* More mature, which means better support

### Negative Consequences

* The markdown written for sphinx may not look right in Github, since there are extension syntaxes Github markdown does not support.

## Pros and Cons of the Options

### Markdown files on Github

* Good, because it's already being done in README and CONTRIBUTING
* Bad, because it lacks the sophistications of the documentation generators.
* Bad, because plain markdown becomes inadequate when documentation expands beyond README, INSTALL, and CONTRIBUTING, and when pages get long. The Github wiki solves the long page problem with an auto-generated table of contents, but it has its own problems. See decision 0001 for discussion on that.
* Bad, because it's hacky to do things like dropping to html to make hidden content.
* Bad, because There's only one theme and it's not very pleasing.

### Sphinx

This is the standard documentation generator for python projects, and many other projects also use it. Some published books for professionals are written in sphinx.

* Good, because it's in python and made for the python ecosystem first.
* Good, because many of our dependencies use it, including linux kernel, python, and django.
* Good, because its mature, with lots of useful features and plugins.
* Good, because there's MyST parser, which adds markdown support to all sphinx core functionalities.
* Good, because readthedocs supports it
* Good, because there's lots of themes and plugins.
* Good, because it can cross-reference documentation in other sphinx projects using inter-sphinx
* Bad, because it defaults to restructured text (ReST), which is extra learning for many developers. MyST parser solves this problem.
* Bad, because sphinx plugins may or may not support markdown. It's up to the plugin developers.
* Bad, because it's a little more work to set up than mkdoc. But it's also a positive, because it's easy to transition away if we are unhappy with it.

### Mkdoc

This is a relative newcomer compared to sphinx, but it's a strong contender.

* Good, because it treats markdown as first class.
* Good, because it's easier to get started using.
* Good, because it has a more active developer community.
* Good, because it's quickly catching up to sphinx in featureset.
* Good, because it's used by some of our dependencies, including django REST framework.
* Good, because it's likely more popular among new projects and especially non-python projects.
* Good, because readthedocs supports it
* Good, because there's lots of themes and plugins.
* Good, because there's a plugin that reads inter-sphinx data and allows it to cross-reference sphinx-documented projects' documentation.
* Good, because it's easier to set up than sphinx + MyST. It's a negative because we'd likely just stick with it if we are unhappy with it, because it's more work to switch.
* Bad, because it's not as mature as sphinx
* Bad, because it's not being preferred over sphinx for most serious projects

### asciidoc

This is designed for documentation. I expect the syntax to be more well-thought-out (expressive) than what markdown can be extended to do.
I didn't do as much research on this option, although I have a friend that feels very strongly for this.

* Good, because it seems to be more featureful than the others. In particular, it supports callouts in quoted text, which sphinx doesn't yet, although there's a PR for it.
* Good, because it's probably the best out of all the options in terms of technical merit. The syntax makes more sense.
* Bad, because it's a new syntax to learn
* Bad, because it has a much smaller install base than sphinx and mkdoc.
