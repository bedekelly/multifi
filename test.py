# coding: utf-8

from multifi import interface


with interface("en0") as session:
    print(session.get("http://example.com"))
