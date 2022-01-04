#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import plistlib
import re
from datetime import datetime
from datetime import timezone
from pathlib import Path


class DevCertificateModel(object):
    """解析出'cer/der证书'文件信息的model对象"""

    def __init__(self, x509_cer):
        """Constructor for DevCertificateModel"""
        self.x509_cer = x509_cer
        self._sha256 = None
        self._sha1 = None

    def __repr__(self):
        # 使用cer证书内置的hash算法和对应的值
        hash_algorithm = self.x509_cer.signature_hash_algorithm
        hash_value = self.x509_cer.fingerprint(hash_algorithm).hex().upper()
        return "Common Name: {}, {}: {}".format(self.common_name, hash_algorithm.name.upper(),
                                                hash_value)

    @property
    def common_name(self):
        from cryptography.x509.oid import NameOID
        return self.x509_cer.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    @property
    def sha256(self):
        """
        cer证书的sha256值，
        :return: 大写str字符串
        """
        if not self._sha256:
            from cryptography.hazmat.primitives.hashes import SHA256
            self._sha256 = self.x509_cer.fingerprint(SHA256()).hex().upper()
        return self._sha256

    @property
    def sha1(self):
        """
        cer证书的sha1值，
        :return: 大写str字符串
        """
        if not self._sha1:
            from cryptography.hazmat.primitives.hashes import SHA1
            self._sha1 = self.x509_cer.fingerprint(SHA1()).hex().upper()
        return self._sha1

    @property
    def not_valid_before(self):
        """
        证书在此日期前 无效
        :return: UTC时间戳，int值
        """
        dt = self.x509_cer.not_valid_before.replace(tzinfo=timezone.utc)
        return dt.timestamp()

    @property
    def not_valid_after(self):
        """
        证书在此日期后 无效
        :return: UTC时间戳，int值
        """
        dt = self.x509_cer.not_valid_after.replace(tzinfo=timezone.utc)
        return dt.timestamp()

    def date_is_valid(self):
        """
        证书现在是否在有效日期范围内
        :return: 有效则返回true
        """
        return self.not_valid_before < datetime.utcnow().timestamp() < self.not_valid_after


class MobileProvisionModel(object):
    """解析出'.mobileprovision'文件信息的model对象"""

    def __init__(self, file_path_or_text):
        """
        初始化方法
        :param file_path_or_text: 文件路径/文件内容
        """
        tmp_file_path = Path(file_path_or_text)
        if tmp_file_path.is_file():
            self.file_path = tmp_file_path
            file_content = tmp_file_path.read_text(encoding="ascii", errors="ignore")
        else:
            self.file_path = None
            file_content = file_path_or_text
        self.xml_content = xml_from_mp_text(file_content)
        self._origin_info = plistlib.loads(bytes(self.xml_content, encoding="ascii"))
        # 将key转为小写
        self._dict_info = {k.lower(): v for k, v in self._origin_info.items()}
        self._device_sets = None
        self._dev_cer_list = None

    def __getitem__(self, item):
        return self._dict_info.get(item.lower(), None)

    def __repr__(self):
        import pprint
        tmp_dict = dict(self._origin_info)
        tmp_dict["DeveloperCertificates"] = self.developer_certificates

        return pprint.pformat(tmp_dict)

    @property
    def app_id_name(self):
        """
        Apple开发者中心里，创建此mobileprovision文件时，选中的"Identifiers"的名称，注意：是ID的名称
        :return:
        """
        return self["AppIDName"]

    @property
    def name(self):
        """
        Apple开发者中心里，"Profiles"里此mobileprovision文件的名称
        :return: name字符串
        """
        return self["Name"]

    @property
    def provisioned_devices(self):
        """
        :return: 此mobileprovision文件包含（支持）的设备ID字符串列表
        """
        return self["ProvisionedDevices"]

    @property
    def team_name(self):
        """
        Apple开发者中心里，团队名称
        :return: 名称字符串
        """
        return self["TeamName"]

    @property
    def team_identifier(self):
        """
        :return: 团队id字符串
        """
        return self["TeamIdentifier"][0]

    @property
    def uuid(self):
        return self["UUID"]

    @property
    def version(self):
        return self["Version"]

    @property
    def entitlements(self):
        """
        :return: 字典对象
        """
        return self["Entitlements"]

    @property
    def creation_timestamp(self):
        """
        证书的有效起始时间
        :return: UTC时间戳，int值
        """
        return self["CreationDate"].timestamp()

    @property
    def expiration_timestamp(self):
        """
        证书的有效截止时间
        :return: UTC时间戳，int值
        """
        return self["ExpirationDate"].timestamp()

    @property
    def app_id_prefix(self):
        return self["ApplicationIdentifierPrefix"][0]

    @property
    def developer_certificates(self):
        """
        包含的cer证书信息列表
        :return: DevCertificateModel对象列表
        """
        if not self._dev_cer_list:
            from cryptography.hazmat import backends
            from cryptography import x509

            backend = backends.default_backend()
            original_list = self["DeveloperCertificates"]
            dev_cer_list = []
            for tmp_cer_data in original_list:
                cer_obj = x509.load_der_x509_certificate(tmp_cer_data, backend)
                dev_cer_list.append(DevCertificateModel(cer_obj))
            self._dev_cer_list = dev_cer_list

        return self._dev_cer_list

    def date_is_valid(self):
        """
        文件现在是否在有效日期范围内
        :return: 有效则返回true
        """
        return self.creation_timestamp < datetime.utcnow().timestamp() < self.expiration_timestamp

    def app_id(self, is_need_prefix=False):
        """
        标示App的bundleID，例如：com.apple.xcode
        :param is_need_prefix: 是否需要带上ApplicationIdentifierPrefix前缀，默认False
        :return: 标示App的ID
        """
        full_app_id = self.entitlements["application-identifier"]
        if is_need_prefix:
            return full_app_id
        else:
            return full_app_id.replace("{}.".format(self.app_id_prefix), "", 1)

    def contain_device_id(self, device_id):
        """
        是否包含(支持) 此设备ID(deviceID)
        :param device_id: 设备ID字符串
        :return: 包含此设备ID则返回True
        """
        if not self._device_sets:
            self._device_sets = set(self.provisioned_devices)
        return device_id in self._device_sets

    def export_entitlements_file(self, dst_path):
        """
        从mobileprovision文件，提取entitlements环境文件到dst_path；
        效果如同以下命令：
            security cms -D -i embedded.mobileprovision > temp.plist  # 先把mp文件转为plist文件
            /usr/libexec/PlistBuddy -x -c 'Print :Entitlements' temp.plist > entitlements.plist

        :param dst_path: 导出的entitlements文件路径
        :return:
        """
        dst_path = Path(dst_path)
        dst_path.write_bytes(plistlib.dumps(self.entitlements))

    def convert_to_plist_file(self, dst_plist_path):
        """
        转换为plist文件
        :param dst_plist_path: 转换后的plist文件路径
        :return:
        """
        Path(dst_plist_path).open("w").write(self.xml_content)

    # def is_support_valid_cer(self, cer_sha256):
    #     for tmp_cer_model in self.developer_certificates:
    #         if not tmp_cer_model.is


def xml_from_mp_text(mp_text: str):
    """
    从mobileprovision文件内容里，提取出plist部分的字符串；
    效果如同以下命令：
        security cms -D -i embedded.mobileprovision > temp.plist

    :param mp_text: mobileprovision文件内容
    :return: plist部分的字符串内容
    """
    p_start = re.escape("<?xml")
    p_end = re.escape("</plist>")
    pattern_str = f"{p_start}.+{p_end}"
    result = re.search(pattern_str, mp_text, flags=re.DOTALL)
    xml_content = result.group()
    return xml_content


def content(file_path):
    """
    从mobileprovision文件里提取出plist部分的字符串内容；
    效果如同以下命令：
        security cms -D -i embedded.mobileprovision > temp.plist

    :param file_path: mobileprovision文件路径
    :return: plist部分的字符串内容
    """
    file_content = Path(file_path).read_text(encoding="ascii", errors="ignore")
    return xml_from_mp_text(file_content)


def plist_obj(file_path):
    """
    (已废弃，推荐使用'MobileProvisionModel'代替)
    从mobileprovision文件里提取出plist对象;
    :param file_path: mobileprovision文件路径
    :return: plist对象
    """
    return MobileProvisionModel(file_path)._origin_info
    # xml_content = content(file_path)
    # return plistlib.loads(bytes(xml_content, encoding="ascii"))


def convert_plist_file(mp_file_path, dst_file_path):
    """
    (已废弃，推荐使用'MobileProvisionModel.convert_to_plist_file'代替)
    转换为plist文件;
    :param mp_file_path: mobileprovision文件路径
    :param dst_file_path: 转换后得到的plist文件路径
    :return:
    """
    MobileProvisionModel(mp_file_path).convert_to_plist_file(dst_file_path)
    # xml_content = content(mp_file_path)
    # Path(dst_file_path).open("w").write(xml_content)
