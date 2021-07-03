from fastapi import APIRouter

from app.api.api_v1.endpoints import cash, series, login, users, utils, episodes, episode_images, payments

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(series.router, prefix="/series", tags=["series"])
api_router.include_router(episodes.router, prefix="/episodes", tags=["episodes"])
api_router.include_router(episode_images.router,
                          prefix="/episode_images", tags=["episode images"])
api_router.include_router(cash.router, prefix="/cash", tags=["cash"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
