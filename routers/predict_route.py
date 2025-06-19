from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from PIL import Image
import io
from utils.auth import get_current_user
from utils.breed import preprocess_image, get_prediction
import tempfile
import traceback
from utils.panting import analyze_video,safe_delete_file
from utils.rib_compression import rib_analyze_video

router = APIRouter()

@router.post("/breed")
async def predict_breed(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        processed_image = preprocess_image(image)
        model = request.app.state.breed_model
        prediction = get_prediction(model, processed_image)

        return {
            "prediction": prediction,
            "user": current_user["name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


