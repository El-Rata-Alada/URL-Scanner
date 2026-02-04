import socket
import ssl


def _check_whois():
    try:
        import whois
        return whois
    except ImportError:
        print("[!] Missing dependency: python-whois")
        print("    Install using: pip install python-whois")
        return None


def _check_dns():
    try:
        import dns.resolver
        return dns.resolver
    except ImportError:
        print("[!] Missing dependency: dnspython")
        print("    Install using: pip install dnspython")
        return None


def main(domain: str) -> dict:
    result = {
        "whois": {
            "registrar": None,
            "creation_date": None,
            "country": None
        },
        "dns": {
            "A": [],
            "AAAA": [],
            "MX": [],
            "NS": [],
            "TXT": []
        },
        "tls": {
            "https": False,
            "tls_version": None,
            "certificate": {
                "issuer": None,
                "expires": None
            }
        }
    }

    if not domain or not isinstance(domain, str):
        return result

    # ---------------- WHOIS ----------------
    whois_lib = _check_whois()
    if whois_lib:
        try:
            w = whois_lib.whois(domain)
            result["whois"]["registrar"] = w.registrar
            result["whois"]["creation_date"] = w.creation_date
            result["whois"]["country"] = w.country
        except Exception:
            print("[!] No internet connection (WHOIS)")

    # ---------------- DNS ----------------
    dns_resolver = _check_dns()
    if dns_resolver:
        try:
            for record_type in ["A", "AAAA", "MX", "NS", "TXT"]:
                try:
                    answers = dns_resolver.resolve(domain, record_type)
                    for rdata in answers:
                        result["dns"][record_type].append(str(rdata))
                except Exception:
                    pass
        except Exception:
            print("[!] No internet connection (DNS)")

    # ---------------- TLS ----------------
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                result["tls"]["https"] = True
                result["tls"]["tls_version"] = ssock.version()

                issuer = cert.get("issuer")
                if issuer:
                    result["tls"]["certificate"]["issuer"] = issuer[0][0][1]

                result["tls"]["certificate"]["expires"] = cert.get("notAfter")
    except Exception:
        pass

    return result
