#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import argparse


def import_mp(file_path, delete_repeat_name):
    from mobileprovision import util
    attrs = 'Name' if delete_repeat_name else None
    util.import_mobileprovision(file_path, replace_at_attrs=attrs)


def parse_mp(file_path):
    from mobileprovision import parser
    import pprint
    plist_obj = parser.plist_obj(file_path)
    pprint.pprint(plist_obj)


def convert_mp(file_path, dst_plist_path):
    from mobileprovision import parser
    parser.convert_plist_file(file_path, dst_plist_path)


def parse_arg():
    """解析命令行的输入的参数"""
    parser = argparse.ArgumentParser("OKEx工程里的多语言国际化相关的便捷操作")
    subparsers = parser.add_subparsers(help="支持的命令如下：")

    import_mp_parser = subparsers.add_parser("import", help="导入mobileprovision文件到系统默认路径里")
    import_mp_parser.set_defaults(func=import_mp)
    import_mp_parser.add_argument("file_path", help="mobileprovision文件路径")
    import_mp_parser.add_argument("-d", "--delete-repeat-name", action="store_true",
                                  help="是否删除Name属性相同的文件")

    parser_mp_parser = subparsers.add_parser("parse", help="解析、打印mobileprovision文件里的内容")
    parser_mp_parser.set_defaults(func=parse_mp)
    parser_mp_parser.add_argument("file_path", help="mobileprovision文件路径")

    convert_mp_parser = subparsers.add_parser("convert", help="转换mobileprovision文件为plist文件")
    convert_mp_parser.set_defaults(func=convert_mp)
    convert_mp_parser.add_argument("file_path", help="mobileprovision文件路径")
    convert_mp_parser.add_argument("dst_plist_path", help="转换后的plist文件路径")

    args = parser.parse_args()
    return args


def main():
    args = parse_arg()
    f_params = args.__dict__.copy()
    del f_params["func"]  # 删除无用参数
    args.func(**f_params)  # 执行命令对应的函数


if __name__ == '__main__':
    main()
