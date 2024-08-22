Option Explicit                                                                 ' Generate a compile-time error


'-------------------------------------------------------------------------------
Dim WithEvents XASession_Account As XASession


'-------------------------------------------------------------------------------
' Read the account list
Private Sub btnReadAccounts_Click()

    ' Initialize account list table
    Range("a9:b9") = ""
    Range("A11:E30") = ""

    Set XASession_Account = CreateObject("XA_Session.XASession")

    Dim nCnt As Integer, i As Integer, szAcct As String
    nCnt = XASession_Account.GetAccountListCount()                              ' start from 0

    ' Output
    Cells(9, 1) = XASession_Account.GetServerName()
    Cells(9, 2) = nCnt

    For i = 0 To nCnt - 1
        szAcct = XASession_Account.GetAccountList(i)                            ' get each account number

        Cells(11 + i, 1) = i + 1
        Cells(11 + i, 2) = szAcct
        Cells(11 + i, 3) = XASession_Account.GetAccountName(szAcct)
        Cells(11 + i, 4) = XASession_Account.GetAcctDetailName(szAcct)          ' get account type
        Cells(11 + i, 5) = XASession_Account.GetAcctNickname(szAcct)

        If i >= 10 Then
            Cells(11 + i + 1, 2) = "계좌 수가 " & i & "개를 초과하였습니다."
            Exit Sub
        End If
    Next

End Sub