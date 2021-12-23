# MIUI Task
一个适用于 小米社区3.0 自动完成 KPI 任务的脚本

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu) ![GitHub](https://img.shields.io/github/license/0-8-4/miui-auto-tasks) ![python](https://img.shields.io/badge/python-3.6+-blue)


## **关于项目**:

  由 `東雲研究所` 的某位大佬编写  
  由大佬授权 `0-8-4` 使用 `MIT` 开源   
  `0-8-4` 和 `TardisLX` 会进行基础维护  
  我们认为小米社区无权在无任何回报的情况下强制要求内测用户完成KPI任务，因此诞生了这个脚本


## **重要声明**:
- 虽然理论上本脚本不会影响小米社区账户安全，但您需要自行承担使用本脚本的后果

- **我们不鼓励，不支持一切商业使用**
  - 鉴于项目的特殊性，我们可能在任何时间**停止更新**或**删除项目**


### **使用说明**：
关于项目的详细使用方法请阅览 **[WiKi](https://github.com/0-8-4/miui-auto-tasks/wiki)**


### **项目依赖**：
  1. 需要前往 Python 官网自行下载自己系统对应的 Python 版本，或使用自己系统对应的包管理安装，推荐至少 Python 3.6 以上

  ```
  https://www.python.org/downloads/
  ```

  2. Python 3 安装完成之后，请在 **项目目录** 执行以下命令安装所需模块
  ```bash
  pip install -r requirements.txt
  ```
  注意：你可能需要使用管理员权限运行命令行


### **项目介绍**：  
- [x] 支持 多账号 配置
- [x] 支持 Docker 部署
- [x] 支持 腾讯云函数 部署
- [x] 自动登录小米账号刷新社区 Cookie 实现自动化   
- [x] 选择性启用小米社区拔萝卜签到
- [x] 自动完成以下小米社区KPI任务且不留下可见痕迹  
  - “在内测圈分享这个版本的体验” KPI任务  
  - “参与当前版本满意度投票” KPI任务  
  - “内测圈内互动（答疑、点赞、投票）” KPI任务   
- [x] 可自动完成以下小米社区活跃分任务且不留下可见痕迹
  - “加入1个圈子” 活跃分任务  
  - “关注1位用户” 活跃分任务  
  - “点赞1篇帖子” 活跃分任务
- [x] 增强模式下可完成以下社区任务且不留下可见痕迹
  - “在内测圈提交带日志的bug反馈” KPI任务  
  - “发布1条评论” 活跃分任务  
  - “发布1篇帖子” 活跃分任务  


#### **其他**：  
* 在使用本脚本时请临时关闭网络代理工具及广告拦截程序  
* 在服务器上使用前建议先使用服务器IP登录 `https://account.xiaomi.com`  
* 建议配合 Python3 及 Crontab 使用  
* **欢迎提供有关的思路，提交BUG以及更多完成社区其他任务方式，我们会认真对待~**


#### **贡献**：

如果你在使用过程中发现任何问题，可以 [提交 issue](https://github.com/0-8-4/miui-auto-tasks/issues/new) 或自行 Fork 修改后提交 Pull request。

如果你要提交 Pull request，请确保你的代码风格和项目已有的代码保持一致，遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008) ，变量命名清晰，有适当的注释。


#### **更新说明**：

 v1.3.4
 - 新增 多账户支持
 - 修改 配置文件为 YAML  
 - 兼容 旧版 `config.env` 配置文件

 v1.3.3
 - 新增 Docker 支持
 - 新增 腾讯云函数 支持
 - 新增 回帖签名算法
 - 修改 使用面向对象编程重构代码
 - 修改 发帖相关任务移至增强模式
 - 修复 回帖失败的问题

 v1.3.2 - bugfix
 - 修复 在部分Python环境中，读取不到配置文件
 - 修复 安卓的部分编辑器中 找不到隐藏文件的问题

 v1.3.2 :
 - 增加 获取最新的内测分

 v1.3.1 ：
 - 增加 增加写入 Log 到文件

 v1.3 :
 - 增加 独立配置文件
 - 增加 密码登陆方式

 v1.2.3 :
 - 符合 [PEP 8](https://www.python.org/dev/peps/pep-0008) 代码风格

 v1.2.2 :
- 增加 输出系统信息到控制台

 v1.2.1 :
- 默认关闭 “社区拔萝卜签到” 功能  
  - 根据小米社区规则，非正常渠道签到**一经发现可能会导致账户封禁**
  - 如您愿意承担一切可能的后果，请根据 [使用说明](#使用说明) 开启功能

 v1.2.0 :
- 增加 “社区拔萝卜签到” 功能  

 v1.1.0 :
- 增加领取延迟保证成功率
- 增加完成 “发布1篇帖子” 活跃分任务功能


# **License**
```
MIT License

Copyright (c) 2021 東雲研究所

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
