import re


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
        "cms": None,
        "frameworks": [],
        "javascript": [],
        "cloud": None
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
        return result

    headers = response.headers

    # ---------------- HEADER-BASED DETECTION ----------------

    if headers.get("Server"):
        result["web_server"] = headers.get("Server")

    for header in ["X-Powered-By", "X-Generator"]:
        if headers.get(header):
            result["technologies"].append(headers.get(header))

    # Framework hints
    framework_headers = {
        "X-AspNet-Version": "ASP.NET",
        "X-Django-Version": "Django",
        "X-Runtime": "Ruby on Rails",
        "X-Powered-By-Plesk": "Plesk"
    }

    for h, name in framework_headers.items():
        if headers.get(h):
            result["frameworks"].append(name)

    # Cloud / CDN detection
    if headers.get("CF-RAY"):
        result["cloud"] = "Cloudflare"
    elif headers.get("X-Amz-Cf-Id"):
        result["cloud"] = "AWS CloudFront"
    elif headers.get("X-Azure-Ref"):
        result["cloud"] = "Azure"

    # ---------------- HTML-BASED DETECTION ----------------

    try:
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception:
        return result

    # Meta generator
    meta_gen = soup.find("meta", attrs={"name": "generator"})
    if meta_gen and meta_gen.get("content"):
        gen = meta_gen["content"]
        result["technologies"].append(gen)

        gl = gen.lower()
        if "wordpress" in gl:
            result["cms"] = "WordPress"
        elif "joomla" in gl:
            result["cms"] = "Joomla"
        elif "drupal" in gl:
            result["cms"] = "Drupal"

    # CMS fingerprints
    html = response.text.lower()

    if "/wp-content/" in html or "/wp-includes/" in html:
        result["cms"] = "WordPress"

    if "/sites/default/" in html:
        result["cms"] = "Drupal"

    if "content=\"joomla" in html:
        result["cms"] = "Joomla"

    # JavaScript libraries
    scripts = soup.find_all("script", src=True)
    for s in scripts:
        src = s["src"].lower()
        if "jquery" in src:
            result["javascript"].append("jQuery")
        elif "react" in src:
            result["javascript"].append("React")
        elif "vue" in src:
            result["javascript"].append("Vue.js")
        elif "angular" in src:
            result["javascript"].append("Angular")

    # Deduplicate lists
    result["technologies"] = list(set(result["technologies"]))
    result["frameworks"] = list(set(result["frameworks"]))
    result["javascript"] = list(set(result["javascript"]))

    return result
