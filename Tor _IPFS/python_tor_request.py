import requests


def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

# Make a request through the Tor connection
# IP visible through Tor

session = get_tor_session()
print(session.get("http://httpbin.org/ip").text)
# Above should print an IP different than your public IP

# Following prints your normal public IP
print(requests.get("http://httpbin.org/ip").text)
#print(requests.get("http://127.0.0.1:5001/get_chain").text)
#print(session.get("http://ec2-43-206-122-178.ap-northeast-1.compute.amazonaws.com:5001/get_chain").text)
#url request:-
#print(requests.get("https://ohyicong.medium.com/how-to-create-tor-proxy-with-python-cheat-sheet-101-3d2d619a1d39").text)


from stem import Signal
from stem.control import Controller

# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="Trial@1234")
        controller.signal(Signal.NEWNYM)

renew_connection()
session = get_tor_session()
print(session.get("http://httpbin.org/ip").text)