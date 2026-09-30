import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('delivery', Path(__file__).with_name('deliver-render.py'))
delivery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(delivery)


class DeliveryTests(unittest.TestCase):
    def test_verified_existing_file_is_reused_without_upload(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'preview.mp4'
            path.write_bytes(b'known media')
            api = delivery.API.__new__(delivery.API)
            api.get = lambda _: {'id': 'reserved', 'mimeType': 'video/mp4', 'size': str(path.stat().st_size), 'md5Checksum': hashlib.md5(path.read_bytes()).hexdigest(), 'parents': ['folder']}
            api.call = lambda *a, **k: self.fail('Existing media must not be uploaded again.')
            self.assertEqual(api.upload(path, {'fileId': 'reserved', 'size': path.stat().st_size}, 'folder'), 'reserved')

    def test_checksum_or_destination_mismatch_cannot_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'preview.mp4'
            path.write_bytes(b'known media')
            api = delivery.API.__new__(delivery.API)
            api.get = lambda _: {'id': 'reserved', 'mimeType': 'video/mp4', 'size': '11', 'md5Checksum': 'wrong', 'parents': ['other']}
            api.call = lambda *a, **k: self.fail('Mismatched media must not be replaced.')
            with self.assertRaises(RuntimeError):
                api.upload(path, {'fileId': 'reserved', 'size': path.stat().st_size}, 'folder')

    def test_request_id_is_bound_to_original_content(self):
        api = delivery.API.__new__(delivery.API)
        api.matches = lambda _: [{'id': 'state'}]
        api.call = lambda *a, **k: ({'sha256': 'old', 'mode': 'preview', 'size': 10}, {})
        with self.assertRaises(RuntimeError):
            api.checkpoint('v04-preview-one', 'new', 'preview', 10)


if __name__ == '__main__':
    unittest.main()
