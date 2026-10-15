import unittest
from importlib.resources import files

import truthrail_core
from truthrail_core.reference import ReferenceAdapter
from truthrail_core.validation import (
    CONTINUITY_SCHEMA_FILES,
    SCHEMA_FILES,
    validate_document,
)


class PackagingTests(unittest.TestCase):
    def test_version_and_single_canonical_api(self):
        self.assertEqual(truthrail_core.__version__, "0.5.0")
        self.assertIs(truthrail_core.ReferenceAdapter, ReferenceAdapter)
        self.assertIs(truthrail_core.validate_document, validate_document)
        self.assertTrue(callable(truthrail_core.bind_execution_plan))

    def test_all_schemas_are_packaged(self):
        root = files("truthrail_core.schemas.v0_1")
        for filename in SCHEMA_FILES.values():
            with self.subTest(version="0.1", filename=filename):
                self.assertTrue(root.joinpath(filename).is_file())

        root_v02 = files("truthrail_core.schemas.v0_2")
        for filename in CONTINUITY_SCHEMA_FILES.values():
            with self.subTest(version="0.2", filename=filename):
                self.assertTrue(root_v02.joinpath(filename).is_file())


if __name__ == "__main__":
    unittest.main()
