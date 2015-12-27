import cgi,cgitb
import urllib2
form = cgi.FieldStorage()
name = form.getvalue('username')
pwd = form.getvalue('password')

print name