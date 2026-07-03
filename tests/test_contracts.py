import unittest

from hesperia_assist.contracts import load_contracts


class ContractTests(unittest.TestCase):
    def test_exact_approved_tool_set(self):
        registry = load_contracts()
        self.assertEqual(
            registry.approved_tool_names,
            ("knowledge_base_search", "order_lookup", "subscription_lookup"),
        )

    def test_fail_closed_policy(self):
        registry = load_contracts()
        self.assertTrue(registry.policy["approvedOnly"])
        self.assertTrue(registry.policy["failClosed"])
        self.assertEqual(registry.policy["secretHandling"], "managed-secret")


if __name__ == "__main__":
    unittest.main()
