from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Request,
    Response,
    status,
    Form,
    Query,
)
from fastapi.security import APIKeyHeader
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timedelta
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
import qrcode
from io import BytesIO
from starlette.responses import StreamingResponse
from app.utils import *
from app.schemas import *
from app.database import *
from app.models import *
import string
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = "".join(random.choice(characters) for _ in range(6))
    return short_url


@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(request, name="index.html")


@app.post("/shorten")
async def shorten_url(
    request: Request,
    response: Response,
    original_url: str = Form(),
    custom_url: str = Form(None),
    db: Session = Depends(get_db),
):
    if custom_url:
        short_url = custom_url
    else:
        short_url = generate_short_url()
    new_url = URL(shortened_url=short_url, original_url=original_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return templates.TemplateResponse(
        "index.html", {"request": request, "short_url": short_url}
    )


@app.post("/custom_shorten")
async def create_custom_url(
    url_request: URLRequest, db: Session = Depends(get_db), original_url: str = Form()
):
    if db.query(URL).filter(URL.custom_url == url_request.custom_url).first():
        raise HTTPException(status_code=400, detail="Custom URL already in use")
    new_url = URL(
        original_url=url_request.original_url, custom_url=url_request.custom_url
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url


@app.get("/download-qrcode")
async def download_qr_code_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate_qr")
async def generate_qr(original_url: str = Form(...)):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(original_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes_io = BytesIO()
    img.save(img_bytes_io, format="PNG")
    img_bytes_io.seek(0)

    return StreamingResponse(
        img_bytes_io,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=qr_code.png"},
    )


@app.get("/analytics")
def record_analytics(request: Request):
    return templates.TemplateResponse("index.html", {"request": Request})


@app.get("/link-analytics")
async def get_link_analytics(
    short_url: Optional[str] = Query(None, min_length=1), db: Session = Depends(get_db)
):
    if not short_url:
        raise HTTPException(status_code=400, detail="Short URL is required")

    url_record = db.query(URL).filter(URL.shortened_url == short_url).first()
    if not url_record:
        raise HTTPException(status_code=404, detail="URL not found in link history")

    return {"click_count": url_record.click_count}


@app.get("/{shortened_url}")
async def redirect_to_original(
    shortened_url: str, response: Response, db: Session = Depends(get_db)
):
    db_url = db.query(URL).filter(URL.shortened_url == shortened_url).first()
    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shortened URL not found"
        )

    original_url = db_url.original_url
    if db_url:
        db_url.click_count += 1
        return RedirectResponse(
            original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
    else:
        raise HTTPException(status_code=404, detail="URL not found")
