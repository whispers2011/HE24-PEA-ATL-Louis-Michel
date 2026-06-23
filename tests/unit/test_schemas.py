import pytest
from pydantic import ValidationError

from app.schemas import LinkCreate


def test_linkcreate_accepts_https_url():
    data = LinkCreate(target_url="https://example.com/path")
    assert str(data.target_url).startswith("https://example.com")


def test_linkcreate_accepts_http_url():
    data = LinkCreate(target_url="http://example.com")
    assert str(data.target_url).startswith("http://example.com")


@pytest.mark.parametrize(
    "url",
    ["ftp://example.com", "not-a-url", "javascript:alert(1)"],
)
def test_linkcreate_rejects_non_http_schemes(url: str):
    with pytest.raises(ValidationError):
        LinkCreate(target_url=url)
