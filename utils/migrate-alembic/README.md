# Migrations with Alembic

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
