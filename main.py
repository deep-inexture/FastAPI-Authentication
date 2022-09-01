from fastAPI_authentication import models, create_app
from database import engine


models.Base.metadata.create_all(engine)

app = create_app()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
