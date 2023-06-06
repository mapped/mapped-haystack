
Mapped Haystack
===============

Mapepd Haystack is a Haystack HTTP endpoint using Mapped GraphQL API as a data source. This is currently an alpha version and will be actively updated in the next few weeks. Consider this is v0.0.1.


## How to Install?
This is a Python [poetry](https://python-poetry.org/) project.  

`poetry install` to install dependencies.

## How to Run?
1. Create an account at [Mapped](app.mapped.com/signup)
2. Go to [the developer portal](https://developer.mapped.com/docs/introduction) and create a PAT [here](https://developer.mapped.com/tools/personal-access-token)
3. Create `.env` by copying it from `.env.example`.
4. Update `PAT` value with the one generated at 2.
5. Run `flask --app mapped_haystack.server run` (possibly after `poetry shell` within your poetry environment)


## Available Endpoint

- [Read](https://project-haystack.org/doc/docHaystack/Ops#read):
  - [x] by filter: filter over points is only available for now but it will be gneralized to any types. `spaceRef` is to be implemented.
  - [ ] by id: under dev. 
  - [ ] only `zinc` is supported but will support `hayson` soon as well.
