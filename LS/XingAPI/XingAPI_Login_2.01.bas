Option Explicit                                                                 ' Generate a compile-time error


'-------------------------------------------------------------------------------
Dim WithEvents XASession_Login As XASession                                     ' must be declared in the Excel object


'-------------------------------------------------------------------------------
' Login
Private Sub btnLogin_Click()

    ' Initialize status cells
    Cells(5, 2) = ""                                                            ' .Clear : clear even cell form
    Cells(6, 2) = ""

    ' Determine server type
    Dim server As String
    If Cells(1, 2).Value = "실서버" Then
        server = "hts.ebestsec.co.kr"
    ElseIf Cells(1, 2).Value = "모의투자" Then
        server = "demo.ebestsec.co.kr"
    Else
        Cells(6, 2) = "서버를 지정해주세요 : 실서버 / 모의투자"
        Exit Sub
    End If

    Set XASession_Login = CreateObject("XA_Session.XASession")

    ' Connect server
    If XASession_Login.ConnectServer(server, 0) = False Then
        Cells(5, 2) = "서버 접속 실패"
    Else
        Cells(5, 2) = "서버 접속 성공"
    End If

    ' Enter ID, password and certificate password
    Dim ID As String, pwd As String, certPwd As String
    ID = Cells(2, 2).Value
    pwd = Cells(3, 2).Value
    certPwd = Cells(4, 2).Value

    ' Send login information
    If XASession_Login.Login(ID, pwd, certPwd, 0, False) = False Then
        Cells(5, 2) = "로그인정보 전송 실패"
    Else
        Cells(5, 2) = "로그인정보 전송 성공"
    End If

End Sub


' Check the result of login
Private Sub XASession_Login_Login(ByVal szCode As String, ByVal szMsg As String)

    Cells(6, 2) = szCode & " : " & szMsg

End Sub