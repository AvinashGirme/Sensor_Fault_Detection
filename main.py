import os,sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.application import APP_HOST,APP_PORT
from fastapi import  FastAPI,File,UploadFile
from uvicorn import run as app_run
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from sensor.pipeline.training_pipeline import TrainPipeline


env_file_path=os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):

    if os.getenv('MONGO_DB_URL',None) is None:
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running")
        train_pipeline.run_pipeline()
        return Response("Training Successful !!")
    except Exception as e:
        raise SensorException(e, sys)
        return Response(f"Error Occurred! {e}")
        

def main():
    try:
        set_env_variable(env_file_path)
        training_pipeline=TrainPipeline()
        training_pipeline.run_pipeline()
    
    except Exception as e:
        print(e)
        logging.exception(e)

if __name__=="__main__":
    app_run(app,host=APP_HOST,port=APP_PORT)



