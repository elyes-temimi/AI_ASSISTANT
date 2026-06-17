from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import io
import numpy as np
import google.generativeai as genai
from config2 import HOST, PORT, SERVICE_NAME, SERVICE_VERSION, SAMPLE_RATE, AUDIO_DURATION, GEMINI_API_KEY, GEMINI_MODEL

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(
    title=SERVICE_NAME,
    version=SERVICE_VERSION,
    description="Gemini AI Service: Chat (fake) + Image Generation (real)"
)


class ChatRequest(BaseModel):
    message: str
    mode: str = "text"  # "audio" or "text"
    thread_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    mode: str
    type: str = "llm"


class ImageRequest(BaseModel):
    prompt: str


class ImageResponse(BaseModel):
    type: str = "image"
    success: bool = True
    data: str  # base64 encoded PNG


# ==================== FUNCTION 1: CHAT RESPONSES (FAKE FOR TESTING) ====================



def generate_response(message: str) -> str:
    """
    FUNCTION 1: Chat Response Generator (Simulated)
    - Takes user message
    - Returns text response based on keywords
    - For testing purposes
    """
    message_lower = message.lower().strip()
    
    # Check for keyword matches
    for keyword, response in RESPONSE_MAP.items():
        if keyword in message_lower:
            return response
    
    # Default response
    return f"You asked: '{message}'. This is a simulated response. " + RESPONSE_MAP["default"]


def generate_audio_bytes() -> bytes:
    """
    Generate WAV audio bytes (sine wave)
    Used for audio mode responses
    """
    duration = AUDIO_DURATION
    samples = np.sin(2 * np.pi * 440 * np.linspace(0, duration, int(SAMPLE_RATE * duration)))
    audio_data = (samples * 32767).astype(np.int16)
    
    wav_buffer = io.BytesIO()
    
    # WAV header
    num_channels = 1
    bytes_per_sample = 2
    byte_rate = SAMPLE_RATE * num_channels * bytes_per_sample
    block_align = num_channels * bytes_per_sample
    
    wav_buffer.write(b'RIFF')
    wav_buffer.write((36 + len(audio_data) * bytes_per_sample).to_bytes(4, 'little'))
    wav_buffer.write(b'WAVE')
    wav_buffer.write(b'fmt ')
    wav_buffer.write((16).to_bytes(4, 'little'))
    wav_buffer.write((1).to_bytes(2, 'little'))
    wav_buffer.write(num_channels.to_bytes(2, 'little'))
    wav_buffer.write(SAMPLE_RATE.to_bytes(4, 'little'))
    wav_buffer.write(byte_rate.to_bytes(4, 'little'))
    wav_buffer.write(block_align.to_bytes(2, 'little'))
    wav_buffer.write((16).to_bytes(2, 'little'))
    
    wav_buffer.write(b'data')
    wav_buffer.write((len(audio_data) * bytes_per_sample).to_bytes(4, 'little'))
    wav_buffer.write(audio_data.tobytes())
    
    return wav_buffer.getvalue()


# ==================== FUNCTION 2: IMAGE GENERATION (REAL GEMINI API) ====================

def generate_image(prompt: str) -> bytes:
    """
    FUNCTION 2: AI Image Generation (Real Gemini API)
    - Takes text prompt
    - Calls Gemini API
    - Returns PNG image bytes
    - Errors thrown to caller
    """
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(
        [f"Create a professional image representing: {prompt}"],
        stream=False
    )
    
    # Extract image data from response
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'data'):
                return part.data
    
    raise ValueError("Gemini API did not return image data")

# ==================== API ROUTES ====================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - FUNCTION 1 (Fake responses)
    Supports text and audio modes
    
    Returns:
    {
        "response": "text response",
        "mode": "text",
        "type": "llm"
    }
    """
    try:
        print(f"[CHAT_{request.mode.upper()}] {request.message}")
        text_response = generate_response(request.message)
        return ChatResponse(
            response=text_response,
            mode=request.mode,
            type="llm"
        )
    
    except Exception as e:
        print(f"[CHAT_ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate", response_model=Dict[str, Any])
async def generate(request: ImageRequest):
    """
    Image generation endpoint - FUNCTION 2 (Real Gemini API)
    Returns JSON with base64 encoded PNG image
    
    Returns:
    {
        "type": "image",
        "success": true,
        "data": "base64_encoded_png_data"
    }
    """
    try:
        import base64
        print(f"[IMAGE_GEN] Prompt: {request.prompt}")
        image_bytes = generate_image(request.prompt)
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        return {
            "type": "image",
            "success": True,
            "data": image_base64
        }
    
    except Exception as e:
        print(f"[IMAGE_ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION
    }


@app.get("/")
async def root():
    """Service info"""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "functions": {
            "chat": "generate_response() - Simulated chat",
            "image": "generate_image() - Real Gemini API"
        },
        "endpoints": {
            "chat": "/api/chat (POST)",
            "image": "/api/generate (POST)"
        }
    }


if __name__ == "__main__":
    print(f"\n{'='*50}")
    print(f"Starting {SERVICE_NAME}")
    print(f"{'='*50}")
    print(f"Server: http://{HOST}:{PORT}")
    print(f"Chat: POST /api/chat")
    print(f"Image Gen: POST /api/generate")
    print(f"{'='*50}\n")
    
    uvicorn.run(app, host=HOST, port=PORT)
