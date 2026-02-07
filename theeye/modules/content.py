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
        from bs4 import BeautifulSoup, Comment
        return BeautifulSoup, Comment
    except ImportError:
        print("[!] Missing dependency: beautifulsoup4")
        print("    Install using: pip install beautifulsoup4")
        return None, None


def main(url: str) -> dict:
    result = {
        "title": None,
        "meta_description": None,
        "forms_count": 0,
        "input_types": [],
        "password_fields": False,
        "file_uploads": False,
        "external_forms": False,
        "html_comments": False,
        "scripts_count": 0,
        "iframes_count": 0
    }

    if not url or not isinstance(url, str):
        return result

    requests = _check_requests()
    BeautifulSoup, Comment = _check_bs4()
    if not requests or not BeautifulSoup:
        return result

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException:
        return result

    try:
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception:
        return result

    # -------- Title --------
    if soup.title and soup.title.string:
        result["title"] = soup.title.string.strip()

    # -------- Meta Description --------
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        result["meta_description"] = meta_desc["content"].strip()

    # -------- Forms --------
    forms = soup.find_all("form")
    result["forms_count"] = len(forms)

    input_types = set()
    for form in forms:
        action = form.get("action", "")
        if action.startswith("http") and url.split("/")[2] not in action:
            result["external_forms"] = True

        inputs = form.find_all("input")
        for inp in inputs:
            t = inp.get("type", "text").lower()
            input_types.add(t)

            if t == "password":
                result["password_fields"] = True
            if t == "file":
                result["file_uploads"] = True

    result["input_types"] = sorted(input_types)

    # -------- Scripts --------
    scripts = soup.find_all("script")
    result["scripts_count"] = len(scripts)

    # -------- Iframes --------
    iframes = soup.find_all("iframe")
    result["iframes_count"] = len(iframes)

    # -------- HTML Comments --------
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    if comments:
        result["html_comments"] = True

    return result
