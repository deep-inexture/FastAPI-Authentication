from fastapi import FastAPI
from fastAPI_authentication import constants


def create_app():
    app = FastAPI(
        title='FastAPI Authentication Routes',
        description=constants.DESCRIPTION,
        version='1.0.0',
    )

    from fastAPI_authentication.authentications import authentication
    from fastAPI_authentication.users import user

    app.include_router(authentication.router)
    app.include_router(user.router)

    return app
