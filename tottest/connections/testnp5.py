from telnetconnection import TelnetConnection

t = TelnetConnection(hostname="192.168.10.61", prompt=">")

out, err = t.login("admin")
for line in out:
    print line

for line in err:
    print line
    
out, err = t.password("admin")
for line in out:
    print line

for line in err:
    print line
                     
out, err = t.pshow()
for line in out:
    print line

for line in err:
    print line
