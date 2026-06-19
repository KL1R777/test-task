import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import async_session_maker
from app.services.parser import parse_and_store
from app.services.scheduler import create_scheduler

logger = logging.getLogger(__name__)


async def _run_parse_job() -> None:
    """Фоновая задача парсинга вакансий."""
    try:
        async with async_session_maker() as session:
            await parse_and_store(session)
    except Exception as exc:
        logger.exception("Ошибка фонового парсинга: %s", exc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Тут настройка до запуска приложения
    """Управление жизненным циклом приложения."""
    
    logger.info("Запуск приложения")
    
    await _run_parse_job()
    
    scheduler = create_scheduler(_run_parse_job)
    scheduler.start()
    logger.info(
        "Планировщик запущен. Парсинг будет выполняться каждые %s минут",
        settings.parse_schedule_minutes
    )
    
    yield  # Приложение работает
    
    # Тут остановка приложения
    logger.info("Остановка приложения")
    scheduler.shutdown(wait=False)
    logger.info("Планировщик остановлен")


# создание app с lifespan
app = FastAPI(
    title="Selectel Vacancies API",
    lifespan=lifespan,
)

# это подключение роутера
app.include_router(api_router)

# логгирование
setup_logging()


