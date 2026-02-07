import requests

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
    "Pragma"
]


def _analyze_headers(headers: dict) -> dict:
    flags = {
        "critical": [],
        "warning": [],
        "info": []
    }

    if not headers["Content-Security-Policy"]["present"]:
        flags["critical"].append("Missing Content-Security-Policy")

    if not headers["Strict-Transport-Security"]["present"]:
        flags["critical"].append("Missing HSTS")

    xfo = headers["X-Frame-Options"]
    if not xfo["present"]:
        flags["critical"].append("Missing X-Frame-Options")
    elif "ALLOW-FROM" in (xfo["value"] or ""):
        flags["warning"].append("X-Frame-Options uses deprecated ALLOW-FROM")

    if headers["Access-Control-Allow-Origin"]["value"] == "*":
        flags["warning"].append("CORS allows all origins (*)")

    if not headers["X-XSS-Protection"]["present"]:
        flags["info"].append("X-XSS-Protection not set (legacy)")

    if not headers["Cross-Origin-Opener-Policy"]["present"]:
        flags["info"].append("COOP not set")

    if not headers["Cross-Origin-Embedder-Policy"]["present"]:
        flags["info"].append("COEP not set")

    return flags


def main(url: str) -> dict:
    result = {
        "status_code": None,
        "server": None,
        "security_headers": {},
        "flags": {}
    }

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        r = requests.get(url, timeout=8, allow_redirects=True)
    except Exception:
        return result

    result["status_code"] = r.status_code
    result["server"] = r.headers.get("Server")

    for header in SECURITY_HEADERS:
        value = r.headers.get(header)
        result["security_headers"][header] = {
            "present": value is not None,
            "value": value
        }

    result["flags"] = _analyze_headers(result["security_headers"])

    return result
