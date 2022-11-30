from sensor.configuration.mongo_db_connection import MongoDBClient
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
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
import shutil
import pandas as pd 
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from sensor.pipeline import training_pipeline


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
        return Response(f"Error Occurred! {e}")


@app.post("/upload-file/") 
async def create_upload_file(uploaded_file:UploadFile = File(...)):
    try:
        dir="/config/workspace/predict/input"
        file_location=f"{dir}/{uploaded_file.filename}"
        file_list=os.listdir(dir)
        if uploaded_file.filename =="predict_sensorfault.csv":
            if len(file_list)>0:
                os.remove(file_location)
        with open(file_location,"wb+") as file_object:
            shutil.copyfileobj(uploaded_file.file, file_object)
        
        return {"info": f"file '{uploaded_file.filename} saved at '{file_location}'"}
    except Exception as e:
        return Response(f"Error Occured! {e}")

@app.get("/predict")
async def predict_route():
    try:
        logging.info("Starting Prediction..")
        df=pd.read_csv(r"/config/workspace/predict/input/predict_sensorfault.csv")
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")

        best_model_path=model_resolver.get_best_model_path()
        model=load_object(file_path=best_model_path)
        y_pred=model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        dir="/config/workspace/predict/output"
        #decide how to return file to user
        output=df.to_csv(f"{dir}/predicted.csv")
        output_file_path=f"{dir}/predicted.csv"
        return FileResponse(output_file_path)
    except Exception as e:
        raise Response(f"Error Occured! {e}")


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



