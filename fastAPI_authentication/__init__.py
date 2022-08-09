import config
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastAPI_authentication import exceptions, constants


@AuthJWT.load_config
def get_config():
    return config.Settings()


def create_app():
    app = FastAPI(
        title='FastAPI Authentication Routes',
        description=constants.DESCRIPTION,
        version='1.0.0',
        exception_handlers={AuthJWTException: exceptions.authjwt_exception_handler},
    )

    from fastAPI_authentication.authentications import authentication
    from fastAPI_authentication.users import user

    app.include_router(authentication.router)
    app.include_router(user.router)

    return app