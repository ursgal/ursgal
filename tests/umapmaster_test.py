#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import unittest
import pprint
from ursgal import umapmaster as umama


class UMapMaster(unittest.TestCase):
    def setUp(self):
        self.umama = umama.UParam.Mapper()


if __name__ == '__main__':
    unittest.main()
