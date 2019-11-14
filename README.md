# PyMobileProvision


parse ".mobileprovision" file in MacOS System;      
解析 MacOS 系统里，iOS和Mac开发常用到的".mobileprovision"文件，提取出里面的"plist"格式的内容

仅支持 **Python3**，Python2版本见：[Py2MobileProvision](https://github.com/shede333/Py2MobileProvision)

## Install

```

pip install PyMobileProvision

```

## Example:

```python

from mobileprovision import parser

mp_file_path = "/Users/shede333/Desktop/upload.mobileprovision"
print parser.content(mp_file_path)
print parser.plist_obj(mp_file_path)

```

## 待完成的功能

* 增加pytest标准测试；
* 增加mp等测试资源；
* 增加CLI控制功能；
