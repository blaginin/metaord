# Metaorder CRM

### Setup
On Unix systems `make`, otherwise:
- Make virtualenv - `python -m venv menv`
- Activate it - `cd menv/Scripts/ & activate.bat & cd ../..`
- Install e.g. - `pip install -r deps/local.txt`
- Migrate DB - `python apps/manage.py migrate`
- Run - `python apps/manage.py runserver`

### Project structure
- `deps` folder contain pip dependencies.
- `apps` standart Django apps folder.

### Requirements
- Python >= 3.4
- PostgreSQL >= 9.5
- pip
- virtualenv
- [make]
