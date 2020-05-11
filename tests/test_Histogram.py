#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `Histogram` class."""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import contextlib
import unittest
from pathlib import Path

import kalasiris as isis
from .utils import resource_check as rc


run_real_files = True
run_real_files_reason = "Tests on real files, and runs ISIS."

# Hardcoding this, but I sure would like a better solution.
HiRISE_img = Path("test-resources") / "PSP_010502_2090_RED5_0.img"
img = HiRISE_img


@unittest.skipUnless(run_real_files, run_real_files_reason)
class TestResources(unittest.TestCase):
    """Establishes that the test image exists."""

    def test_resources(self):
        (truth, test) = rc(img)
        self.assertEqual(truth, test)


class TestHistogram(unittest.TestCase):
    def setUp(self):
        self.h = isis.Histogram(
            """Cube:           foo.cub
Band:           1
Average:        6490.68
Std Deviation:  166.739
Variance:       27801.9
Median:         6489
Mode:           6489
Skew:           0.0302975
Minimum:        3889
Maximum:        8230

Total Pixels:    2048000
Valid Pixels:    2048000
Null Pixels:     0
Lis Pixels:      0
Lrs Pixels:      0
His Pixels:      0
Hrs Pixels:      0


DN,Pixels,CumulativePixels,Percent,CumulativePercent
3889,1,1,4.88281e-05,4.88281e-05
3924,1,2,4.88281e-05,9.76563e-05
3960,2,4,9.76563e-05,0.000195313
3995,1,5,4.88281e-05,0.000244141
4030,4,9,0.000195313,0.000439453
4065,6,15,0.000292969,0.000732422
4101,12,27,0.000585937,0.00131836
4136,13,40,0.000634766,0.00195312
4171,11,51,0.000537109,0.00249023
4207,11,62,0.000537109,0.00302734
4242,10,72,0.000488281,0.00351562
4277,14,86,0.000683594,0.00419922
4312,4,90,0.000195313,0.00439453
4348,17,107,0.000830078,0.00522461
4383,23,130,0.00112305,0.00634766
4418,9,139,0.000439453,0.00678711
4454,10,149,0.000488281,0.00727539
4489,17,166,0.000830078,0.00810547
4525,17,183,0.000830078,0.00893555
4561,21,204,0.00102539,0.00996094
4597,24,228,0.00117187,0.0111328
4633,19,247,0.000927734,0.0120605
4669,26,273,0.00126953,0.0133301
4705,25,298,0.0012207,0.0145508
4741,16,314,0.00078125,0.015332
4778,20,334,0.000976562,0.0163086
4814,16,350,0.00078125,0.0170898
4850,28,378,0.00136719,0.018457
4886,40,418,0.00195312,0.0204102
4922,24,442,0.00117187,0.021582
4958,45,487,0.00219727,0.0237793
4995,53,540,0.00258789,0.0263672
5031,54,594,0.00263672,0.0290039
5067,64,658,0.003125,0.0321289
5103,57,715,0.0027832,0.0349121
5139,76,791,0.00371094,0.038623
5175,69,860,0.00336914,0.0419922
5212,74,934,0.00361328,0.0456055
5248,97,1031,0.00473633,0.0503418
5284,90,1121,0.00439453,0.0547363
5320,101,1222,0.00493164,0.059668
5356,101,1323,0.00493164,0.0645996
5393,139,1462,0.00678711,0.0713867
5429,134,1596,0.00654297,0.0779297
5465,144,1740,0.00703125,0.0849609
5501,162,1902,0.00791016,0.0928711
5537,167,2069,0.0081543,0.101025
5573,196,2265,0.00957031,0.110596
5610,225,2490,0.0109863,0.121582
5646,271,2761,0.0132324,0.134814
5682,352,3113,0.0171875,0.152002
5718,420,3533,0.0205078,0.17251
5754,524,4057,0.0255859,0.198096
5790,658,4715,0.0321289,0.230225
5827,745,5460,0.036377,0.266602
5863,881,6341,0.0430176,0.309619
5899,1124,7465,0.0548828,0.364502
5935,1329,8794,0.0648926,0.429395
5971,1767,10561,0.0862793,0.515674
6007,2522,13083,0.123145,0.638818
6044,3499,16582,0.17085,0.809668
6081,5372,21954,0.262305,1.07197
6118,8701,30655,0.424854,1.49683
6155,14642,45297,0.714941,2.21177
6192,24158,69455,1.17959,3.39136
6229,39133,108588,1.91079,5.30215
6266,58840,167428,2.87305,8.1752
6303,84919,252347,4.14644,12.3216
6340,115400,367747,5.63477,17.9564
6378,153026,520773,7.47197,25.4284
6415,179963,700736,8.78726,34.2156
6452,204294,905030,9.97529,44.1909
6489,215791,1120821,10.5367,54.7276
6526,208155,1328976,10.1638,64.8914
6563,185376,1514352,9.05156,73.943
6600,151221,1665573,7.38384,81.3268
6637,117121,1782694,5.7188,87.0456
6674,85864,1868558,4.19258,91.2382
6711,59945,1928503,2.927,94.1652
6751,45028,1973531,2.19863,96.3638
6795,30064,2003595,1.46797,97.8318
6841,17215,2020810,0.840576,98.6724
6887,9753,2030563,0.476221,99.1486
6934,5370,2035933,0.262207,99.4108
6980,3296,2039229,0.160937,99.5717
7026,2113,2041342,0.103174,99.6749
7073,1411,2042753,0.0688965,99.7438
7119,1067,2043820,0.0520996,99.7959
7165,818,2044638,0.0399414,99.8358
7211,578,2045216,0.0282227,99.8641
7258,460,2045676,0.0224609,99.8865
7304,364,2046040,0.0177734,99.9043
7350,279,2046319,0.013623,99.9179
7397,276,2046595,0.0134766,99.9314
7443,225,2046820,0.0109863,99.9424
7494,228,2047048,0.0111328,99.9535
7557,240,2047288,0.0117188,99.9652
7624,196,2047484,0.00957031,99.9748
7691,142,2047626,0.00693359,99.9817
7759,108,2047734,0.00527344,99.987
7826,104,2047838,0.00507813,99.9921
7893,78,2047916,0.00380859,99.9959
7961,37,2047953,0.00180664,99.9977
8028,21,2047974,0.00102539,99.9987
8095,12,2047986,0.000585937,99.9993
8163,12,2047998,0.000585937,99.9999
8230,2,2048000,9.76563e-05,100"""
        )

    def test_init_str(self):
        self.assertIsInstance(self.h, isis.Histogram)

    def test_dictlike(self):
        self.assertEqual(self.h["Cube"], "foo.cub")

    def test_listlike(self):
        self.assertEqual(5, len(self.h[0]))

    def test_contains(self):
        self.assertTrue("Std Deviation" in self.h)

    def test_len(self):
        self.assertEqual(107, len(self.h))


@unittest.skipUnless(run_real_files, run_real_files_reason)
class TestHistogram_filesystem(unittest.TestCase):
    def setUp(self):
        self.cube = Path("test_Histogram.cub")
        self.histfile = Path("test_Histogram.hist")
        isis.hi2isis(img, to=self.cube)
        isis.hist(self.cube, to=self.histfile)

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()
        self.cube.unlink()
        self.histfile.unlink()

    def test_init_histfile(self):
        h = isis.Histogram(self.histfile)
        self.assertIsInstance(h, isis.Histogram)

    def test_init_cube(self):
        h = isis.Histogram(self.cube)
        self.assertIsInstance(h, isis.Histogram)

    def test_init_str(self):
        h = isis.Histogram(isis.hist_k(self.cube))
        self.assertIsInstance(h, isis.Histogram)

    def test_dictlike(self):
        h = isis.Histogram(self.histfile)
        self.assertEqual(self.cube.name, h["Cube"])

    def test_listlike(self):
        h = isis.Histogram(self.histfile)
        self.assertEqual(5, len(h[0]))

    def test_contains(self):
        h = isis.Histogram(self.histfile)
        self.assertTrue("Std Deviation" in h)

    def test_len(self):
        h = isis.Histogram(self.histfile)
        self.assertEqual(107, len(h))
