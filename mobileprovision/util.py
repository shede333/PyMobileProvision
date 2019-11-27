#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import shutil
import stat
from pathlib import Path

from .parser import MobileProvisionModel

MP_ROOT_PATH = Path("~/Library/MobileDevice/Provisioning Profiles").expanduser()
MP_EXT_NAME = ".mobileprovision"


def mp_path_in_dir(dir_path):
    """
    查找dir_path目录下所有的mobileprovision文件
    :param dir_path: 目录路径
    :return: mobileprovision文件路径列表
    """
    path_list = []
    for file_path in Path(dir_path).iterdir():
        if file_path.suffix == MP_EXT_NAME:
            path_list.append(file_path)
    return path_list


def import_mobileprovision(mp_file_path, replace_at_attrs=('Name',)):
    """
    导入新的mobileprovision文件
    :param mp_file_path: mobileprovision文件路径
    :param replace_at_attrs: 删除属性相同的文件，这里代表需要对比的属性列表，属性间为"或"的关系，默认['Name']，不区分大小写
    :return:
    """
    mp_model = MobileProvisionModel(mp_file_path)
    if isinstance(replace_at_attrs, str):
        replace_at_attrs = [replace_at_attrs]  # 将字符串转为list
    replace_at_attrs = set(replace_at_attrs) if replace_at_attrs else None
    print("开始导入mobileprovision 文件：")

    # 删除同属性的mp文件
    has_same_attr = False  # 是否有同Name的文件
    if replace_at_attrs:
        for file_path in mp_path_in_dir(MP_ROOT_PATH):
            tmp_model = MobileProvisionModel(file_path)
            for tmp_key in replace_at_attrs:
                tmp_value = tmp_model[tmp_key]
                current_value = mp_model[tmp_key]
                if tmp_value and current_value and (tmp_value == current_value):
                    has_same_attr = True
                    print("\t- 删除文件({}: {}): {}".format(tmp_key, tmp_value, file_path))
                    file_path.unlink()

        if not has_same_attr:
            print("\t* 没有相同属性({})的mobileprovision文件".format(replace_at_attrs))

    # 导入新的 mobileprovision 文件
    MP_ROOT_PATH.mkdir(parents=True, exist_ok=True)
    file_name = "{}{}".format(mp_model.uuid, MP_EXT_NAME)
    dst_path = MP_ROOT_PATH.joinpath(file_name)
    shutil.copy(mp_file_path, dst_path)
    # 修改文件权限"-rw-r--r-- "
    dst_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    print("+ 成功导入mobileprovision: \n\tfrom: {}\n\tto: {}".format(mp_file_path, dst_path))
