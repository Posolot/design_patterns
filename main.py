from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn
from Src.Core.responce_format import response_formats
from Src.Logics.factory_entities import facrtory_entities
from Src.reposity import reposity
from Src.start_service import start_service
from Src.settings_manager import settings_manager


# === Инициализация зависимостей ===
settings_file = "Docs/test_rest.json"
start_service = start_service()
settings_manager = settings_manager()
factory = facrtory_entities()

# === Создание приложения FastAPI ===
app = FastAPI(title="REST API", description="Converted from Connexion/Flask to FastAPI")


# === Проверка доступности API ===
@app.get("/api/status")
async def status():
    """Проверить доступность REST API"""
    return {"status": "success"}


# === Список доступных форматов ответов ===
@app.get("/api/responses/formats")
async def get_response_formats():
    """Доступные форматы ответов"""
    types = response_formats.answers_types()
    return [t.lower() for t in dict.fromkeys(types)]


# === Список типов моделей, доступных для формирования ответов ===
@app.get("/api/responses/models")
async def get_response_models():
    """Типы моделей, доступные для формирования ответов"""
    return list(reposity.keys())


# === Сформировать ответ для указанной модели и формата ===
@app.get("/api/responses/build")
async def build_response(
        format: str = Query(..., description="Формат ответа (csv, json, excel, markdown)"),
        model: str = Query(..., description="Имя модели для формирования ответа"),
):
    """Сформировать ответ для моделей (model) в переданном формате (format)"""
    format = format.lower()

    available_formats = [t.lower() for t in response_formats.answers_types()]
    available_models = list(start_service._repo.keys())

    # Проверка формата
    if format not in available_formats:
        return JSONResponse(
            status_code=400,
            content={
                "error": f"not such format '{format}'. Available: {available_formats}"
            },
        )

    # Проверка модели
    if model not in available_models:
        return JSONResponse(
            status_code=400,
            content={
                "error": f"not such model '{model}'. Available: {available_models}"
            },
        )

    # Получение данных модели
    models = start_service.get_models(model)

    # Формирование результата через фабрику
    result = factory.create(format).build(models)
    return {"result": result}


# === Запуск приложения ===
def start():
    """Точка входа при запуске"""
    start_service.load_from_file(settings_file)
    settings_manager._file_name = settings_file
    settings_manager.load()
    uvicorn.run(app, host="localhost", port=8080)


if __name__ == "__main__":
    start()
