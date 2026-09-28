from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from routers.buku import router_buku
from routers.user import router_user

from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.exception_handler(HTTPException)
async def set_Format_JSON_Handler(request: Request, exc: HTTPException):
    
    # if exc.status_code == status.HTTP_403_FORBIDDEN:
    #     with open("403.html", "r", encoding="utf-8") as f:
    #         html_file = f.read();

    #         return HTMLResponse(content=html_file, status_code= status.HTTP_403_FORBIDDEN)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "pesan": str(exc.detail),
            "data": None
        }
    )

app.include_router(router_user)
app.include_router(router_buku)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8080",
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
