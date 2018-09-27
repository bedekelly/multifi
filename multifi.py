# coding=utf-8

import requests
from contextlib import contextmanager
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

_interface_ip = {
    "eth0": '192.168.43.92'
}


class _SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        self.poolmanager = None
        super(SourceAddressAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **kwargs):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       source_address=self.source_address)


@contextmanager
def interface(iface_name):
    ip = _interface_ip[iface_name]
    port = 8080
    session = requests.Session()
    adapter = _SourceAddressAdapter((ip, port))
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    yield session


__all__ = ["interface"]
