# Import smtplib for the actual sending function
import smtplib
import email.utils
import getpass

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
content = 'Hello World'
# Create a text/plain message
msg = MIMEText(content)

me = 'yuanjian3260@sina.com'
you = 'yuanhang3260@gmail.com'
msg['Subject'] = 'Test smtplib'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
servername = 'smtp.sina.com'
port = 587

print 'Connecting to %s' % servername
server = smtplib.SMTP(servername, port)
server.set_debuglevel(True) # show communication with the server
username = me
password = getpass.getpass("%s's password: " % username)

server.ehlo()
# If we can encrypt this session, do it
if server.has_extn('STARTTLS'):
  server.starttls()
  server.ehlo() # re-identify ourselves over TLS connection

server.starttls()

server.login(username, password)
server.sendmail(me, [you], msg.as_string())
server.quit()
