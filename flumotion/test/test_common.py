# -*- Mode: Python; test-case-name: flumotion.test.test_common -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2004,2005 Fluendo, S.L. (www.fluendo.com). All rights reserved.

# This file may be distributed and/or modified under the terms of
# the GNU General Public License version 2 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.GPL" in the source distribution for more information.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with the
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

# Headers in this file shall remain intact.

import os
import sys
import time
import tempfile

from twisted.trial import unittest
from twisted.spread import pb
from twisted.internet import reactor, address

from flumotion.common import common

class TestFormatStorage(unittest.TestCase):
    def testBytes(self):
        value = 4
        assert common.formatStorage(value) == "4.00 "

    def testKibibyte(self):
        value = 1024
        assert common.formatStorage(value) == "1.02 k"
        assert common.formatStorage(value, 3) == "1.024 k"

    def testMegabyte(self):
        value = 1000 * 1000
        assert common.formatStorage(value) == "1.00 M"

    def testMebibyte(self):
        value = 1024 * 1024
        assert common.formatStorage(value) == "1.05 M"
        assert common.formatStorage(value, 3) == "1.049 M"
        assert common.formatStorage(value, 4) == "1.0486 M"

    def testGibibyte(self):
        value = 1024 * 1024 * 1024
        assert common.formatStorage(value, 4) == "1.0737 G"
    
    def testTebibyte(self):
        value = 1024 * 1024 * 1024 * 1024
        assert common.formatStorage(value, 4) == "1.0995 T"
    
    def testPebibyte(self):
        value = 1024 * 1024 * 1024 * 1024 * 1024
        assert common.formatStorage(value, 4) == "1.1259 P"
    
    def testExbibyte(self):
        value = 1024 * 1024 * 1024 * 1024 * 1024 * 1024
        assert common.formatStorage(value, 4) == "1.1529 E"

class TestFormatTime(unittest.TestCase):
    def testSecond(self):
        value = 1
        assert common.formatTime(value) == "00:00"

    def testMinuteSecond(self):
        value = 60 + 1
        assert common.formatTime(value) == "00:01"

    def testHourMinuteSecond(self):
        value = 60 * 60 + 60 + 2
        assert common.formatTime(value) == "01:01"

    def testDay(self):
        value = 60 * 60 * 24
        assert common.formatTime(value) == "1 day 00:00"

    def testDays(self):
        value = 60 * 60 * 24 * 2
        assert common.formatTime(value) == "2 days 00:00"
    
    def testWeek(self):
        value = 60 * 60 * 24 * 7
        assert common.formatTime(value) == "1 week 00:00"
    
    def testWeeks(self):
        value = 60 * 60 * 24 * 7 * 2
        assert common.formatTime(value) == "2 weeks 00:00"
    
    def testYear(self):
        value = 60 * 60 * 24 * 365
        assert common.formatTime(value) == "52 weeks 1 day 00:00"
    
    def testReallyLong(self):
        minute = 60
        hour = minute * 60
        day = hour * 24
        week = day * 7
        
        value = week * 291 + day * 5 + hour * 13 + minute * 5
        assert common.formatTime(value) == "291 weeks 5 days 13:05"

class I1: pass
class I2: pass

class A:
    __implements__ = (I1, )

class B:
    __implements__ = (I2, )
    
class C: pass

class TestMergeImplements(unittest.TestCase):
    def testTwoImplements(self):
        self.assertEquals(common.mergeImplements(A, B), (I1, I2))
        
    def testFirstWithout(self):
        self.assertEquals(common.mergeImplements(B, C), (I2, ))

    def testSecondWithout(self):
        self.assertEquals(common.mergeImplements(A, C), (I1, ))

    def testBothWithout(self):
        self.assertEquals(common.mergeImplements(C, C), ( ))
     
class TestVersion(unittest.TestCase):
    def testVersion(self):
        self.assert_(common.version('abinary'))

class TestArgRepr(unittest.TestCase):
    def testEmpty(self):
        self.assertEqual(common.argRepr(), '')
        
    def testArg(self):
        self.assertEqual(common.argRepr((1, '2')), "1, '2'")
        self.assertEqual(common.argRepr(((None,))), "None")

    def testKwargs(self):
        self.assertEqual(common.argRepr((), dict(foo='bar')), "foo='bar'")
        self.assertEqual(common.argRepr(((1,)), dict(foo='bar')), "1, foo='bar'")

class TestComponentPath(unittest.TestCase):
    def testPath(self):
        self.assertEqual(common.componentPath('Cain', 'Adam'), '/Adam/Cain')
        
    def testArg(self):
        self.assertEqual(common.argRepr((1, '2')), "1, '2'")
        self.assertEqual(common.argRepr(((None,))), "None")

    def testKwargs(self):
        self.assertEqual(common.argRepr((), dict(foo='bar')), "foo='bar'")
        self.assertEqual(common.argRepr(((1,)), dict(foo='bar')), "1, foo='bar'")
         
class TestEnsureDir(unittest.TestCase):
    def testNonExisting(self):
        self.tempdir = tempfile.mkdtemp()
        os.system("rm -r %s" % self.tempdir)
        common.ensureDir(self.tempdir, "a description")
        os.system("rm -r %s" % self.tempdir)
    def testExisting(self):
        self.tempdir = tempfile.mkdtemp()
        common.ensureDir(self.tempdir, "a description")
        os.system("rm -r %s" % self.tempdir)

class TestPid(unittest.TestCase):
    def testAll(self):
        pid = common.getPid('test', 'default')
        self.failIf(pid)
        common.writePidFile('test', 'default')
        common.waitPidFile('test', 'default')
        pid = common.getPid('test', 'default')
        self.assertEquals(os.getpid(), pid)
        common.deletePidFile('test', 'default')

class TestPackagePath(unittest.TestCase):
    def testCurrent(self):
        self.tempdir = tempfile.mkdtemp()
        packagedir = os.path.join(self.tempdir, "package")
        os.mkdir(packagedir)
        handle = open(os.path.join(packagedir, "__init__.py"), "w")
        handle.close()
        common.registerPackagePath(self.tempdir)
        os.system("rm -r %s" % self.tempdir)

    def testTwoStackedProjects(self):
        # we create two stacked projects
        # A is under a subdir of tempdir
        # B lives in the tempdir
        # each has parts of a common namespace
        # set up stuff so we can import from both
        # this shows we can develop uninstalled against uninstalled
        self.cwd = os.getcwd()
        self.tempdir = tempfile.mkdtemp('', 'trial')

        self._createA()
        self._createB()

        os.chdir(self.tempdir)

        # first show we cannot import from A
        try:
            import package.A
            self.fail("Should not be able to import package.A")
        except ImportError:
            pass

        # set up so we can import from A
        sys.path.append(self.adir)
        try:
            import package.A
        except ImportError:
            self.fail("Should be able to import package.A")

        # but still can't from project B under same namespace
        try:
            import package.B
            self.fail("Should not be able to import package.B")
        except ImportError:
            pass

        # but we can pull in registerPackagePath from project A to bootstrap,
        # and register the space for B
        package.A.registerPackagePath(self.tempdir, prefix='package')
        try:
            import package.B
        except ImportError:
            self.fail("Should be able to import package.B")

    def _createA(self):
        self.adir = os.path.join(self.tempdir, "A")
        os.mkdir(self.adir)
        apackagedir = os.path.join(self.adir, "package")
        os.mkdir(apackagedir)
        open(os.path.join(apackagedir, "__init__.py"), "w").close()
        handle = open(os.path.join(apackagedir, "A.py"), "w")
        handle.write('me = "A"\n')
        handle.write('from flumotion.common.common import registerPackagePath\n')
        handle.close()

    def _createB(self):
        packagedir = os.path.join(self.tempdir, "package")
        os.mkdir(packagedir)
        open(os.path.join(packagedir, "__init__.py"), "w").close()
        handle = open(os.path.join(packagedir, "B.py"), "w")
        handle.write('me = "B"\n')
        handle.close()

class TestAddress(unittest.TestCase):
    def setUp(self):
        self.address = address.IPv4Address('TCP', 'localhost', '8000')
        
    def testGetHost(self):
        self.failUnlessEqual(common.addressGetHost(self.address), 'localhost')

    def testGetPort(self):
        self.failUnlessEqual(common.addressGetPort(self.address), '8000')

class TestPort(unittest.TestCase):
    def testCheckPortFree(self):
       factory = pb.PBServerFactory(pb.Root())
       p = reactor.listenTCP(0, factory, interface="127.0.0.1")
       port = common.addressGetPort(p.getHost())
       #reactor.callLater(0, self._print, p)
       #reactor.run()
       self.failIf(common.checkPortFree(port))
       self.failUnless(common.checkRemotePort('127.0.0.1', port))
       self.failUnless(common.checkRemotePort('localhost', port))
       self.failIf(common.getFirstFreePort(port) <= port)

       # run reactor and schedule the stop, which would stop the factory
       reactor.callLater(0, lambda: reactor.stop())
       reactor.run()
       self.failUnless(common.checkPortFree(port))
       self.failIf(common.checkRemotePort('127.0.0.1', port))
       self.failIf(common.checkRemotePort('localhost', port))
       self.failUnlessEqual(common.getFirstFreePort(port), port)

    def _print(self, p):
        print p, p.getHost()
        
class TestProcess(unittest.TestCase):
    def testTermPid(self):
        ret = os.fork()
        if ret == 0:
            # child
            time.sleep(4)
            os._exit(0)
        else:
            # parent
            self.failUnless(common.checkPidRunning(ret))
            self.failUnless(common.termPid(ret))
            os.waitpid(ret, 0)
            # now that it's gone, it should fail
            self.failIf(common.checkPidRunning(ret))
            self.failIf(common.termPid(ret))
            
    def testKillPid(self):
        ret = os.fork()
        if ret == 0:
            # child
            common.waitForTerm()
            os._exit(0)
        else:
            # parent
            self.failUnless(common.killPid(ret))
            os.waitpid(ret, 0)
            # now that it's gone, it should fail
            self.failIf(common.killPid(ret))

    def testKillPid(self):
        pid = os.getpid()

        ret = os.fork()
        if ret == 0:
            # child
            time.sleep(0.5)
            self.failUnless(common.termPid(pid))
            os._exit(0)
        else:
            # parent
            common.waitForTerm()

class TestObjRepr(unittest.TestCase):
    def testMe(self):
        t = TestObjRepr()
        self.assertEquals(common.objRepr(t),
            'flumotion.test.test_common.TestObjRepr')
    
class TestPathToModule(unittest.TestCase):
    def testPaths(self):
        tests = {
            'flumotion/common/common.py': 'flumotion.common.common',
            'flumotion/common/__init__.pyc': 'flumotion.common',
            'flumotion/common': 'flumotion.common',
        }
        
        for (path, module) in tests.items():
            self.assertEquals(common.pathToModuleName(path), module)

class TestRecursively(unittest.TestCase):
    def testListDir(self):
        self.tempdir = tempfile.mkdtemp()

        # empty tree
        a = os.path.join(self.tempdir, 'A')
        common.ensureDir(a, "a description")
        dirs = common._listDirRecursively(self.tempdir)
        self.assertEquals(dirs, [])

        # add a non-python file
        os.system("touch %s" % os.path.join(a, 'test'))
        dirs = common._listDirRecursively(self.tempdir)
        self.assertEquals(dirs, [])

        # add a python file; should now get returned
        os.system("touch %s" % os.path.join(a, 'test.py'))
        dirs = common._listDirRecursively(self.tempdir)
        self.assertEquals(dirs, [a])

        # add another level
        b = os.path.join(self.tempdir, 'B')
        b = os.path.join(self.tempdir, 'B')
        common.ensureDir(b, "a description")
        c = os.path.join(b, 'C')
        common.ensureDir(c, "a description")
        dirs = common._listDirRecursively(self.tempdir)
        self.assertEquals(dirs, [a])

        # add a non-python file
        os.system("touch %s" % os.path.join(c, 'test'))
        dirs = common._listDirRecursively(self.tempdir)
        self.assertEquals(dirs, [a])

        # add a python file; should now get returned
        os.system("touch %s" % os.path.join(c, 'test.py'))
        dirs = common._listDirRecursively(self.tempdir)
        self.assertEquals(dirs.sort(), [a, c].sort())

        # cleanup
        os.system("rm -r %s" % self.tempdir)

    def testListPyfile(self):
        self.tempdir = tempfile.mkdtemp()

        # empty tree
        a = os.path.join(self.tempdir, 'A')
        common.ensureDir(a, "a description")
        dirs = common._listPyFileRecursively(self.tempdir)
        self.assertEquals(dirs, [])

        # add a non-python file
        os.system("touch %s" % os.path.join(a, 'test'))
        dirs = common._listPyFileRecursively(self.tempdir)
        self.assertEquals(dirs, [])

        # add a __init__ file
        os.system("touch %s" % os.path.join(a, '__init__.py'))
        dirs = common._listPyFileRecursively(self.tempdir)
        self.assertEquals(dirs, [])
        os.system("touch %s" % os.path.join(a, '__init__.pyc'))
        dirs = common._listPyFileRecursively(self.tempdir)
        self.assertEquals(dirs, [])

        # add a python file; should now get returned
        test1 = os.path.join(a, 'test.py')
        os.system("touch %s" % test1)
        dirs = common._listPyFileRecursively(self.tempdir)
        self.assertEquals(dirs, [test1])

        # add another level
        b = os.path.join(self.tempdir, 'B')
        common.ensureDir(b, "a description")
        c = os.path.join(b, 'C')
        common.ensureDir(c, "a description")
        dirs = common._listPyFileRecursively(self.tempdir)
        self.assertEquals(dirs, [test1])

        # add a non-python file
        os.system("touch %s" % os.path.join(c, 'test'))
        dirs = common._listPyFileRecursively(self.tempdir)
        self.assertEquals(dirs, [test1])

        # add a python file; should now get returned
        test2 = os.path.join(c, 'test.py')
        os.system("touch %s" % test2)
        dirs = common._listPyFileRecursively(self.tempdir)
        self.assertEquals(dirs.sort(), [test1, test2].sort())
        mods = common._findEndModuleCandidates(self.tempdir,
            prefix='')
        self.assertEquals(mods, ['B.C.test', 'A.test'])

        # add a python file but with .c; should now get returned, but
        # no new module candidate
        test3 = os.path.join(c, 'test.pyc')
        os.system("touch %s" % test3)
        dirs = common._listPyFileRecursively(self.tempdir)
        self.assertEquals(dirs.sort(), [test1, test2, test3].sort())

        mods = common._findEndModuleCandidates(self.tempdir,
            prefix='')
        self.assertEquals(mods, ['B.C.test', 'A.test'])

        # cleanup
        os.system("rm -r %s" % self.tempdir)
