from urllib.parse import urlparse
import re

def _check_tldextract():
    try:
        import tldextract
        return tldextract
    except ImportError:
        print("[!] Missing dependency: tldextract")
        print("    Install using: pip install tldextract")
        return None


def _is_ip(value: str) -> bool:
    ip_regex = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    return re.match(ip_regex, value) is not None


def main(target: str) -> dict:
    result = {
        "scheme": None,
        "domain": None,
        "subdomain": None,
        "tld": None,
        "port": None,
        "path": None,
        "query": None,
        "fragment": None,
        "is_ip": False
    }

    if not target or not isinstance(target, str):
        return result

    if not target.startswith(("http://", "https://")):
        target = "http://" + target

    parsed = urlparse(target)

    result["scheme"] = parsed.scheme
    result["path"] = parsed.path or "/"
    result["query"] = parsed.query
    result["fragment"] = parsed.fragment
    result["port"] = parsed.port

    hostname = parsed.hostname
    if not hostname:
        return result

    result["is_ip"] = _is_ip(hostname)

    if result["is_ip"]:
        result["domain"] = hostname
        return result

    tldextract = _check_tldextract()
    if not tldextract:
        return result

    try:
        extracted = tldextract.extract(hostname)
    except Exception:
        print("[!] No internet connection")
        return result

    result["domain"] = extracted.domain
    result["subdomain"] = extracted.subdomain or None
    result["tld"] = extracted.suffix or None

    return result
