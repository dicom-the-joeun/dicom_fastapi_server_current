from fastapi import Depends, FastAPI
# CORS 설정
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from app.router import router


from app.conf.config import get_config

metadata = get_config()['DEFAULT']

app = FastAPI(
    title=metadata.get('title'),
    version=metadata.get('version'),
    contact={
        'name': metadata.get('name'),
        'email': metadata.get('email')
    },
    license_info={
        'name': metadata.get('license_name'),
        'url': metadata.get('license_url')
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router.router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run()
