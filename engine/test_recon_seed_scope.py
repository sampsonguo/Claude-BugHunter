import subprocess
import unittest
from unittest.mock import patch

import recon as R
from scope import Scope

OOS = "http://127.0.0.1:8799"


def _scope(**kwargs):
    return Scope(in_scope=["example.test"], seeds=[OOS, "https://example.test"], **kwargs)


def _recording_probe(calls):
    def probe(url, timeout=12):
        calls.append(url)
        return 0, ""
    return probe


class _Result:
    stdout = ""


class ReconSeedScopeTests(unittest.TestCase):
    """Every recon entry point must refuse a seed outside the scope file."""

    def test_openapi_recon_skips_out_of_scope_seed(self):
        calls = []
        with patch.object(R, "_probe", side_effect=_recording_probe(calls)):
            R.openapi_recon(_scope(), log=lambda *_: None)
        self.assertTrue(calls)
        self.assertEqual([u for u in calls if "127.0.0.1" in u], [])

    def test_platform_recon_skips_out_of_scope_seed(self):
        calls = []
        with patch.object(R, "_probe", side_effect=_recording_probe(calls)):
            R.platform_recon(_scope(), log=lambda *_: None)
        self.assertTrue(calls)
        self.assertEqual([u for u in calls if "127.0.0.1" in u], [])

    def test_katana_only_crawls_in_scope_seeds(self):
        argv = []
        with patch.object(R, "which", return_value="/usr/local/bin/katana"), \
                patch.object(subprocess, "run", side_effect=lambda cmd, **kw: argv.append(cmd) or _Result()):
            R._katana_urls(_scope(), log=lambda *_: None)
        self.assertEqual(len(argv), 1)
        self.assertIn("https://example.test", argv[0])
        self.assertNotIn(OOS, argv[0])

    def test_gau_only_queries_in_scope_apexes(self):
        argv = []
        with patch.object(R, "which", return_value="/usr/local/bin/gau"), \
                patch.object(subprocess, "run", side_effect=lambda cmd, **kw: argv.append(cmd) or _Result()):
            R._gau_urls(_scope(), log=lambda *_: None)
        self.assertEqual(argv, [["gau", "example.test"]])


class PlatformReconPortTests(unittest.TestCase):
    def test_explicit_port_is_preserved(self):
        calls = []
        with patch.object(R, "_probe", side_effect=_recording_probe(calls)):
            R.platform_recon(Scope(in_scope=["127.0.0.1"], seeds=[OOS]), log=lambda *_: None)
        self.assertTrue(calls)
        for url in calls:
            self.assertTrue(url.startswith(OOS + "/"), url)


if __name__ == "__main__":
    unittest.main()
