import socket

from wilde.plugins.whois.client.WhoisClient import WhoisClient


class DefaultWhoisClient(WhoisClient):
    def get_whois_info(self, domain: str, server: str = "whois.iana.org") -> str:
        with socket.create_connection((server, 43)) as sock:
            sock.sendall(f"{domain}\r\n".encode("idna"))

            chunks = b''
            while chunk := sock.recv(4096):
                chunks += chunk

            return chunks.decode()
