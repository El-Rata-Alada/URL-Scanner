import socket
import ssl
import datetime


# ---------------- DEPENDENCY CHECKS ----------------

def _check_whois():
    try:
        import whois
        return whois
    except ImportError:
        print("[!] Missing dependency: python-whois")
        return None


def _check_dns():
    try:
        import dns.resolver
        return dns.resolver
    except ImportError:
        print("[!] Missing dependency: dnspython")
        return None


# ---------------- MAIN FUNCTION ----------------

def main(domain: str) -> dict:
    result = {
        "whois": {
            "registrar": None,
            "creation_date": None,
            "country": None,
            "domain_age_days": None
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
        },
        "flags": {
            "critical": [],
            "warning": [],
            "info": []
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

            # Domain age calculation
            if w.creation_date:
                if isinstance(w.creation_date, list):
                    created = w.creation_date[0]
                else:
                    created = w.creation_date

                age_days = (datetime.datetime.utcnow() - created.replace(tzinfo=None)).days
                result["whois"]["domain_age_days"] = age_days

                if age_days < 30:
                    result["flags"]["critical"].append("Domain age < 30 days")
                elif age_days < 180:
                    result["flags"]["warning"].append("Domain age < 180 days")

            if not w.registrar:
                result["flags"]["warning"].append("WHOIS registrar missing")

            if w.registrar and "privacy" in str(w.registrar).lower():
                result["flags"]["warning"].append("WHOIS privacy enabled")

        except Exception:
            result["flags"]["warning"].append("WHOIS lookup failed")

    # ---------------- DNS ----------------

    dns_resolver = _check_dns()
    if dns_resolver:
        for record_type in ["A", "AAAA", "MX", "NS", "TXT"]:
            try:
                answers = dns_resolver.resolve(domain, record_type)
                for rdata in answers:
                    result["dns"][record_type].append(str(rdata))
            except Exception:
                pass

    # SPF check
    spf_found = any("v=spf1" in txt.lower() for txt in result["dns"]["TXT"])
    if not spf_found:
        result["flags"]["critical"].append("SPF record missing")

    # DMARC check
    try:
        dmarc_answers = dns_resolver.resolve(f"_dmarc.{domain}", "TXT")
        dmarc_found = any("v=dmarc1" in str(r).lower() for r in dmarc_answers)
        if not dmarc_found:
            result["flags"]["warning"].append("DMARC record missing")
    except Exception:
        result["flags"]["warning"].append("DMARC record missing")

    # IPv6 info
    if not result["dns"]["AAAA"]:
        result["flags"]["info"].append("No IPv6 support")

    if len(result["dns"]["NS"]) <= 1:
        result["flags"]["warning"].append("Single or no nameserver detected")

    # ---------------- TLS / HTTPS ----------------

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

                expires = cert.get("notAfter")
                result["tls"]["certificate"]["expires"] = expires

    except Exception:
        result["flags"]["critical"].append("HTTPS not supported")

    # HTTPS + MX mismatch
    if result["dns"]["MX"] and not result["tls"]["https"]:
        result["flags"]["warning"].append("Email infra present but HTTPS disabled")

    return result
