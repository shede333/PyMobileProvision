#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import shutil
from pathlib import Path

from mobileprovision import parser
from mobileprovision import util

RESOURCE_PATH = Path(__file__).resolve().parent.joinpath("resource")
SRC_MP_PATH = RESOURCE_PATH.joinpath("sw-src.mobileprovision")


def test_cli_import():
    origin_path = util.MP_ROOT_PATH
    util.MP_ROOT_PATH = RESOURCE_PATH.joinpath("Provisioning Profiles")
    if util.MP_ROOT_PATH.is_dir():
        shutil.rmtree(util.MP_ROOT_PATH)
    util.MP_ROOT_PATH.mkdir()

    pl_obj = parser.plist_obj(SRC_MP_PATH)
    file_name = "{}.mobileprovision".format(pl_obj["UUID"])
    dst_path = util.MP_ROOT_PATH.joinpath(file_name)
    assert not dst_path.is_file()
    util.import_mobileprovision(SRC_MP_PATH)
    assert dst_path.is_file()
    assert len(list(util.MP_ROOT_PATH.iterdir())) == 1

    cp_mp_path = dst_path.with_name("123.mobileprovision")
    assert not cp_mp_path.is_file()
    shutil.copy(SRC_MP_PATH, cp_mp_path)
    assert cp_mp_path.is_file()
    assert len(list(util.MP_ROOT_PATH.iterdir())) == 2

    util.import_mobileprovision(SRC_MP_PATH, replace_at_attrs=None)
    assert len(list(util.MP_ROOT_PATH.iterdir())) == 2

    util.import_mobileprovision(SRC_MP_PATH, replace_at_attrs='Name')
    assert len(list(util.MP_ROOT_PATH.iterdir())) == 1

    # 删除测试目录
    shutil.rmtree(util.MP_ROOT_PATH)
    # 恢复路径
    util.MP_ROOT_PATH = origin_path


def test_cli_convert():
    dst_path = SRC_MP_PATH.with_name("dst.plist")
    if dst_path.is_file():
        dst_path.unlink()
    parser.convert_plist_file(SRC_MP_PATH, dst_path)
    assert dst_path.is_file()

    import plistlib
    p_obj = plistlib.loads(dst_path.read_bytes())
    assert p_obj["Name"]

    dst_path.unlink()
