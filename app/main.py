from fastapi import FastAPI, HTTPException, Depends, Request, Response, status, Form
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import qrcode
from io import BytesIO
from starlette.responses import StreamingResponse
from utils import *
from schemas import *
from database import *
from models import *
import string
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# API_KEY = "supersecretapikey"
# API_KEY_NAME = "X-API-Key"
# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# api_key_header = APIKeyHeader(name=API_KEY_NAME)


def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = "".join(random.choice(characters) for _ in range(6))
    return short_url


@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(request, name="index.html")


@app.post("/login-user")
def login(user_login: LoginUser, db: Session = Depends(get_db)):
    user = db.query(USER).filter(USER.username == user_login.username).first()
    if user is None or user.password != user_login.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return {"message": "Login successful", "username": user.username}


@app.post("/shorten", response_class=HTMLResponse)
async def shorten_url(
    request: Request,
    response: Response,
    original_url: str = Form(),
    db: Session = Depends(get_db),
):
    short_url = generate_short_url()
    new_url = URL(shortened_url=short_url, original_url=original_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    response.headers["Location"] = f"/{short_url}"
    response.status_code = 201

    return templates.TemplateResponse(
        "index.html", {"request": request, "short_url": short_url}
    )


@app.get("/generate_qr", response_class=HTMLResponse)
async def generate_qr(request: Request, response: Response, url: str):

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes_io = BytesIO()
    img.save(img_bytes_io, format="PNG")
    img_bytes_io.seek(0)

    return templates.TemplateResponse("index.html", {"request": request, "qr": qr})


@app.get("/yuh")
def record_analytics(shortened_url: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.shortened_url == shortened_url).first()
    if db_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")

    db_url.click_count += 1
    db_url.last_accessed = datetime.datetime.utcnow()

    db.commit()


@app.get("/{shortened_url}")
async def redirect_to_original(
    shortened_url: str, response: Response, db: Session = Depends(get_db)
):
    db_url = db.query(URL).filter(URL.shortened_url == shortened_url).first()
    if not URL:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")

    record_analytics(shortened_url, db)

    original_url = db_url.original_url
    response.headers["/shorten"] = original_url
    response.status_code = status.HTTP_303_SEE_OTHER
    return {"original_url": original_url}


@app.get("/link-analytics")
async def get_link_analytics(short_url: str, db: Session = Depends(get_db)):
    # Fetch the URL record from the database
    url_record = db.query(URL).filter(URL.shortened_url == short_url).first()
    if not url_record:
        raise HTTPException(status_code=404, detail="URL not found in link history")

    return url_record


@app.get("/history/{user_id}")
async def get_user_link_history(user_id: str, db: Session = Depends(get_db)):
    new_id = id
    user_history = db.query(URL).filter(URL.id == new_id).all()
    if not user_history:
        raise HTTPException(status_code=404, detail="User history not found")
    return user_history
