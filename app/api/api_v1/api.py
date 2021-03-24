from fastapi import APIRouter

from app.api.api_v1.endpoints import series, login, users, utils, episode, episode_image

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(series.router, prefix="/series", tags=["series"])
api_router.include_router(episode.router, prefix="/episode", tags=["episode"])
api_router.include_router(episode_image.router, prefix="/episode_image", tags=["episode image"])
