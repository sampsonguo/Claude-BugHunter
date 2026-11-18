import unittest

from cbh import cli


class HostRankTests(unittest.TestCase):
    def test_label_lookalikes_are_not_high_value(self):
        for host in ("latest.example.test", "contest.example.test", "digital.example.test"):
            with self.subTest(host=host):
                self.assertEqual(cli._rank_host(host)[0], "P2")

    def test_high_value_labels_still_rank_p1(self):
        for host in ("api.example.test", "auth.example.test", "dev.example.test",
                     "api-v2.example.test", "portal.example.test"):
            with self.subTest(host=host):
                self.assertEqual(cli._rank_host(host)[0], "P1")

    def test_static_hosts_stay_kill(self):
        for host in ("static.example.test", "cdn.example.test", "images.example.test"):
            with self.subTest(host=host):
                self.assertEqual(cli._rank_host(host)[0], "KILL")


if __name__ == "__main__":
    unittest.main()
