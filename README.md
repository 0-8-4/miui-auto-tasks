# MIUI Task
一个适用于 社区 4.0 模拟网络功能请求的脚本

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu) 
![GitHub](https://img.shields.io/github/license/0-8-4/miui-auto-tasks) 
![Python](https://img.shields.io/badge/python-3.7+-blue) 
![DockerHub](https://github.com/0-8-4/miui-auto-tasks/actions/workflows/docker-image.yml/badge.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/0-8-4/miui-auto-tasks/badge)](https://www.codefactor.io/repository/github/0-8-4/miui-auto-tasks)

## 我们收到反馈，部分用户已收到通知要求不得继续随意调用社区接口，否则社区账户将被永久封禁。<br/>鉴于以上情况，我们作为项目维护者建议停用脚本。<br/>感谢大家的支持，谢谢所有Star和Fork的人。

## **关于项目**:

  受`東雲研究所` 的某位大佬启发  
  最初的源码由大佬授权 `0-8-4` 使用 `MIT` 开源   
  项目初期由`0-8-4` 和 `TardisLX` 进行维护，现已逐渐转为社区驱动
  我们认为社区无权在无任何回报的情况下强制要求内测用户完成 KPI 任务，因此诞生了这个脚本


## **重要声明**:
- 虽然理论上本脚本不会影响社区账户安全，但您需要自行承担使用本脚本的后果

- **我们不鼓励，不支持一切商业使用**
  - 鉴于项目的特殊性，我们可能在任何时间 **停止更新** 或 **删除项目**


### **使用说明**：
项目支持本地、Docker、青龙面板等部署方式，详细使用说明请参见 **[WiKi](https://github.com/0-8-4/miui-auto-tasks/wiki)**


### **项目依赖**：
  1. 需要前往 Python 官网自行下载自己系统对应的 Python 版本，或使用自己系统对应的包管理安装，推荐至少 Python 3.7 以上

  ```
  https://www.python.org/downloads/
  ```

  2. Python 3 安装完成之后，请在 **项目目录** 执行以下命令安装所需模块
  ```bash
  pip install -r requirements.txt
  ```
  **推荐**
  ```bash
  pip install pdm
  pdm install
  ```
  注意：你可能需要使用管理员权限运行命令行

### **项目介绍**：  
- [x] 支持 多账号 配置
- [x] 支持 Docker 部署
- [x] 支持 青龙面板 部署
- [x] 支持 自动登录账号刷新社区 Cookie 以便于实现自动化   
- [x] 绝大多数功能均可在配置文件中自行开关启用   

&#x26A0; 请注意，配置文件默认禁用了 MIUI Task 绝大多数模拟网络请求的功能能力，请注意修改配置文件按需启用。根据社区相关规则，模拟这些功能的网络请求可能存在一定风险。您需要自行承担使用本脚本的后果

#### **其他**：  
* 在使用本脚本时请临时关闭网络代理工具及广告拦截程序  
* 在服务器上使用前建议先使用服务器IP登录 `https://account.xiaomi.com`  
* 如需定时自动化建议配合 Python3 及 Crontab 使用  
* **欢迎提供有关的思路，提交BUG以及更多完成社区其他任务方式，我们会认真对待~**


#### **贡献**：

如果你在使用过程中发现任何问题，可以使用模板 [提交 issue](https://github.com/0-8-4/miui-auto-tasks/issues/new) 或自行 Fork 修改后提交 Pull request

如果你要提交 Pull request，请确保你的代码风格和项目已有的代码保持一致，遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008) ，变量命名清晰，有适当的注释


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

# **鸣谢**
## 项目

感谢由 [Xiaomi-Community-AutoTask](https://github.com/CMDQ8575/Xiaomi-Community-AutoTask) 启发的部分相关功能代码

## 社区

感谢以下贡献者对本项目做出的贡献

<a href="https://github.com/0-8-4/miui-auto-tasks/graphs/contributors">

  <img src="https://contrib.rocks/image?repo=0-8-4/miui-auto-tasks" />

</a>

![Alt](https://repobeats.axiom.co/api/embed/073d4816527b3720a03cb44fa876fe0de0216124.svg "Repobeats analytics image")

<br><br>

### 本项目所有贡献者感谢所有Star了本项目的人

[![Star History Chart](https://api.star-history.com/svg?repos=0-8-4/miui-auto-tasks&type=Date)](https://star-history.com/#0-8-4/miui-auto-tasks&Date)

## JetBrains 

特别感谢 [JetBrains](https://www.jetbrains.com/) 为开源项目提供免费的 [PyCharm](https://www.jetbrains.com/pycharm/) 等 IDE 的授权  
[<img src=".github/md_pic/jetbrains-variant-3.png" width="200"/>](https://www.jetbrains.com/)