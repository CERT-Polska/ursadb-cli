import argparse
import json
import sys
import zmq
from .terminal import setup_terminal
from tabulate import tabulate

setup_terminal()

ANSI = {"RED": "\x1b[31m", "GREEN": "\x1b[32m", "RESET": "\x1b[39m"}

parser = argparse.ArgumentParser(description="Communicate with UrsaDB.")
parser.add_argument("db_url", nargs="?", default="tcp://localhost:9281")
parser.add_argument(
    "--cmd",
    nargs="?",
    help="execute provided command, print results and terminate",
)

args = parser.parse_args()

context = zmq.Context()

if not args.cmd:
    print("[ ] Connecting: {}".format(args.db_url))

socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.LINGER, 0)
socket.setsockopt(zmq.RCVTIMEO, 1000)
socket.connect(args.db_url)

socket.send_string("ping;")

while True:
    try:
        socket.recv()
    except zmq.error.Again as e:
        print(
            "{}[!] Connection failed: {}{}".format(
                ANSI["RED"], str(e), ANSI["RESET"]
            )
        )
    else:
        break


progress_socket = context.socket(zmq.REQ)
progress_socket.connect(args.db_url)


if not args.cmd:
    print("{}[+] Connected{}".format(ANSI["GREEN"], ANSI["RESET"]))


def print_progress_bars():
    progress_socket.send_string("status;")
    result = json.loads(progress_socket.recv())
    tasks = [
        task
        for task in result.get("result", {}).get("tasks", [])
        if task.get("work_done") < task.get("work_estimated")
    ]

    for task in tasks:
        frac = float(task["work_done"]) / task["work_estimated"]
        bar = "#" * int(20 * frac)
        bar = bar + (20 - len(bar)) * "."
        print("task {:4} {:3.2f}% [{}]".format(task["id"], frac * 100, bar))


def do_query(query):
    if not query.endswith(";"):
        query += ";"
    socket.send_string(query)
    while True:
        try:
            res = json.loads(socket.recv())
            return res
        except Exception:
            print_progress_bars()


def main():
    while True:
        if args.cmd:
            query = args.cmd
        else:
            sys.stdout.write("> ")
            sys.stdout.flush()
            query = sys.stdin.readline()
            if not query:
                break
            query = query.strip()

        res = do_query(query)

        if "error" in res:
            print(
                "{}ERR {}{}".format(
                    ANSI["RED"],
                    res.get("error").get("message", "(no error provided)"),
                    ANSI["RESET"],
                )
            )
        else:
            if res.get("type") == "topology":
                data = []

                for k, v in res["result"]["datasets"].items():
                    indexes = ", ".join(
                        sorted([ndx["type"] for ndx in v["indexes"]])
                    )
                    data.append([k, indexes])

                print(tabulate(data, ("dataset", "indexes"), tablefmt="psql"))
            elif res.get("type") == "status":
                data = []

                for v in res["result"]["tasks"]:
                    data.append(
                        [
                            v["id"],
                            v["connection_id"],
                            v["epoch_ms"],
                            v["work_done"],
                            v["work_estimated"],
                            v["request"],
                        ]
                    )

                print(
                    tabulate(
                        data,
                        (
                            "id",
                            "conn id",
                            "epoch ms",
                            "work done",
                            "work estimated",
                            "request",
                        ),
                        tablefmt="psql",
                    )
                )
            elif res.get("type") == "select":
                for fname in res.get("result", {}).get("files", []):
                    print(fname)
            elif res.get("type") in "ok":
                print("{}OK{}".format(ANSI["GREEN"], ANSI["RESET"]))
            else:
                print("{}OK: {}{}".format(ANSI["GREEN"], res, ANSI["RESET"]))

        if args.cmd:
            break


if __name__ == "__main__":
    main()
