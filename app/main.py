# import os
# import shutil
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
# from plan_belt import synchro_summarizer

app = FastAPI()


try:
    from .config import URL_PATH
except ImportError:
    URL_PATH = ""


@app.post(f"{URL_PATH}/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}

# @app.post(f"{URL_PATH}/uploadfiles/")
# async def create_upload_files(
#     files: list[UploadFile], background_tasks: BackgroundTasks
# ):
#     for file in files:
#         return {"filename": file.filename}
    # with open(file.filename, "wb") as buffer:
    # shutil.copyfileobj(file.file, buffer)
    # cwd = os.getcwd()
    # summary = cwd
    # summary_filepath = os.path.normpath(summary[0])
    # summary_filename = str(os.path.basename(os.path.normpath(summary[0])))
    # return FileResponse(
    # summary_filepath,
    # media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    # filename=summary_filename,
    # )


app.mount("/", StaticFiles(directory="app/static",
                           html=True), name="static")


@app.get("/")
async def read_index():
    return HTMLResponse('app/static/index.html')
