import os
import shutil
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from plan_belt.synchro_summarizer import SynchroTxt

app = FastAPI()


try:
    from .config import URL_PATH
except ImportError:
    URL_PATH = ""


@app.post(f"{URL_PATH}/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile], background_tasks: BackgroundTasks
):
    for file in files:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            cwd = os.getcwd()
            summary = SynchroTxt(cwd + "/" + file.filename)
            filepath = summary.excel_path
    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="synchro_sum.xlsx",
    )


app.mount("/", StaticFiles(directory="app/static",
                           html=True), name="static")


@app.get("/")
async def read_index():
    return HTMLResponse('app/static/index.html')
