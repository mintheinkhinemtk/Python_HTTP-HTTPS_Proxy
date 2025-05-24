# Python_HTTP-HTTPS_Proxy
HTTP/HTTPS Relay Proxy Server written in Python using sockets

##Features
- Support HTTP and HTTPS (via tunneling with CONNECT method)
- Relays traffic without decrypting HTTPS (no MITM or CA certificate)
- Handles multiple clients using multithreading

## Files

### `proxy.py`
Main file that runs the HTTP/HTTPS proxy server.

## Usage
1. Run `proxy.py` to start the proxy server.
2. Set your browser or system proxy settings to the proxy server's **IP address and port**.
3. Browse normally. HTTP and HTTPS requests will be relayed through your proxy.

Note: Since this is a **relay proxy**, it **cannot intercept or view HTTPS traffic**. This proxy does not generate or install a certificate authority (CA).


### `talking_with_telnet.py`
A lightweight script for interacting with Telnet. Designed just for fun, focusing on avoiding echoing the user's input when typing.

## Disclaimer

This project is intended for educational and testing purposes only.
