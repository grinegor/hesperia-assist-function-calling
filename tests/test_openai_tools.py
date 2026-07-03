import unittest

from hesperia_assist.openai_tools import to_openai_tools


class OpenAIToolTests(unittest.TestCase):
    def test_exports_strict_function_tools(self):
        tools = to_openai_tools()
        self.assertEqual(len(tools), 3)
        for tool in tools:
            self.assertEqual(tool["type"], "function")
            self.assertTrue(tool["function"]["strict"])
            self.assertFalse(tool["function"]["parameters"]["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
