"""
FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from src.api.routes import products, content, links, analytics
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Cria app FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API para automação de operação de afiliados Shopee"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui routers
app.include_router(products.router, prefix="/api/products", tags=["Produtos"])
app.include_router(content.router, prefix="/api/content", tags=["Conteúdo"])
app.include_router(links.router, prefix="/api/links", tags=["Links"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])


@app.on_event("startup")
async def startup_event():
    """Evento de inicialização"""
    logger.info(f"{settings.APP_NAME} v{settings.VERSION} iniciando...")
    
    # Inicializa banco de dados
    from src.database.connection import init_db
    init_db()
    
    logger.info("Banco de dados inicializado")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento de encerramento"""
    logger.info("Aplicação encerrando...")


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    from config.credentials import credentials
    
    is_valid, missing = credentials.validate()
    
    return {
        "status": "healthy" if is_valid else "degraded",
        "credentials_configured": is_valid,
        "missing_credentials": missing if not is_valid else []
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
