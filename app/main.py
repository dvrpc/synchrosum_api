import os
import shutil
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from plan_belt.synchro_summarizer import SynchroTxt, SynchroSim

app = FastAPI()


try:
    from .config import URL_PATH
except ImportError:
    URL_PATH = ""


@app.post(f"{URL_PATH}/uploadfiles/")
async def create_upload_files(files: list[UploadFile], background_tasks: BackgroundTasks):
    files.sort(key=lambda f: os.path.splitext(f.filename)[1])
    for file in files:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    cwd = os.getcwd()
    if len(files) == 1:
        if files[0].filename.endswith(".txt"):
            summary = SynchroTxt(cwd + "/" + files[0].filename)
            filepath = summary.excel_path
        elif files[0].filename.endswith(".pdf"):
            summary = SynchroSim(cwd + "/" + files[0].filename, "true")
            filepath = summary.excel_path
    elif len(files) == 2:
        summary = SynchroTxt(cwd + "/" + files[1].filename, files[0].filename)
        filepath = summary.excel_path
    background_tasks.add_task(cleanup)
    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="synchro_sum.xlsx",
    )


def cleanup():
    path = os.getcwd()
    os.chdir(path)
    targets = [".xlsx", ".xls", ".pdf", ".txt"]
    for file in os.listdir(path):
        for target in targets:
            if file.endswith(target):
                os.remove(file)


app.mount(f"{URL_PATH}/", StaticFiles(directory="app/static", html=True), name="static")


@app.get(f"{URL_PATH}/")
async def read_index():
    return HTMLResponse("app/static/index.html")
