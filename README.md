# synchrosum_api
API for the SynchroSum toolset
## Production

(TBD)

## Development

### Dependencies 

```
python3 -m venv ve
. ve/bin/activate
pip install -r reqs/requirements_dev.txt
```

### Development Server

Launch Uvicorn server with: `uvicorn app.main:app --reload`.

Upload a Synchro Report, Simtraffic report, or one of each, and a summary will be returned to your browser. 
