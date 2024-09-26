
# Files structure

## Status
accepted and pending

## Decision
Move protocols and interface implementations into seperate files:
- prtocols.py
- implementation.py

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Options Considered
1. keep all code in main file

## Consequences
What becomes easier or more difficult to do because of this change?
Easier:
- code decoupling
- adding new ways how tcp connections are handled
- main code logic readability
- main file is more readable without logging, that now can exist at implementation lvl
More difficult:
- lots of imports
- track explicit knowledge which Protocol given class implements