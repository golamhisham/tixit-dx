from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes import auth, project, issue, comment, notifications
from app.database import engine
from app.models import user

# Create database tables
user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tixit DX API", version="1.0.0")

# Add this function to customize OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(project.router, tags=["projects"])
app.include_router(issue.router, tags=["issues"])
app.include_router(comment.router, tags=["comments"])
app.include_router(notifications.router, tags=["notifications"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 