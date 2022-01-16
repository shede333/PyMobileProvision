# PyMobileProvision


parse ".mobileprovision" file in MacOS System;      
解析 MacOS 系统里，iOS和Mac开发常用到的".mobileprovision"文件，提取出里面的"plist"格式的内容

仅支持 **Python3**，Python2版本见：[Py2MobileProvision](https://github.com/shede333/Py2MobileProvision)


## Install

```

# 注意：pip要用最新的（version>=21.0），否则，在安装cryptography依赖包时会失败
pip install PyMobileProvision

```

## Example Modules:

```python

from mobileprovision import MobileProvisionModel

mp_file_path = "/Users/shede333/Desktop/test.mobileprovision"
mp_model = MobileProvisionModel(mp_file_path)

# 也支持直接使用mobileprovision文件内容来创建model，AppStore Connect API一般会需要这种情况：
# from pathlib import Path
# file_content = Path(mp_file_path).read_text(encoding="ascii", errors="ignore")
# mp_model = MobileProvisionModel(file_content)

print(mp_model)  # 打印mobileprovision文件的详细信息
print(mp_model.app_id_prefix)  # appID的前缀
print(mp_model.app_id(is_need_prefix=True))  # app的BundleID，带app_id_prefix前缀
print(mp_model["name"])  # mobileprovision的"Name"属性（属性不区分大小写）
print(mp_model.date_is_valid())  # 现在的是否过期
print(mp_model.creation_timestamp)  # 证书创建时间（时间戳，int值）
# ......还有很多其他属性.......

# 将int时间戳 转换为 本地日期时间
from datetime import datetime
local_dt = datetime.fromtimestamp(mp_model.creation_timestamp)
print(local_dt)  

# 打印mobileprovision文件里包含的cer公钥证书信息
print(mp_model.developer_certificates)

# mobileprovision文件是否包含（支持）device_id设备
device_id = "00008020-000XXXXXXXXXXXXXX"  # 设备的唯一ID
print(mp_model.contain_device_id(device_id))  

# 转换为plist格式文件
dst_plist_path = "/Users/shede333/Desktop/test.plist"
mp_model.convert_to_plist_file(dst_plist_path)

# 导出entitlements.plist文件信息
ent_dst_path = "Users/shede333/Desktop/entitlements.plist"
mp_model.export_entitlements_file(ent_dst_path)

```

## Example CLI:

```shell

mobileprovision -h 

输出：

usage: OKEx工程里的多语言国际化相关的便捷操作 [-h] {import,parse,convert,entitlements} ...

positional arguments:
  {import,parse,convert,entitlements}
                        支持的命令如下：
    import              导入mobileprovision文件到系统默认路径里
    parse               解析、打印mobileprovision文件里的内容
    convert             转换mobileprovision文件为plist文件
    entitlements        打印/导出 mobileprovision文件里 entitlements信息

optional arguments:
  -h, --help            show this help message and exit


```


## 公司招聘：

欧科云链招募新同学：  
可分布式`居家办公`，行业龙头，高薪资，年终奖优越，拒绝加班，**1075工作制**，公司提供团建费每人每周200元，还提供各种福利；  
各地同学均可在家办公（**拿北京薪资+社保，在老家工作+生活**），也可在北京公司内（海淀上地）办公；  
支持远程 **线上面试**；  
**web前端、后端、移动端**均在招人，欢迎加入团队~  
**简历**可发送至：<wshw333@gmail.com>  
微信搜索“shede333sw”咨询岗位详情；  

移动端招聘详情如下：  

iOS工程师任职要求：  
1.本科以上学历，可使用英文交流者加分；  
2.三年以上的iOS平台研发经验，良好的代码编写规范。有已上线App开发经验加分，有跨平台开发经验加分；  
3.精通Object-C/Swift语言，熟悉账户Xcode等开发佛能根据，熟练掌握使用iOS SDK，熟悉Go、Python、Ruby语言加分；  
4.有高性能客户端编程经验，有性能调优经历加分；  
5.熟悉iOS主流开源框架，并学习、研究过实现原理和源码；  

Android工程师任职要求：  
1.本科以上学历，可使用英文交流者加分；  
2.三年以上Android开发经验；  
3.熟悉Android常用控件的使用并理解其原理；  
4.熟悉Android Framework原理，阅读过Android源代码者优先；  
5.对java、Kotlin、基本数据结构、计算机网络有较为深入的了解；  
