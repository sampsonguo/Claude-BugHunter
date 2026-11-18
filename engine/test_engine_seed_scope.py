import unittest

from engine import _in_scope_seed_hosts
from scope import Scope


class EngineSeedScopeTests(unittest.TestCase):
    def test_only_scope_cleared_seeds_are_probed(self):
        scope = Scope(in_scope=["example.test"], seeds=[
            "https://example.test", "http://127.0.0.1:8799", "https://api.example.test"])
        self.assertEqual(_in_scope_seed_hosts(scope), ["api.example.test", "example.test"])

    def test_deny_rule_still_wins_for_seeds(self):
        scope = Scope(in_scope=["example.test"], out_of_scope=["admin.example.test"],
                      seeds=["https://admin.example.test", "https://example.test"])
        self.assertEqual(_in_scope_seed_hosts(scope), ["example.test"])


if __name__ == "__main__":
    unittest.main()
