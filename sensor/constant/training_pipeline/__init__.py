import os
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME

SAVED_MODEL_DIR = os.path.join("saved_models")
#defining common constant variable for training pipeline
TARGET_COLUMN ="class"
PIPELINE_NAME: str ="sensor"
ARTIFACT_DIR: str ="artifact"
FILE_NAME: str ="sensor.csv"




"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str ="sensor"
DATA_INGESTION_DIR_NAME: str ="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str ="feature_store"
DATA_INGESTION_INGESTED_DIR: str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float =0.2
