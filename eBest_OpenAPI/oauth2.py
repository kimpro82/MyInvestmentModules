"""
eBest Open API / 접근토큰 발급 (token)
2023.07.21

이 코드는 eBest Open API 서버에 OAuth 토큰을 요청하는 함수를 포함한 코드입니다.
OAuth 토큰은 API를 호출할 때 인증 정보로 사용되며, API 호출을 위해 반드시 필요합니다.

사용 전 준비사항:
1. eBest Open API 개발자 센터에서 앱 키와 시크릿 키를 발급받아야 합니다.
2. key.py 파일에 발급받은 앱 키와 시크릿 키를 저장해야 합니다. (예: MOCK_KEY, MOCK_SECRET)

개선사항:
1. OAuth.py (2023.07.11)의 코드를 oauth()라는 함수로 재작성하였습니다.
2. test 변수의 값(True/False)에 따라 return값이 달라집니다.
"""


import pprint
import requests

import key


def oauth(test = False):
    """
    eBest Open API 서버에 OAuth 토큰을 요청하는 함수입니다.

    Parameters:
        test (bool) : 테스트 모드 여부를 설정하는 매개변수입니다. 기본값은 False입니다.

    Returns:
        str         : 성공적으로 OAuth 토큰을 받아온 경우 해당 토큰을 반환합니다.

    Raises:
        requests.exceptions.RequestException : OAuth 요청 중 예외가 발생한 경우 예외를 발생시킵니다.
    """

    # 개발자가 발급받은 앱 키와 시크릿 키를 사용합니다.
    _app_key = key.MOCK_KEY
    _app_secret = key.MOCK_SECRET

    # OAuth 토큰을 요청할 API 경로를 설정합니다.
    _path = "oauth2/token"
    _url_base = "https://openapi.ebestsec.co.kr:8080"
    _url = f"{_url_base}/{_path}"

    # OAuth 요청에 필요한 헤더 정보를 설정합니다.
    _header = {
        "content-type": "application/x-www-form-urlencoded"
    }

    # OAuth 요청에 필요한 파라미터 정보를 설정합니다.
    _param = {
        "grant_type": "client_credentials",
        "appkey": _app_key,
        "appsecretkey": _app_secret,
        "scope": "oob"
    }

    # OAuth 요청을 실행하고 응답을 받아옵니다.
    try:
        _res = requests.post(_url, headers=_header, params=_param, timeout=1)
        _access_token = _res.json()["access_token"]
    except requests.exceptions.RequestException as _e:
        # OAuth 요청 중 예외가 발생한 경우 예외를 발생시킵니다.
        raise _e

    if test:
        return _url, _res, _access_token
    else:
        return _access_token


if __name__ == "__main__":
    # OAuth 함수를 호출하여 액세스 토큰을 받아옵니다.

    url, res, _ = oauth(test = True)
    print("URL      :", url, "\n")                          # OAuth 토큰 요청을 보낸 URL 출력
    print("OAuth    :")
    pprint.pprint(res.json())                               # OAuth 응답 내용 출력
