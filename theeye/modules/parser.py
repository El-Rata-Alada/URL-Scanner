from urllib.parse import urlparse
import re


# Try importing tldextract safely
# This library is used to split domain / subdomain / tld correctly
def _check_tldextract():
    try:
        import tldextract
        return tldextract
    except ImportError:
        # Clear error message for the user
        print("[!] Missing dependency: tldextract")
        print("    Install using: pip install tldextract")
        return None


# Check if the given value is an IPv4 address
def _is_ip(value: str) -> bool:
    ip_regex = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    return re.match(ip_regex, value) is not None


# Pretty-print the parsed URL data
# Each key-value pair is printed on a new line
def _pretty_print(result: dict):
    print()
    for key, value in result.items():
        print(f"[+] {key:<10}: {value}")
    print()


# Main parser logic
# Takes a URL / domain / IP as input
# Returns a dictionary with extracted components
def main(target: str) -> dict:
    # Default output structure
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

    # Validate input
    if not target or not isinstance(target, str):
        _pretty_print(result)
        return result

    # Add scheme if missing (required for urlparse)
    if not target.startswith(("http://", "https://")):
        target = "http://" + target

    # Parse the URL
    parsed = urlparse(target)

    # Extract basic URL components
    result["scheme"] = parsed.scheme
    result["path"] = parsed.path or "/"
    result["query"] = parsed.query or None
    result["fragment"] = parsed.fragment or None
    result["port"] = parsed.port

    # Extract hostname (domain or IP)
    hostname = parsed.hostname
    if not hostname:
        _pretty_print(result)
        return result

    # Check if hostname is an IP address
    result["is_ip"] = _is_ip(hostname)

    # If input is an IP, no need for tldextract
    if result["is_ip"]:
        result["domain"] = hostname
        _pretty_print(result)
        return result

    # Load tldextract for domain parsing
    tldextract = _check_tldextract()
    if not tldextract:
        _pretty_print(result)
        return result

    # Extract subdomain, domain, and TLD
    try:
        extracted = tldextract.extract(hostname)
    except Exception:
        print("[!] No internet connection")
        _pretty_print(result)
        return result

    # Populate extracted values
    result["domain"] = extracted.domain
    result["subdomain"] = extracted.subdomain or None
    result["tld"] = extracted.suffix or None

    # Print final output
    _pretty_print(result)
    return result
