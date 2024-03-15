# from fastapi import FastAPI, Request, APIRouter
# from fastapi.middleware.cors import CORSMiddleware

# # from main import app
# from fastapi.templating import Jinja2Templates
# from utils import

# SHAMz = APIRouter()

# # app.include_router(router=SHAMz)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# templates = Jinja2Templates(directory="templates")


# @SHAMz.get("/")
# async def home(request: Request):

#     return templates.TemplateResponse(request, name="index.html")
