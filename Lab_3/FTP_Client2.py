from ftplib import FTP

ftp=FTP("press.tretyakov.ru")
print(ftp.login())
data = ftp.retrlines("LIST")
print(data)

ftp.cwd('Lebedeva')

data = ftp.retrlines("LIST")
print(data)

fileName = "1.jpg"
ftp.retrbinary("RETR "+fileName, open(fileName, "wb").write)
print("done!")
ftp.quit()

