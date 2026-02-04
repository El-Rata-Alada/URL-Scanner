import argparse

from theeye.modules import parser
from theeye.modules import headers
from theeye.modules import infra
from theeye.modules import fprint
from theeye.modules import content
from theeye.modules import report


def banner():
    print("""
████████╗██╗  ██╗███████╗             ███████╗██╗   ██╗███████╗
╚══██╔══╝██║  ██║██╔════╝             ██╔════╝╚██╗ ██╔╝██╔════╝
   ██║   ███████║█████╗               █████╗   ╚████╔╝ █████╗
   ██║   ██╔══██║██╔══╝               ██╔══╝    ╚██╔╝  ██╔══╝
   ██║   ██║  ██║███████╗             ███████╗   ██║   ███████╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝             ╚══════╝   ╚═╝   ╚══════╝
""")
    print("The Eye is watching 👁️\n")
    


def main():
    banner()

    argp = argparse.ArgumentParser(
        prog="theeye",
        description="Passive reconnaissance and security analysis tool"
    )

    sub = argp.add_subparsers(dest="command")

    sub.add_parser("parser").add_argument("target")
    sub.add_parser("headers").add_argument("target")
    sub.add_parser("infra").add_argument("target")
    sub.add_parser("fprint").add_argument("target")
    sub.add_parser("content").add_argument("target")
    sub.add_parser("full").add_argument("target")

    args = argp.parse_args()

    if not args.command:
        argp.print_help()
        return

    # -------- Dispatch --------
    if args.command == "parser":
        data = parser.main(args.target)
        print(data)

    elif args.command == "headers":
        data = headers.main(args.target)
        print(data)

    elif args.command == "infra":
        data = infra.main(args.target)
        print(data)

    elif args.command == "fprint":
        data = fprint.main(args.target)
        print(data)

    elif args.command == "content":
        data = content.main(args.target)
        print(data)

    elif args.command == "full":
        report_file = report.main(args.target)
        if report_file:
            print(f"\n[+] Report written to: {report_file}\n")


if __name__ == "__main__":
    main()
