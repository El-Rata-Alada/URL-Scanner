def _check_requests():
    try:
        import requests
        return requests
    except ImportError:
        print("[!] Missing dependency: requests")
        print("    Install using: pip install requests")
        return None


def _check_bs4():
    try:
        from bs4 import BeautifulSoup
        return BeautifulSoup
    except ImportError:
        print("[!] Missing dependency: beautifulsoup4")
        print("    Install using: pip install beautifulsoup4")
        return None


def main(url: str) -> dict:
    result = {
        "web_server": None,
        "technologies": [],
        "cms": None
    }

    if not url or not isinstance(url, str):
        return result

    requests = _check_requests()
    BeautifulSoup = _check_bs4()
    if not requests or not BeautifulSoup:
        return result

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException:
        print("[!] No internet connection")
        return result

    headers = response.headers

    # -------- Header-based detection --------
    server = headers.get("Server")
    if server:
        result["web_server"] = server

    powered = headers.get("X-Powered-By")
    if powered:
        result["technologies"].append(powered)

    generator = headers.get("X-Generator")
    if generator:
        result["technologies"].append(generator)

    # -------- HTML-based detection --------
    try:
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception:
        return result

    meta_gen = soup.find("meta", attrs={"name": "generator"})
    if meta_gen and meta_gen.get("content"):
        gen = meta_gen["content"]
        result["technologies"].append(gen)

        g = gen.lower()
        if "wordpress" in g:
            result["cms"] = "WordPress"
        elif "joomla" in g:
            result["cms"] = "Joomla"
        elif "drupal" in g:
            result["cms"] = "Drupal"

    return result
