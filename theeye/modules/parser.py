from urllib.parse import urlparse, parse_qs
import tldextract


def _normalize_url(target: str) -> str:
    target = target.strip()
    if "://" not in target:
        target = "http://" + target
    return target


def main(target: str) -> dict:
    if not target or not isinstance(target, str):
        raise ValueError("Invalid target")

    normalized = _normalize_url(target)
    parsed = urlparse(normalized)

    host = parsed.hostname or ""

    ext = tldextract.extract(host)
    subdomain = ext.subdomain
    registered_domain = (
        f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
    )

    query_params = parse_qs(parsed.query)

    return {
        "input": target,
        "normalized_url": normalized,
        "scheme": parsed.scheme,
        "host": host,
        "subdomain": subdomain,
        "domain": registered_domain,
        "port": parsed.port,
        "path": parsed.path,
        "path_segments": [p for p in parsed.path.split("/") if p],
        "query_string": parsed.query,
        "query_params": query_params,
        "param_count": len(query_params),
        "fragment": parsed.fragment,
    }
