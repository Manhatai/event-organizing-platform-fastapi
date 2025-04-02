import uvicorn
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.source.apps.api.controllers.building_controller import building_router
from backend.source.apps.api.controllers.category_controller import category_router
from backend.source.apps.api.controllers.event_controller import event_router
from backend.source.apps.api.controllers.region_controller import region_router
from backend.source.apps.api.controllers.reservation_controller import reservation_router
from backend.source.apps.api.controllers.stand_controller import stand_router
from backend.source.apps.api.security.login import user_login_router
from backend.source.apps.api.security.register import user_registration_router
from backend.source.infra.database.database_connection import engine
from backend.source.utils.unexpected_exception_handler.global_catch import register_exception_handlers


def get_session():
    with Session(engine) as session:
        yield session



SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(title="EventAppBackend")
register_exception_handlers(app)

app.include_router(user_login_router)
app.include_router(user_registration_router)
app.include_router(reservation_router, tags=["reservations"])
app.include_router(category_router, tags=["categories"])
app.include_router(region_router, tags=["regions"])
app.include_router(building_router, tags=["buildings"])
app.include_router(event_router, tags=["events"])
app.include_router(stand_router, tags=["stands"])

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile='./utils/certificates/key.pem',
        ssl_certfile='./utils/certificates/cert.pem',
    )

@app.get("/")
def health_check():
    return "Service is running."