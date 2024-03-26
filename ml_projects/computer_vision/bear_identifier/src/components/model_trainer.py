from dataclasses import dataclass
from data_ingestion import DataIngestion
from fastai.vision.all import *
import os

@dataclass
class ModelTrainerConfig:
    trained_model_filepath = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    def initiate_model_training(self):
        data = DataIngestion()
        path = Path(data.ingestion_config.raw_data_path)
        bears = DataBlock(
                        blocks=(ImageBlock, CategoryBlock), 
                        get_items=get_image_files, 
                        splitter=RandomSplitter(valid_pct=0.2, seed=42),
                        get_y=parent_label,
                        item_tfms=Resize(128, method='squish')
                        )
        bears = bears.new(
                        item_tfms=RandomResizedCrop(224, min_scale=0.5),
                        batch_tfms=aug_transforms()
                        )
        dls = bears.dataloaders(path)
        model = vision_learner(
                dls, 
                resnet18, 
                metrics = error_rate
                )
        model.fine_tune(4)
        save_object(
                    self.model_trainer_config.trained_model_file_path, 
                    model)