import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('worker', Path(__file__).with_name('calendar-worker.py'))
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)


class SelectionTests(unittest.TestCase):
    def test_skips_completed_and_orders_by_date(self):
        values = [['Video ID', 'Publish Date', 'Status'], ['V03', '2026-10-01', 'Ready for review'], ['V05', '2026-10-14', 'Queued'], ['V04', '2026-10-12', 'Queued']]
        self.assertEqual(worker.select_episode(values)['episode'], 'V04')

    def test_busy_queue_does_not_select_another(self):
        values = [['Video ID', 'Publish Date', 'Status'], ['V04', '2026-10-12', 'Queued'], ['V05', '2026-10-14', 'In progress']]
        self.assertEqual(worker.select_episode(values)['state'], 'busy')

    def test_rejects_duplicates_and_invalid_dates(self):
        for rows in ([['V04', '2026-10-12', 'Queued'], ['V04', '2026-10-14', 'Queued']], [['V04', 'unknown', 'Queued']]):
            with self.assertRaises(ValueError):
                worker.select_episode([['Video ID', 'Publish Date', 'Status']] + rows)

    def test_sheets_serial_dates(self):
        self.assertEqual(worker.publish_date(46207).isoformat(), '2026-07-04')

    def test_existing_mp4_blocks_and_is_not_confused_with_other_episode(self):
        selected = {'state': 'selected', 'episode': 'V04'}
        with tempfile.TemporaryDirectory() as folder:
            result = worker.preflight(selected, [{'name': 'v04-final-4k.mp4', 'mimeType': 'video/mp4'}, {'name': 'v040-final.mp4', 'mimeType': 'video/mp4'}], Path(folder))
            self.assertEqual(result['existing_episode_masters'], 1)
            self.assertFalse(result['production_started'])
            self.assertIn('already exists', result['blockers'][0])

    def test_idle(self):
        self.assertEqual(worker.select_episode([['Video ID', 'Publish Date', 'Status']])['state'], 'idle')


if __name__ == '__main__':
    unittest.main()
