#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import plistlib
import shutil
from pathlib import Path

from mobileprovision import util
from mobileprovision import MobileProvisionModel

RESOURCE_PATH = Path(__file__).resolve().parent.joinpath("resource")
SRC_MP_PATH = RESOURCE_PATH.joinpath("sw-src.mobileprovision")


def test_cli_import():
    origin_path = util.MP_ROOT_PATH
    util.MP_ROOT_PATH = RESOURCE_PATH.joinpath("Provisioning Profiles")
    if util.MP_ROOT_PATH.is_dir():
        shutil.rmtree(util.MP_ROOT_PATH)
    util.MP_ROOT_PATH.mkdir()

    mp_model = MobileProvisionModel(SRC_MP_PATH)
    file_name = "{}.mobileprovision".format(mp_model.uuid)
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

    util.import_mobileprovision(SRC_MP_PATH, replace_at_attrs='name')
    assert len(list(util.MP_ROOT_PATH.iterdir())) == 1

    # 删除测试目录
    shutil.rmtree(util.MP_ROOT_PATH)
    # 恢复路径
    util.MP_ROOT_PATH = origin_path


def test_cli_convert():
    dst_path = SRC_MP_PATH.with_name("dst.plist")
    if dst_path.is_file():
        dst_path.unlink()
    MobileProvisionModel(SRC_MP_PATH).convert_to_plist_file(dst_path)
    assert dst_path.is_file()

    p_obj = plistlib.loads(dst_path.read_bytes())
    assert p_obj["AppIDName"] == "XC xyz shede333 testFirst"

    dst_path.unlink()


def test_mp_property():
    from datetime import datetime
    from datetime import timezone
    from datetime import timedelta

    mp_model = MobileProvisionModel(SRC_MP_PATH)

    assert mp_model["name"] == "iOS Team Provisioning Profile: xyz.shede333.testFirst"
    assert mp_model.app_id_name == "XC xyz shede333 testFirst"
    assert mp_model.name == "iOS Team Provisioning Profile: xyz.shede333.testFirst"
    assert len(mp_model.provisioned_devices) == 1
    assert mp_model.team_name == "ShaoWei Wang"
    assert mp_model.team_identifier == "RR23U62KET"
    assert mp_model.uuid == "5e3f9cc7-59d2-4cef-902b-97ba409e5874"
    assert isinstance(mp_model.entitlements, dict)
    assert mp_model.app_id_prefix == "RR23U62KET"
    assert mp_model.app_id() == "xyz.shede333.testFirst"
    assert mp_model.app_id(is_need_prefix=True) == "RR23U62KET.xyz.shede333.testFirst"
    assert mp_model.contain_device_id("00008020-0009306C1429002E")

    assert mp_model.creation_timestamp == datetime(2019, 11, 19, 9, 27, 50).replace(
        tzinfo=timezone.utc).timestamp()
    assert mp_model.expiration_timestamp == datetime(2019, 11, 26, 9, 27, 50).replace(
        tzinfo=timezone.utc).timestamp()
    assert mp_model.date_is_valid() == (datetime.utcnow().timestamp() < mp_model.expiration_timestamp)
    utc_dt = datetime.fromtimestamp(mp_model.creation_timestamp, tz=timezone.utc)
    assert utc_dt.strftime("%Y-%m-%d %H:%M:%S") == "2019-11-19 09:27:50"
    tz_8h = timezone(timedelta(hours=8))  # 东八区
    local_dt = utc_dt.astimezone(tz_8h)
    assert local_dt.strftime("%Y-%m-%d %H:%M:%S") == "2019-11-19 17:27:50"

    import tempfile
    with tempfile.TemporaryDirectory() as dir_path:
        ent_dst_path = Path(dir_path).joinpath("entitlements.plist")
        if ent_dst_path.is_file():
            ent_dst_path.unlink()
        mp_model.export_entitlements_file(ent_dst_path)
        assert ent_dst_path.is_file()

        p_obj = plistlib.loads(ent_dst_path.read_bytes())
        assert p_obj["application-identifier"] == "RR23U62KET.xyz.shede333.testFirst"

    assert len(mp_model.developer_certificates) == 2
    cer_model = mp_model.developer_certificates[0]
    assert cer_model.common_name == "iPhone Developer: 333wshw@163.com (6EWWJK58A9)"
    assert cer_model.sha256 == "122F041D0C659348CC9CB1C1CBC6A60BBB3C8184D9261C73F117DBE785F9AA20"
    assert cer_model.sha1 == "38C56BC325AF693E16E8B4C17CAAB50982868C32"
    assert cer_model.not_valid_before == datetime(2019, 5, 21, 4, 28, 15).replace(
        tzinfo=timezone.utc).timestamp()
    assert cer_model.not_valid_after == datetime(2020, 5, 20, 4, 28, 15).replace(
        tzinfo=timezone.utc).timestamp()
