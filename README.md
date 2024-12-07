# Flight search service
Fitfth project of non-relational databases

> [!NOTE]
**run.sh** for linux/mac, **run.bat** - for windows machines

> [!TIP]
To run python virtual environment for tests, use commands below

For windows:
```powershell
python -m venv ./.venv
./.venv/Scripts/activate.ps1 
pip3 install -r requirements.txt
pytest ./test/test_api.py
```

For linux/mac:
```shell
python -m venv ./.venv
source ./.venv/Scripts/activate.bat
pip3 install -r requirements.txt
pytest ./test/test_api.py
```