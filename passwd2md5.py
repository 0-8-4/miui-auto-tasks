from hashlib import md5

mi_passwd = 'my_password'
# 请将"my_password"改为你的小米账号密码
md5_mi_passwd = md5(mi_passwd.encode('utf8')).hexdigest()
# 利用hashlib模块本地计算md5
print(md5_mi_passwd)
# 输出
