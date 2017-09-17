#coding:utf-8

import re
from convert import iter_file
from os import path
from configx import conf_stream


INCLUDE_PATTERN = re.compile(r'^\s*?#include\s+?(?P<fn>[-_a-zA-Z\d].*?\.ini)\s*?$')


class MergeConfigX(object):
    def __init__(self, fn):
        self.__lines = []
        self.__duplicate = set()
        self.__load(None, path.normpath(path.abspath(fn)))
        self.__target_x = conf_stream('\n'.join(self.__lines))

        del self.__lines
        del self.__duplicate

    def __load(self, src, dst):
        root = path.dirname(dst) if not src else path.dirname(src)

        for l in iter_file(dst):
            m = INCLUDE_PATTERN.search(l)
            if not m:
                self.__lines.append(l)
                continue
            fn = path.normpath(path.abspath(path.join(root, m.groupdict().get('fn'))))
            if fn in self.__duplicate:
                raise ValueError('circular include for %s by %s' % (fn, src))
            self.__duplicate.add(fn)
            self.__load(dst, fn)

    def get_resolve(self, section, key):
        return self.__target_x.get_resolve(section, key)

    def get(self, section, key, _type=None):
        return self.__target_x.get(section, key, _type)

    def get_fields(self, section):
        return self.__target_x.get_fields(section)

    def has_section(self, section):
        return self.__target_x.has_section(section)

    def get_sections(self):
        return self.__target_x.get_sections()

def load(*files):
    for f in files:
        yield f, MergeConfigX(f)


conf_load = load