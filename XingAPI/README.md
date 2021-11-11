# My `xingAPI` Application Modules

Codes with `XingAPI` from **eBest Investment & Securities**


**\<Reference>**  
&nbsp;- xingAPI 홈페이지 ☞ https://www.ebestsec.co.kr/xingapi/xingMain.jsp  
&nbsp;- xingAPI 도움말 ☞ https://www.ebestsec.co.kr/apiguide/guide.jsp  
&nbsp;- xingAPI COM 개발가이드 ☞ https://www.ebestsec.co.kr/apiguide/guide.jsp?cno=200

- [VBA : Read Account List (2021.11.10)](/XingAPI#vba--read-account-list-20211110)
- [VBA : Login 2 (2021.11.09)](/XingAPI#vba--login-2-20211109)
- [VBA : Login 1 (2021.11.08)](/XingAPI#vba--login-1-20211108)


## [VBA : Read Account List (2021.11.10)](/XingAPI#my-xingapi-application-modules)

- read account list with using `XASession`

![VBA : Read Account List](Images/XingAPI_VBA_Account.gif)

```vba
Dim WithEvents XASession_Account As XASession
```

```vba
Private Sub readAccounts_Click()

    ' Initialize account list table
    ActiveSheet.Range("a9:b9") = ""
    ActiveSheet.Range("A11:E30") = ""

    Set XASession_Account = CreateObject("XA_Session.XASession")

    Dim nCnt As Integer, i As Integer, szAcct As String
    nCnt = XASession_Account.GetAccountListCount()                                  ' start from 0

    ' Output
    ActiveSheet.Cells(9, 1) = XASession_Account.GetServerName()
    ActiveSheet.Cells(9, 2) = nCnt
    
    For i = 0 To nCnt - 1
        szAcct = XASession_Account.GetAccountList(i)                                ' get each account number

        ActiveSheet.Cells(11 + i, 1) = i + 1
        ActiveSheet.Cells(11 + i, 2) = szAcct
        ActiveSheet.Cells(11 + i, 3) = XASession_Account.GetAccountName(szAcct)
        ActiveSheet.Cells(11 + i, 4) = XASession_Account.GetAcctDetailName(szAcct)  ' get account type
        ActiveSheet.Cells(11 + i, 5) = XASession_Account.GetAcctNickname(szAcct)

        If i >= 10 Then
            ActiveSheet.Cells(11 + i + 1, 2) = "계좌 수가 " & i & "개를 초과하였습니다."
            Exit Sub
        End If
    Next

End Sub
```


## [VBA : Login 2 (2021.11.09)](/XingAPI#my-xingapi-application-modules)

- advanced from [VBA : Login 1 (2021.11.08)](/XingAPI#vba--login-1-20211108)
- enter login information on the Excel sheet, not on the `InputBox`
- can choose server type

![VBA : Login 2](Images/XingAPI_VBA_Login_2.gif)

```vba
Option Explicit                                                             ' Generate a compile-time error
```

```vba
Dim WithEvents XASession_Login As XASession                                 ' must be declared in the Excel object
```

```vba
Private Sub btnLogin_Click()

    ' Initialize status cells
    ActiveSheet.Cells(5, 2) = ""                                            ' .Clear : clear even cell form
    ActiveSheet.Cells(6, 2) = ""

    ' Determine server type
    Dim server As String
    If ActiveSheet.Cells(1, 2).Value = "실서버" Then
        server = "hts.ebestsec.co.kr"
    ElseIf ActiveSheet.Cells(1, 2).Value = "모의투자" Then
        server = "demo.ebestsec.co.kr"
    Else
        ActiveSheet.Cells(6, 2) = "서버를 지정해주세요 : 실서버 / 모의투자"
        Exit Sub
    End If

    Set XASession_Login = CreateObject("XA_Session.XASession")

    ' Connect server
    If XASession_Login.ConnectServer(server, 0) = False Then
        ActiveSheet.Cells(5, 2) = "서버 접속 실패"
    Else
        ActiveSheet.Cells(5, 2) = "서버 접속 성공"
    End If

    ' Enter ID, password and certificate password
    Dim ID, pwd, certPwd As String
        ID = ActiveSheet.Cells(2, 2).Value
        pwd = ActiveSheet.Cells(3, 2).Value
        certPwd = ActiveSheet.Cells(4, 2).Value

    ' Send login information
    If XASession_Login.Login(ID, pwd, certPwd, 0, False) = False Then
        ActiveSheet.Cells(5, 2) = "로그인정보 전송 실패"
    Else
        ActiveSheet.Cells(5, 2) = "로그인정보 전송 성공"
    End If

End Sub
```

```vba
' Check the result of login
Private Sub XASession_Login_Login(ByVal szCode As String, ByVal szMsg As String)

    Sheet2.Cells(6, 2) = szCode & " : " & szMsg

End Sub
```


## [VBA : Login 1 (2021.11.08)](/XingAPI#my-xingapi-application-modules)

- **the 1st trial** to build login process into `xingAPI` in **VBA**

![VBA : Login 1](Images/XingAPI_VBA_Login_1.gif)