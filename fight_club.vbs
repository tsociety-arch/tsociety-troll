Set shell = CreateObject("WScript.Shell")
url = "https://streamable.com/ichtjh"

For i = 1 To 3
    shell.Run url
    WScript.Sleep 15000  ' milliseconds
Next
