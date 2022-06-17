Dim WithEvents XAQuery_t1101 As XAQuery


' T1101 : Current Price
Private Sub Request_t1101()

    If XAQuery_t1101 Is Nothing Then
        Set XAQuery_t1101 = CreateObject("XA_DataSet.XAQuery")                      ' set XAQuery object
        XAQuery_t1101.ResFileName = "c:\\eBEST\xingAPI\Res\t1101.res"               ' call related .res file
    End If

    Dim shcode As String
    shcode = ActiveSheet.Range("R2").Value

    Call XAQuery_t1101.SetFieldData("t1101InBlock", "shcode", 0, shcode)            ' 0 : nOccursIndex, '0' 고정

    If XAQuery_t1101.Request(False) < 0 Then
        ActiveSheet.Range("R27") = "전송 오류"
    End If

End Sub


Private Sub XAQuery_t1101_ReceiveData(ByVal szTrCode As String)

    ActiveSheet.Range("R3") = XAQuery_t1101.GetFieldData("t1101OutBlock", "hname", 0)                               ' 종목명
    ActiveSheet.Range("Q5") = XAQuery_t1101.GetFieldData("t1101OutBlock", "price", 0)                               ' 현재가
    Dim sSign As String
    sSign = GetSign(XAQuery_t1101.GetFieldData("t1101OutBlock", "sign", 0))                                         ' 전일대비구분 (※ 별도 함수 GetSign() 정의 필요)
    ActiveSheet.Range("S5") = sSign & XAQuery_t1101.GetFieldData("t1101OutBlock", "change", 0)                      ' 전일대비
    ActiveSheet.Range("T5") = XAQuery_t1101.GetFieldData("t1101OutBlock", "diff", 0) / 100                          ' 등락률
    ActiveSheet.Range("U5") = XAQuery_t1101.GetFieldData("t1101OutBlock", "volume", 0)                              ' (당일)누적거래량

    Dim i As Integer
    For i = 1 To 10
        ActiveSheet.Range("S" & (6 + 11 - i)) = XAQuery_t1101.GetFieldData("t1101OutBlock", "offerho" & i, 0)       ' 매도호가
        ActiveSheet.Range("R" & (6 + 11 - i)) = XAQuery_t1101.GetFieldData("t1101OutBlock", "offerrem" & i, 0)      ' 매도호가수량
        ActiveSheet.Range("Q" & (6 + 11 - i)) = XAQuery_t1101.GetFieldData("t1101OutBlock", "preoffercha" & i, 0)   ' 직전매도대비수량
        ActiveSheet.Range("S" & (6 + 10 + i)) = XAQuery_t1101.GetFieldData("t1101OutBlock", "bidho" & i, 0)         ' 매수호가
        ActiveSheet.Range("T" & (6 + 10 + i)) = XAQuery_t1101.GetFieldData("t1101OutBlock", "bidrem" & i, 0)        ' 매수호가수량
        ActiveSheet.Range("U" & (6 + 10 + i)) = XAQuery_t1101.GetFieldData("t1101OutBlock", "prebidcha" & i, 0)     ' 직전매수대비수량
    Next i

End Sub


Private Function GetSign(ByVal sSign As String)

    Select Case sSign
        Case "1"
            GetSign = "↑"
        Case "2"
            GetSign = "▲"
        Case "4"
            GetSign = "↓"
        Case "5"
            GetSign = "▼"
        Case Else
            GetSign = ""
    End Select

End Function


Private Sub Worksheet_Change(ByVal Target As Range)

    If Not Intersect(Range("R2"), Target) Is Nothing Then
    ' If Target.Range("R2") Is changed Then                                                 ' doesn't work well
        Call btnRequestT1101_Click
    End If

End Sub


Private Sub btnRequestT1101_Click()

    ActiveSheet.Range("R3") = ""
    ActiveSheet.Range("Q5:U5") = ""
    ActiveSheet.Range("Q7:U26") = ""
    ActiveSheet.Range("R27") = ""

    Call Request_t1101

End Sub