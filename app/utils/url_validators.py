from urllib.parse import urlparse


def url_eh_sefaz(url: str) -> bool:
    try:
        parsed = urlparse(url)

        return "sefaz" in parsed.netloc

    except Exception:
        return False
