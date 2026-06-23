"""Owner-scoped CRUD-Endpunkte für Kurzlinks."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.config import settings
from app.database import get_session
from app.models import Link, User
from app.schemas import LinkCreate, LinkRead
from app.security import get_current_user
from app.services import shortcode

router = APIRouter(prefix="/api/links", tags=["links"])


def _to_read(link: Link) -> LinkRead:
    """Wandelt einen Link in seine Ausgabe inkl. vollständiger Kurz-URL."""
    return LinkRead(
        code=link.code,
        target_url=link.target_url,
        short_url=f"{settings.base_url}/{link.code}",
        created_at=link.created_at,
    )


def _get_owned_link(code: str, session: Session, user: User) -> Link:
    """Lädt einen eigenen Kurzlink; `404` unbekannt, `403` fremd."""
    link = session.exec(select(Link).where(Link.code == code)).first()
    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Kurzlink nicht gefunden"
        )
    if link.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kein Zugriff auf fremde Kurzlinks",
        )
    return link


@router.post("", response_model=LinkRead, status_code=status.HTTP_201_CREATED)
def create_link(
    data: LinkCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> LinkRead:
    """Legt einen Kurzlink an; optional mit validiertem Wunsch-Alias."""
    if data.alias is not None:
        if not shortcode.is_valid_alias(data.alias):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Ungültiger Alias"
            )
        if shortcode.code_exists(session, data.alias):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Alias bereits vergeben"
            )
        code = data.alias
    else:
        code = shortcode.generate_unique_code(session)
    link = Link(code=code, target_url=str(data.target_url), owner_id=user.id)
    session.add(link)
    session.commit()
    session.refresh(link)
    return _to_read(link)


@router.get("", response_model=list[LinkRead])
def list_links(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[LinkRead]:
    """Listet alle Kurzlinks des aktuellen Benutzers."""
    links = session.exec(select(Link).where(Link.owner_id == user.id)).all()
    return [_to_read(link) for link in links]


@router.get("/{code}", response_model=LinkRead)
def get_link(
    code: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> LinkRead:
    """Liefert einen eigenen Kurzlink."""
    return _to_read(_get_owned_link(code, session, user))


@router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(
    code: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> None:
    """Löscht einen eigenen Kurzlink samt seiner Klicks."""
    link = _get_owned_link(code, session, user)
    session.delete(link)
    session.commit()
