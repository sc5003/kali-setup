import ldap3
host = "10.16.6.57"
port = 636
server = ldap3.Server(host, get_info = ldap3.ALL, port = port, use_ssl = True)
connection = ldap3.Connection(server)
connection.bind()

print(server.info)