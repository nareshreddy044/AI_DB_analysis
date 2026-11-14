# DB Monitor (Oracle connect only)

Minimal Python app: connect to a remote Oracle database and verify the link.

## Setup

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # if needed
# edit .env with real Oracle host / user / password
# and either ORACLE_SERVICE or ORACLE_SID
```

## Service name vs SID

In `.env`, set **one** of:

```env
ORACLE_SERVICE=ORCLPDB1    # modern / PDB — usual choice
# ORACLE_SID=ORASID        # older SID style — comment out SERVICE
```

Priority: `ORACLE_DSN` → `ORACLE_SERVICE` → `ORACLE_SID`.  
If both SERVICE and SID are filled, **service name wins**.

No spaces around `=` (`ORACLE_SID=ORASID`, not `ORACLE_SID =ORASID`).

## Run

```bash
python main.py test-connection
```

## Layout

```
main.py
.env                 # your Oracle credentials
db_monitor/
  config.py          # reads .env (service or SID)
  cli.py             # test-connection command
  connectors/
    oracle.py        # opens / closes Oracle connection
```
