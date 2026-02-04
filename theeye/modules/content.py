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
        "title": None,
        "forms_count": 0,
        "input_types": [],
        "html_comments": False
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

    try:
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception:
        return result

    # -------- Title --------
    if soup.title and soup.title.string:
        result["title"] = soup.title.string.strip()

    # -------- Forms --------
    forms = soup.find_all("form")
    result["forms_count"] = len(forms)

    # -------- Inputs --------
    input_types = set()
    for form in forms:
        inputs = form.find_all("input")
        for inp in inputs:
            t = inp.get("type", "text")
            input_types.add(t.lower())

    result["input_types"] = sorted(list(input_types))

    # -------- HTML Comments --------
    from bs4 import Comment
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    if comments:
        result["html_comments"] = True

    return result
