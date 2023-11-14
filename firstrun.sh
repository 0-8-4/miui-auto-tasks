#!/usr/bin/env bash
# new Env("MIUI-Auto-Task 环境配置")
# cron 0 0 1 * * firstrun.sh

echo "开始安装依赖"
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /ql/data/repo/0-8-4_miui-auto-tasks_master/requirements.txt
echo "依赖已安装完毕"

echo "开始首次执行"
task 0-8-4_miui-auto-tasks_master/miuitask.py
echo "首次执行完毕"
echo "请到 脚本管理 - 0-8-4_miui-auto-tasks_master - data - config.yml 中配置参数"
