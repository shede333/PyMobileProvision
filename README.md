# PyMobileProvision

parse ".mobileprovision" file in MacOS System;

解析 MacOS 系统里，iOS和Mac开发常用到的".mobileprovision"文件，提取出里面的"plist"格式的内容


## Install

```

pip isntall PyMobileProvision

```

## Example:

```python

from mobileprovision import parser

mp_file_path = "/Users/shede/Desktop/upload.mobileprovision"
print parser.content(mp_file_path)
print parser.plist_obj(mp_file_path)

```

