from urllib import request

#私密代理授权的账户
user = 'poi'

#私密代理授权的密码
password = 'poi'

#私密代理IP
proxyserver = '61.158.130:16816'

#构建一个密码管理对象，用来保存需要的用户名和密码
passwdmgr = request.HTTPPasswordMgrWithDefaultRealm()

#添加用户的信息，第一个参数realm是与远程服务器的域信息，一般下写None,后面三个参数分别是
passwdmgr.add_password(None, proxyserver, None, None)

#构建一个代理基础用户名/密码验证的ProxyBasicAuthHandler处理器对象，参数是创建的密码管理对象
#注意，这里不再使用普通ProxyHandler
proxyauth_handler = request.ProxyBasicAuthHandler(None)

opener = request.build_opener(proxyauth_handler)
opener.add_handler = []
request.install_opener(opener)
response = opener.open(request.Request('http://www.baidu.com/'))
print(response.read().decode('utf-8'))

print('popi')
