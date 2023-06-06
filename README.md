
Mapped Haystack
===============

Mapepd Haystack is a Haystack HTTP endpoint using Mapped GraphQL API as a data source. This is currently an alpha version and will be actively updated in the next few weeks.


## How to Install?
This is a Python [poetry](https://python-poetry.org/) project.  

`poetry install` to install dependencies.

## How to Run?
`flask --app mapped_haystack.server run`

## Available Endpoint

- [Read](https://project-haystack.org/doc/docHaystack/Ops#read):
  - [x] by filter: filter over points is only available for now but it will be gneralized to any types. `spaceRef` is to be implemented.
  - [ ] by id: under dev. 
  - [ ] only `zinc` is supported but will support `hayson` soon as well.
