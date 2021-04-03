# nom bot

Discord bot for nomming people in m's rat chat server.

## Commands

* `<nom @rat` – nom a user
* `<unnom @rat` – unnom a user
* `<noms` – list all noms
* `<bun` – send a picture of a bun
* `<tok` – join the current voice channel for a bit

## Requirements

* [Python 3](https://www.python.org/downloads/)
* Python libraries: [discord.py](https://discordpy.readthedocs.io/en/latest/intro.html), [asyncpg](https://magicstack.github.io/asyncpg/), [psycopg2](https://pypi.org/project/psycopg2/), [requests](https://pypi.org/project/requests/)

## Environment variables

* `RATS_NOM_TOKEN` – Discord bot token
* `DATABASE_URL` – PostgreSQL connection URI