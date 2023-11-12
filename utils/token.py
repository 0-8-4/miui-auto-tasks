import random
import time
import asyncio
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.backends import default_backend
import base64

from .request import get, post

public_key_pem = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArxfNLkuAQ/BYHzkzVwtu
g+0abmYRBVCEScSzGxJIOsfxVzcuqaKO87H2o2wBcacD3bRHhMjTkhSEqxPjQ/FE
XuJ1cdbmr3+b3EQR6wf/cYcMx2468/QyVoQ7BADLSPecQhtgGOllkC+cLYN6Md34
Uii6U+VJf0p0q/saxUTZvhR2ka9fqJ4+6C6cOghIecjMYQNHIaNW+eSKunfFsXVU
+QfMD0q2EM9wo20aLnos24yDzRjh9HJc6xfr37jRlv1/boG/EABMG9FnTm35xWrV
R0nw3cpYF7GZg13QicS/ZwEsSd4HyboAruMxJBPvK3Jdr4ZS23bpN0cavWOJsBqZ
VwIDAQAB
-----END PUBLIC KEY-----'''

def get_random_chars_as_string(count: int) -> str:
    characters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#,%^&*()-=_+~`{}[]|:<>.?/')
    selected_chars = random.sample(characters, count)
    return ''.join(selected_chars)

def aes_encrypt(key, data):
    iv = b'0102030405060708'
    cipher = Cipher(algorithms.AES(key.encode('utf-8')), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(ciphertext).decode('utf-8')

def rsa_encrypt(public_key_pem, data: str) -> str:
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8'),
        backend=default_backend()
    )
    encoded_data = base64.b64encode(data.encode('utf-8'))
    ciphertext = public_key.encrypt(
        encoded_data,
        PKCS1v15()
    )

    return base64.b64encode(ciphertext).decode('utf-8')

async def get_token_data(uid: str) -> str:
    data = {
        "type": 0,
        "startTs": round(time.time()*1000),
        "endTs": round(time.time()*1000),
        "env": {
            "p1": "0.1",
            "p2": "pc-Chrome119",
            "p3": "Win32",
            "p4": "Gecko",
            "p5": "zh-CN",
            "p6": "Netscape",
            "p7": "Mozilla",
            "p8": "true",
            "p9": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "p10": 480,
            "p11": 1699803509070,
            "p12": 1707,
            "p13": 1067,
            "p14": 1707,
            "p15": 1067,
            "p16": 1354,
            "p17": 880,
            "p18": "https://web.vip.miui.com/page/info/mio/mio/checkIn?app_version=dev.230904",
            "p19": 5,
            "p20": "",
            "p21": "",
            "p22": 6,
            "p23": "",
            "p24": "",
            "p25": "",
            "p26": "",
            "p28": "",
            "p29": 38,
            "p30": 188,
            "p31": 98,
            "p32": "0.65",
            "p33": [],
            "p34": "https://web.vip.miui.com/page/info/mio/mio/checkIn?app_version=dev.230904"
        },
        "action": {
            "a1": [
                1354,
                880
            ],
            "a2": [],
            "a3": [
                [
                    668,
                    269,
                    1028
                ]
            ],
            "a4": [],
            "a5": [
                [
                    1128,
                    301,
                    5
                ],
                [
                    1119,
                    301,
                    57
                ],
                [
                    1111,
                    300,
                    112
                ],
                [
                    1105,
                    299,
                    164
                ],
                [
                    1097,
                    299,
                    220
                ],
                [
                    1087,
                    298,
                    273
                ],
                [
                    1078,
                    297,
                    324
                ],
                [
                    1065,
                    296,
                    377
                ],
                [
                    1049,
                    295,
                    430
                ],
                [
                    1031,
                    295,
                    481
                ],
                [
                    1002,
                    295,
                    532
                ],
                [
                    966,
                    296,
                    584
                ],
                [
                    917,
                    299,
                    636
                ],
                [
                    840,
                    300,
                    691
                ],
                [
                    770,
                    300,
                    742
                ],
                [
                    732,
                    297,
                    793
                ],
                [
                    718,
                    293,
                    844
                ],
                [
                    686,
                    277,
                    895
                ]
            ],
            "a6": [],
            "a7": [],
            "a8": [],
            "a9": [],
            "a10": [],
            "a11": [],
            "a12": [],
            "a13": [],
            "a14": []
        },
        "force": "false",
        "talkBack": "false",
        "uid": uid,
        "nonce": {
            "t": round(time.time()),
            "r": round(time.time())
        },
        "version": "2.0",
        "scene": "GROW_UP_CHECKIN"
    }

    key = get_random_chars_as_string(16)

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-type': 'application/x-www-form-urlencoded',
        'Origin': 'https://web.vip.miui.com',
        'Pragma': 'no-cache',
        'Referer': 'https://web.vip.miui.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'k': '3dc42a135a8d45118034d1ab68213073',
        'locale': 'zh_CN',
        '_t': round(time.time()*1000),
    }


    data = {
        's': rsa_encrypt(public_key_pem, key),
        'd': aes_encrypt(key, str(data)),
        'a': 'GROW_UP_CHECKIN',
    }
    response = await post('https://verify.sec.xiaomi.com/captcha/v2/data', params=params, headers=headers, data=data)
    result = response.json()
    token = result.get("data", {}).get("token", "")
    return token
    