Dim WithEvents XASession_Account As XASession


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

        ActiveSheet.Cells(11 + i, 1) = i
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