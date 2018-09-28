# MultiFi

### Send `requests` through a specified network interface

This is a small utility to send HTTP requests through different network interfaces, using the Python `requests` module.

## Usage:

```python
with interface("eth0") as session:
    session.get("https://bede.io")
```


## Requirements:

* Already set up/connected two WiFi adapters (one can be internal)
* `ifconfig` available on the command line
* Only tested on MacOS but should work anywhere.

## Notes:

The tricky bit on other operating systems is to connect two WiFi adapters to
separate WiFi networks – on MacOS this is possible out of the box but this
may not be true on *nix or Windows machines.

The way this works is to find the machine's IP address on the given
interface, then return a Requests session which is bound to that IP
address. I'm pretty sure this will break if the machine has the
same IP address on both networks, but that's pretty unlikely for small
home networks. 