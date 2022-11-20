from sensor.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os

class TargetValueMapping:
    def __init__(self):
        self.neg: int=0
        self.pos: int=1

    def to_dict(self):
        return self.__dict__
        