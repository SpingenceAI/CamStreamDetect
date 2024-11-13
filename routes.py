"""API routes for the application."""
from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import StreamingResponse
from logic import StreamHandler
from pydantic import BaseModel

router = APIRouter()

def response_template(
    success, data={}, message=""
):  # pylint: disable=dangerous-default-value
    """
    Returns a standard response template.
    """
    if success:
        return {"status": "success", "data": data, "detail": message}
    raise HTTPException(status_code=500, detail=message)


@router.get("/health")
def information():
    """
    Return information about the image uploader microservice.
    """
    return response_template(True, {}, "microservice is healthy.")


@router.get("/stream")
async def stream():
    """
    Stream the camera feed.
    """
    stream_handler = StreamHandler()
    return StreamingResponse(stream_handler.camera_steamer(), media_type="multipart/x-mixed-replace; boundary=frame") # pylint: disable=line-too-long

class PromptRequest(BaseModel):
    prompt: str

@router.post("/vlm_prompt")
def set_llava_prompt(data: PromptRequest):
    """
    Set the prompt for the llava model.
    """
    stream_handler = StreamHandler()
    stream_handler.set_vlm_prompt(data.prompt)
    return response_template(True, {}, f"set VLM prompt:{data.prompt}")

@router.post("/vm_prompt")
def set_owl_prompt(data: PromptRequest):
    """
    Set the prompt for the owl model.
    """
    stream_handler = StreamHandler()
    # convert the prompt to a specific output
    stream_handler.set_raw_vm_prompt(data.prompt)
    prompt = stream_handler.convert_prompt(data.prompt)
    stream_handler.set_vm_input(prompt)
    return response_template(True, {}, f"raw prompt: {data.prompt}；set vlm prompt:{prompt}")

@router.get("/status")
def get_state():
    """
    Get the state of the stream handler.
    """
    stream_handler = StreamHandler()
    # return response_template(True, {"state": stream_handler.get_status()}, "get state")
    return stream_handler.get_status()

