def _check_requests():
    try:
        import requests
        return requests
    except ImportError:
        print("[!] Missing dependency: requests")
        print("    Install using: pip install requests")
        return None


SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",

    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Resource-Policy",
    "Clear-Site-Data",

    "X-XSS-Protection",
    "Expect-CT",
    "Public-Key-Pins",

    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Credentials",
    "Access-Control-Allow-Methods",
    "Access-Control-Allow-Headers",

    "X-Permitted-Cross-Domain-Policies",
    "X-DNS-Prefetch-Control",
    "Cache-Control",
    "Pragma",
]


def main(target: str) -> dict:
    result = {
        "status_code": None,
        "server": None,
        "security_headers": {}
    }

    if not target or not isinstance(target, str):
        return result

    requests = _check_requests()
    if not requests:
        return result

    if not target.startswith(("http://", "https://")):
        target = "http://" + target

    try:
        response = requests.get(
            target,
            timeout=10,
            allow_redirects=True
        )
    except requests.exceptions.RequestException:
        print("[!] No internet connection")
        return result

    result["status_code"] = response.status_code
    result["server"] = response.headers.get("Server")

    for header in SECURITY_HEADERS:
        value = response.headers.get(header)
        result["security_headers"][header] = {
            "present": value is not None,
            "value": value
        }

    return result
