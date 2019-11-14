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

from mobileprovision import parser

mp_file_path = "/Users/shede333/Desktop/upload.mobileprovision"
print parser.content(mp_file_path)
print parser.plist_obj(mp_file_path)

```

## Example CLI:

```shell

mobileprovision -h 

输出：

usage: OKEx工程里的多语言国际化相关的便捷操作 [-h] {test,import,parse,convert} ...

positional arguments:
  {test,import,parse,convert}
                        支持的命令如下：
    import              导入mobileprovision文件到系统默认路径里
    parse               解析、打印mobileprovision文件里的内容
    convert             转换mobileprovision文件为plist文件

optional arguments:
  -h, --help            show this help message and exit

```


## 待完成的功能

* 增加pytest标准测试；
* 增加mp等测试资源；
* 增加CLI控制功能；
