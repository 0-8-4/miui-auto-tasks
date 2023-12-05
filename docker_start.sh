#!/bin/sh
# 执行其他必要的启动命令
nohup pdm run python miuitask.py

# 以前台模式运行 crond，使得容器不会立即退出
exec /usr/sbin/crond -f
