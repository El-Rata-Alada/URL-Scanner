from datetime import datetime

from theeye.modules import parser
from theeye.modules import headers
from theeye.modules import infra
from theeye.modules import fprint
from theeye.modules import content


def _safe_call(func, target):
    try:
        return func(target)
    except Exception:
        return {}


def _write_section(f, title, data, indent=0):
    pad = " " * indent
    f.write(f"\n{pad}{title}\n")
    f.write(f"{pad}{'-' * len(title)}\n")

    if not data:
        f.write(f"{pad}No data available\n")
        return

    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                f.write(f"\n{pad}{k}:\n")
                for sk, sv in v.items():
                    f.write(f"{pad}  {sk}: {sv}\n")
            else:
                f.write(f"{pad}{k}: {v}\n")
    elif isinstance(data, list):
        for item in data:
            f.write(f"{pad}- {item}\n")
    else:
        f.write(f"{pad}{data}\n")


def main(target: str) -> str:
    if not target or not isinstance(target, str):
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_name = target.replace("://", "_").replace("/", "_")
    report_name = f"report_{safe_name}.txt"

    # -------- Run modules --------
    parsed = _safe_call(parser.main, target)
    headers_data = _safe_call(headers.main, target)

    domain = parsed.get("domain") if parsed else None
    infra_data = _safe_call(infra.main, domain) if domain else {}

    #tech_data = _safe_call(tech.main, target
    content_data = _safe_call(content.main, target)

    # -------- Write report --------
    with open(report_name, "w", encoding="utf-8") as f:
        f.write("THEEYE – FULL SCAN REPORT\n")
        f.write("=========================\n")
        f.write(f"Target     : {target}\n")
        f.write(f"Generated  : {timestamp}\n")

        _write_section(f, "Parsed Target", parsed_data)
        _write_section(f, "HTTP & Security Headers", headers_data)
        _write_section(f, "Infrastructure Intelligence", infra_data)
        _write_section(f, "Technology Fingerprinting", tech_data)
        _write_section(f, "Content Analysis", content_data)

        f.write("\n\n[ End of Report ]\n")

    return report_name
