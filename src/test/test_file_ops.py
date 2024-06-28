import unittest
from src.log_utils.yaml_utils import generate, load

class TestYamlUtils(unittest.TestCase):
  def test_generate(self):
    config = {"key1": "value1", "key2": "value2"}
    generate(config, name="test_config")
    self.assertEqual(load("test_config"), config)

  def test_load(self):
    config = {"key1": 1, "key2": 2}
    generate(config, name="test_config")
    self.assertEqual(load("test_config"), config)

  def test_load_error(self):
    with self.assertRaises(SystemExit):
      load("non_existent_file")

if __name__ == '__main__':
    unittest.main()
