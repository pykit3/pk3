"""Tests for pk3.publish module."""

import os
import unittest
from unittest.mock import patch

from pk3.publish import publish


class TestPublish(unittest.TestCase):
    def test_publish_missing_password(self):
        """Test that publish raises error when TWINE_PASSWORD is not set."""
        with patch.dict(os.environ, {}, clear=True):
            # Ensure TWINE_PASSWORD is not set
            os.environ.pop("TWINE_PASSWORD", None)
            with self.assertRaises(RuntimeError) as ctx:
                publish()
            self.assertIn("TWINE_PASSWORD not set", str(ctx.exception))

    def test_publish_missing_password_message(self):
        """Test error message includes usage hint."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("TWINE_PASSWORD", None)
            with self.assertRaises(RuntimeError) as ctx:
                publish()
            self.assertIn("pk3 publish", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
