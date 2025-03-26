# Migrations with Alembic

[Alembi](https://alembic.sqlalchemy.org/en/latest/) is python-based migration making for usage with the  [SQLAlquemy](https://www.sqlalchemy.org/) ecosystem.

## Setup

Create a virtual python environment.

```sh
conda create -n myenv python=3.9
source activate myenv
```

Install requirements(alembic, trino, sqlalquemy)

```sh
pip install -r requirements.txt
```

## Create migration table

Alembic use a table called *alembic_version* to keep track of the latest applied version.

```sql
CREATE TABLE icebergnessie.test.alembic_version (
    version_num VARCHAR(32) NOT NULL
);
```

## Run alembic

```sh
alembic upgrade head
```