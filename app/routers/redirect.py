"""Öffentliche Weiterleitung eines Kurzlinks mit Klick-Erfassung."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.database import get_session
from app.models import Click, Link

router = APIRouter(tags=["redirect"])


@router.get("/{code}")
def redirect(code: str, session: Session = Depends(get_session)) -> RedirectResponse:
    """Leitet öffentlich auf das Ziel weiter und zählt den Klick.

    `307` (Temporary Redirect) verhindert Browser-Caching und stellt so die
    korrekte Klickzählung sicher.
    """
    link = session.exec(select(Link).where(Link.code == code)).first()
    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Kurzlink nicht gefunden"
        )
    session.add(Click(link_id=link.id))
    session.commit()
    return RedirectResponse(
        url=link.target_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
