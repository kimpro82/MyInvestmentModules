"""
eBest Open API / 접근토큰 발급 (token) 3
2024.08.22

이 코드는 eBest Open API 서버에 OAuth 토큰을 요청하는 함수를 포함한 코드입니다.
OAuth 토큰은 API를 호출할 때 인증 정보로 사용되며, API 호출을 위해 반드시 필요합니다.

사용 전 준비사항:
1. eBest Open API 개발자 센터에서 앱 키와 시크릿 키를 발급받아야 합니다.
2. key.py 파일에 발급받은 앱 키와 시크릿 키를 저장해야 합니다. (예: KEY, SECRET)

히스토리:
1   2023.07.11  첫 작성
2   2023.07.21  함수로 재작성 : oauth()
                test 파라미터 추가 (True/False)
3   2024.08.22  real 파라미터 추가 (실서버/모의서버)
                URL 수정 (회사명 변경)
"""


import pprint
import requests
import key


# OAuth 토큰을 요청할 기본 URL
URL = "https://openapi.ls-sec.co.kr:8080/oauth2/token"


def oauth(_test=False, _real=False):
    """
    eBest Open API 서버에 OAuth 토큰을 요청하는 함수입니다.

    Parameters:
        _test (bool): 테스트 모드 여부를 설정하는 매개변수입니다. 기본값은 False입니다.
        _real (bool): 실서버 여부를 설정하는 매개변수입니다. 기본값은 False입니다.

    Returns:
        str: 성공적으로 OAuth 토큰을 받아온 경우 해당 토큰을 반환합니다.
             테스트 모드(_test=True)일 경우 URL, 응답 객체, 토큰을 반환합니다.

    Raises:
        requests.exceptions.RequestException: OAuth 요청 중 예외가 발생한 경우 예외를 발생시킵니다.
    """

    # 실서버 또는 모의서버에 따라 앱 키와 시크릿 키를 설정
    if _real is True:
        _app_key = key.KEY
        _app_secret = key.SECRET
    else:
        _app_key = key.MOCK_KEY
        _app_secret = key.MOCK_SECRET

    # OAuth 요청에 필요한 헤더 정보
    _header = {
        "content-type": "application/x-www-form-urlencoded"
    }

    # OAuth 요청에 필요한 파라미터 정보
    _param = {
        "grant_type": "client_credentials",
        "appkey": _app_key,
        "appsecretkey": _app_secret,
        "scope": "oob"
    }

    # OAuth 요청 실행
    try:
        _res = requests.post(URL, headers=_header, params=_param, timeout=1)
        _access_token = _res.json()["access_token"]
    except requests.exceptions.RequestException as _e:
        # OAuth 요청 중 예외 발생 시 예외를 발생시킴
        raise _e

    # 테스트 모드인 경우 추가 정보를 반환
    if _test:
        return URL, _res, _access_token
    else:
        return _access_token


if __name__ == "__main__":
    # 테스트 모드로 OAuth 함수 호출하여 액세스 토큰과 요청/응답 데이터를 출력
    url, res, _ = oauth(_test=True)
    print("URL      :", url, "\n")                          # OAuth 토큰 요청을 보낸 URL 출력
    print("OAuth 응답 내용:")
    pprint.pprint(res.json())                               # OAuth 응답 내용 출력
