from hashlib import md5

mipasswd = 'mypassword'
# 请将"mypassword"改为你的小米账号密码
md5_mipasswd = md5(mipasswd.encode('utf8')).hexdigest()
# 利用hashlib模块本地计算md5
print(md5_mipasswd) 
# 输出
