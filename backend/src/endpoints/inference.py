import json
from typing import List
from fastapi import File, UploadFile
from fastapi import APIRouter
from fastapi.responses import JSONResponse

import torch
from urllib.request import urlopen
from PIL import Image

from open_clip import create_model_from_pretrained, get_tokenizer

from utils.custom_logger import logger

logger.info("Loading model")
model, preprocess = create_model_from_pretrained('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224', cache_dir='/tmp')
tokenizer = get_tokenizer('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')
logger.info("Model loaded")

logger.info("Setting up device")
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)
model.eval()
logger.info("Device set up")

router = APIRouter()


@router.post("/inference")
def inference(image: UploadFile, labels: List[str], top_k: int = -1):
    try:
        template = 'this is a photo of '
        context_length = 256
        image_data = Image.open(image.file)
        labels = labels[0].split(",")
        
        # Create embeddings
        pre_processed_image =  torch.stack([preprocess(image_data)])
        texts = tokenizer([template + l for l in labels], context_length=context_length).to(device)
        
        with torch.no_grad():
            image_features, text_features, logit_scale = model(pre_processed_image, texts)

            logits = (logit_scale * image_features @ text_features.t()).detach().softmax(dim=-1)
            sorted_indices = torch.argsort(logits, dim=-1, descending=True)

            logits = logits.cpu().numpy()
            sorted_indices = sorted_indices.cpu().numpy()

        # Predict top k
        top_k = len(labels) if top_k == -1 else top_k
        predictions = []
        for j in range(top_k):
            jth_index = sorted_indices[0][j]
            predictions.append({"class": labels[jth_index], "probability": str(logits[0][jth_index])})
            logger.info(f'{labels[jth_index]}: {logits[0][jth_index]}')
        
        return JSONResponse(status_code=200,
                            content={"data": predictions,
                                    "message": "Preidction successful"})
    except Exception as err:
        logger.error(f"Making prediction failed: {err}")
        return JSONResponse(status_code=500,
                            content={"data": {},
                                     "message": "Prediction endpoint is not healthy"})
