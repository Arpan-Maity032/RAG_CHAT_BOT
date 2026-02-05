import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic  import BaseModel
from ragservice import rag_model

app = FastAPI(title="RAG Backend")

class QueryRequest(BaseModel):
    query:str

@app.get("/")
def health_check():
    return {"status":"ok"}

@app.post("/chat")
def chat_endpoint(request: QueryRequest):
    try:
        response = rag_model.ask_question(request.query)
        return {"answare":response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
def upload_document(file:UploadFile = File(...)):
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir,exist_ok=True)
    file_path = f"{temp_dir}/{File.filename}"

    try:
        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        num_chunks = rag_model.addFile(file_path,file.filename)
        os.remove(file_path)

        return {"filename":file.filename, "chunks_added": num_chunks}
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500,detail=str(e))



