import base64
import hmac
import struct
import sys
import time
from urllib import parse
import typing


def hotp(key, counter, digits:int=6, digest='sha1'):
    key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', counter)
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].zfill(digits)

def totp(key, time_step:int=30, digits:int=6, digest='sha1',use_time:typing.Optional[float]=None) -> tuple[int,str]:
    """ returns remainingValidTime in secounds & Token """
    use_time = time.time() if use_time is None else use_time
    return (int(time_step - int(use_time % time_step)), \
                hotp(key, int(use_time / time_step), digits, digest))

def fromUrl(urlString:str, use_time:typing.Optional[float]=None) -> tuple[int,int,str]:
    """returns total validTime in secounds, remainingValidTime in seconds & Token """
    params = dict(parse.parse_qsl(parse.urlsplit((urlString)).query))
    alg = params.get('algorithm','sha1')
    period = int(params.get('period', 30))
    digits = int(params.get('digits', 6))
    #print(params)
    res = totp(params['secret'], period, digits, alg, use_time)
    return (period, res[0], res[1])