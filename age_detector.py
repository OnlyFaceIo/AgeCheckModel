from fastapi import FastAPI,UploadFile, File
import uvicorn
import os 
from datetime import datetime
from insightface.app.common import Face

from PIL import Image
import insightface
import cv2
import numpy as np
import json

app = FastAPI()

FACE_ANALYSER = insightface.app.FaceAnalysis(
    name='buffalo_l', providers=['CPUExecutionProvider'])
FACE_ANALYSER.prepare(ctx_id=0, det_size=(320, 320))


def get_one_face(frame: np.array, analyzer:insightface.app.FaceAnalysis, position: int = 0, ) -> Face :
    many_faces = analyzer.get(frame)
    if many_faces:
        try:
            return many_faces[position]
        except IndexError:
            return many_faces[-1]
    return None

@app.get("/")
def hello():
    return {"API":"API is working fine"}

@app.post("/faceinfo")
async def upload_image(img_file:UploadFile =File(...)):

    today_date=str(datetime.now().date())
    current_time=str(datetime.now().strftime("%H_%M_%S"))

    # if '.jpg' in img_file.filename or '.jpeg' in img_file.filename or '.png' in img_file.filename:
    contents = await img_file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    face = get_one_face(img, FACE_ANALYSER)

    return json.dumps({
            'gender': int(face.gender),
            'sex': face.sex,
            'age': int(face.age)
            })


if __name__=="__main__":
    uvicorn.run(app,)