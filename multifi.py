# coding=utf-8

import requests
import subprocess
import re
import sys

from contextlib import contextmanager
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


def ip_for(interface_name):
    """
    Retrieve this machine's IP address on a given interface.
    """
    output_bytes = subprocess.check_output(["ifconfig", interface_name])
    output = output_bytes.decode(sys.stdout.encoding)
    match = re.search("inet (\d*?\.\d*?\.\d*?\.\d*)", output)
    return match.group(1)


class _SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        self.poolmanager = None
        super(_SourceAddressAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **kwargs):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       source_address=self.source_address)


@contextmanager
def interface(iface_name):
    """
    Returns a Requests session, which will send all traffic through the
    given interface. This is expressed as a context manager so the session
    is closed after use.
    """
    ip = ip_for(iface_name)
    port = 0
    session = requests.Session()
    adapter = _SourceAddressAdapter((ip, port))
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    yield session
    session.close()


__all__ = ["interface"]
