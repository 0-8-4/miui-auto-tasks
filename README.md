# MIUI Task
一个适用于 小米社区3.0 自动完成 KPI 任务的脚本

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)
=========  

## **关于项目**:

  由 `東雲研究所` 的某位大佬编写  
  由大佬授权 `0-8-4` 使用 `MIT` 开源   
  `0-8-4` 和打酱油的 `TardisLX` 会进行基础维护  
  我们认为小米社区无权在无任何回报的情况下强制要求内测用户完成KPI任务，因此诞生了这个脚本

==========

### **项目介绍**：  
- [x] 可自动登录小米账号刷新社区cookie实现自动化
- [x] 可自动完成以下小米社区KPI任务且不留下可见痕迹  
  - [x] 可完成“在内测圈分享这个版本的体验”KPI任务  
  - [x] 可完成“参与当前版本满意度投票”KPI任务  
  - [x] 可完成“在内测圈提交带日志的bug反馈”KPI任务  
  - [x] 可完成“在内测圈分享这个版本的体验”KPI任务
- [x] 可自动完成以下小米社区活跃分任务且不留下可见痕迹
  - [x] 可完成“加入1个圈子”活跃分任务  
  - [x] 可完成“关注1位用户”活跃分任务  
  - [x] 可完成“点赞1篇帖子”活跃分任务
  - [x] 可完成“发布1条评论”活跃分任务
  - [x] 可完成“发布1篇帖子”活跃分任务

==========

### **使用说明**：
- 使用你喜爱的编辑器打开 `miuitask.py` 及 `passwd2md5.py` 
- 在脚本 Line10 中填写你的MID
  - 请注意MID不是手机号或邮箱
  - 示例: `mid = '123456'`
- 在脚本 Line12 中填写小米账号密码使用MD5加密后的密文
  - MD5并不安全，请不要在任何地方暴露密文
  - 请编辑使用随附的"passwd2md5.py"文件本地进行md5转换
  - 在线转换可能不正确或导致密码泄露，因此不建议使用在线工具转换
- 在脚本 Line19 中填写你常用浏览器的UA，UA可在诸如 `https://ie.icoa.cn` 等类似的网站查看
  - 示例:` lUa = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'`
  - 请务必先使用这个浏览器登录`https://account.xiaomi.com`
- 现在可以尝试使用  `Python3 miuitask.py` 运行脚本了

==========  

#### **其他**：  
* 建议配合 Python3 及 Crontab 使用  
* **欢迎提供有关的思路，提交BUG以及更多完成社区其他任务方式，我们会认真对待~**

========== 

#### **更新说明**：  
 V1.1.0 :
- 增加领取延迟保证成功率
- 增加完成“发布1篇帖子”活跃分任务功能

==========

# **License**
MIT License   
Copyright (C) 2021 東雲研究所   
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.   
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
