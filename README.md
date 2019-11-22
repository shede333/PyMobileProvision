# PyMobileProvision


parse ".mobileprovision" file in MacOS System;      
解析 MacOS 系统里，iOS和Mac开发常用到的".mobileprovision"文件，提取出里面的"plist"格式的内容

仅支持 **Python3**，Python2版本见：[Py2MobileProvision](https://github.com/shede333/Py2MobileProvision)


## Install

```

pip install PyMobileProvision

```

## Example Modules:

```python

from mobileprovision import MobileProvisionModel

mp_file_path = "/Users/shede333/Desktop/test.mobileprovision"
mp_model = MobileProvisionModel(mp_file_path)

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


## 待完成的功能

* ~~增加pytest标准测试；~~
* ~~增加mp等测试资源；~~
* ~~增加CLI控制功能；~~
* ~~DevCertificateModel增加创建、失效日期属性~~；
* ~~将日期属性，改为时间戳，避免UTC歧义~~；
