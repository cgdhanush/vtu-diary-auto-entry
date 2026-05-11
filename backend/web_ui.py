from pathlib import Path

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from starlette.responses import FileResponse


router_ui = APIRouter()


@router_ui.get("/{rest_of_path:path}", include_in_schema=False)
async def index_html(rest_of_path: str):
    """
    Emulate path fallback to index.html.
    """
    if rest_of_path.startswith("api") or rest_of_path.startswith("."):
        raise HTTPException(status_code=404, detail="Not Found")

    BASE_DIR = Path(__file__).resolve().parents[1]
    uibase = BASE_DIR / "frontend" / "dist"

    filename = uibase / rest_of_path

    media_type: str | None = None
    if filename.suffix == ".js":
        media_type = "application/javascript"
    if filename.is_file() and filename.is_relative_to(uibase):
        return FileResponse(str(filename), media_type=media_type)

    index_file = uibase / "index.html"

    return FileResponse(str(index_file))
