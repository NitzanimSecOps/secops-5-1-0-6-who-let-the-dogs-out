"""selftest.py — run your router locally without a real network.

    python selftest.py          # run the example scenarios below
    VS Code: open this file, press F5 (Run and Debug), set breakpoints in host.py.

forward_packet opens a real socket via make_socket, which needs root + an interface. This
replaces make_socket with a recorder so process_packet runs anywhere. It builds IPv4 packets,
feeds them in, and prints what your router printed ([DELIVER]/[FORWARD]/[DROP]) and whether a
frame actually went out. Edit the scenarios at the bottom or call send() with your own packets.
"""
import struct

import host as host_module       # your solution's module
from host import Host
from routing import RouteEntry

ROUTER = ("10.0.0.1", "02:00:00:00:00:01")    # (ip, mac)
LAN_HOST = ("10.0.1.5", "02:00:00:00:00:05")  # a machine behind the router, via eth1

_SENT = []


class _FakeSock:
    def send(self, data):
        _SENT.append(data)
        return len(data)

    def close(self):
        pass


def _ip(ip):
    return bytes(int(o) for o in ip.split("."))


def ipv4(src, dst, ttl=64, payload=b"hello"):
    """Build a minimal IPv4 packet (20-byte header + payload)."""
    total_length = 20 + len(payload)
    header = struct.pack("!BBHHHBBH4s4s", 0x45, 0, total_length, 0, 0, ttl, 6, 0,
                         _ip(src), _ip(dst))
    return header + payload


def new_router():
    """A Host whose forwarding uses a fake socket, with one route + ARP entry set up."""
    host_module.make_socket = lambda interface: _FakeSock()   # no real NIC needed
    r = Host(*ROUTER)
    r.routing_table.add_route(RouteEntry("10.0.1.0", "255.255.255.0", None, "eth1"))
    r.arp_table.learn(LAN_HOST[0], LAN_HOST[1])
    return r


def send(r, packet, label=""):
    """Feed one packet into the router, and show what happened."""
    _SENT.clear()
    print(f"\n>>> {label or 'send'}")
    r.process_packet(packet)                               # <-- your code runs here; breakpoint it
    print(f"    {'a frame was forwarded' if _SENT else 'nothing forwarded (delivered or dropped)'}")


if __name__ == "__main__":
    r = new_router()

    send(r, ipv4("10.0.2.2", LAN_HOST[0]), "transit packet -> should FORWARD out eth1")
    send(r, ipv4("10.0.2.2", ROUTER[0]), "packet addressed to the router -> should DELIVER")
    send(r, ipv4("10.0.2.2", "9.9.9.9"), "packet with no matching route -> should DROP")

    print("\nExpected: #1 prints [FORWARD] and sends; #2 prints [DELIVER]; #3 prints [DROP];")
    print("only #1 forwards a frame. Edit the scenarios, or call send(r, ipv4(src, dst), 'label').")
