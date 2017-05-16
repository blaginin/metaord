# Metaorder CRM

### Setup
On Unix systems `make`, otherwise:
- Make virtualenv - `python -m venv menv`
- Activate it - `cd menv/Scripts/ & activate.bat & cd ../..`
- Install e.g. - `pip install -r deps/local.txt`
- Migrate DB - `python apps/manage.py migrate`
- Run - `python apps/manage.py runserver`


### Deploy checklist*:
- Resotre and stop: `screen -r`
- Dump db: `python apps/manage.py dumpdata > db_DATE.json`
- Reset `settings.py`
- Pull changes
- [`python apps/manage.py migrate`]
- `python apps/manage.py runserver 0.0.0.0:80`

* https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/


### Project structure
- `deps` folder contain pip dependencies.
- `apps` standart Django apps folder.


### Requirements
- Python >= 3.4
- PostgreSQL >= 9.5
- pip
- virtualenv
- [make]
