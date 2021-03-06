"""
>>> test()
"""

import os
import shutil
import sys
import tempfile
from datetime import datetime
from cStringIO import StringIO

import dnuos
import dnuos.appdata
import dnuos.audiodir
import dnuos.path

def test():
    """Verify caching functionality"""

    old =  sys.stderr, sys.stdout
    tmpdir = tempfile.mkdtemp()
    cache_file = dnuos.appdata.user_data_file('dirs', tmpdir)
    argv = ['dnuos', '-q', '--cache-dir=' + tmpdir, os.environ['DATA_DIR']]
    try:
        output = StringIO()
        sys.stderr = sys.stdout = output
        try:
            dnuos.main(argv=argv, locale='C')
        finally:
            sys.stderr, sys.stdout = old
        cache = dnuos.setup_cache(cache_file)
        assert cache.version == dnuos.audiodir.Dir.__version__
        for path, adir in cache.iteritems():
            assert dnuos.path.isdir(path)
            adir2 = dnuos.audiodir.Dir(path)
            assert adir.albums == adir2.albums
            assert adir.artists == adir2.artists
            assert adir._audio_files == adir2._audio_files
            assert adir._bad_files == adir2._bad_files
            assert adir._bitrates == adir2._bitrates
            assert adir._lengths == adir2._lengths
            assert adir._types == adir2._types
            m1 = datetime.fromtimestamp(adir.modified).strftime('%x')
            m2 = datetime.fromtimestamp(adir2.modified).strftime('%x')
            assert m1 == m2
            assert adir.path == adir2.path
            assert adir._profiles == adir2._profiles
            assert adir.sizes == adir2.sizes
            assert adir._vendors == adir2._vendors
    finally:
        shutil.rmtree(tmpdir, True)
