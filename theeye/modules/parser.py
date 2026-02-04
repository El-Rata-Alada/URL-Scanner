import sys
import urllib.parse


def _check_dependency():
    try:
        import tldextract  # noqa: F401
        return True
    except ImportError:
        print("[!] Missing dependency: tldextract")
        print("[+] Install it using:")
        print("    pip install tldextract")
        return False


def parse_url(url: str) -> dict:
    import tldextract

    parsed = urllib.parse.urlparse(url)
    extracted = tldextract.extract(url)

    return {
        "scheme": parsed.scheme or None,
        "host": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path or "/",
        "query": parsed.query or None,
        "fragment": parsed.fragment or None,
        "subdomain": extracted.subdomain or None,
        "domain": extracted.domain or None,
        "suffix": extracted.suffix or None,
        "registered_domain": extracted.registered_domain or None,
    }


def main():
    if not _check_dependency():
        return 0

    if len(sys.argv) < 2:
        print("[!] Usage: theeye <url>")
        return 0

    url = sys.argv[1]

    try:
        result = parse_url(url)
    except Exception as e:
        print(f"[!] Failed to parse URL: {e}")
        return 0

    print("\n[+] URL Parsing Result\n" + "-" * 25)
    for key, value in result.items():
        print(f"{key:<20}: {value}")

    return 0
