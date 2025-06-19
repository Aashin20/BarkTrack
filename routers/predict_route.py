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


@router.post("/panting")
async def analyze(file: UploadFile = File(...),current_user: dict = Depends(get_current_user),):
    temp_video_path = None
    try:
       
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_video_path = temp_file.name
            content = await file.read()
            temp_file.write(content)
        
        print(f"[INFO] Received video file: {file.filename}")
        print(f"[INFO] Saved video to: {temp_video_path}")
        
     
        result = analyze_video(temp_video_path)
        print(f"[INFO] Analysis result: {result}")
        
        return {"result": result}
    
    except Exception as e:
        print(f"[ERROR] Exception occurred during processing: {str(e)}")
        return {"error": f"Processing failed: {str(e)}"}
    
    finally:
      
        if temp_video_path:
            safe_delete_file(temp_video_path)
    
