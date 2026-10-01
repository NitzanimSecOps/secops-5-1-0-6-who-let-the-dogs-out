import socket
import struct

from arp import ARPTable
from ipv4 import IPv4Packet
from routing import RoutingTable

# Copy into this repo: ipv4.py (5.1.0.1), routing.py (5.1.0.3), arp.py (5.1.0.4).


def make_socket(interface: str) -> socket.socket:
    pass  # paste make_socket from 4.1.0.2


class Host:
    def __init__(self, ip: str, mac: str):
        pass  # paste your Host.__init__ from 5.1.0.5

    def drop_packet(self, message: str = "") -> None:
        print(f"[DROP] {message}")

    def deliver_packet(self, payload: bytes) -> None:
        print(f"[DELIVER] Packet reached its final destination. Payload: {payload}")

    def forward_packet(self, raw_bytes: bytes, next_mac: str, interface: str) -> None:
        print(f"[FORWARD] Sending out via {interface} to MAC {next_mac}")
        pass # TODO: wrap raw_bytes in an Ethernet frame and send it out of `interface`

    def process_packet(self, raw_bytes: bytes) -> None:
        pass  # paste your process_packet from 5.1.0.5
