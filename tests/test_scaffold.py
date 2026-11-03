"""Behavior checks in isolated directories; no Flutter SDK required."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/scaffold.py'


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'app'

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.root), *args],
                              capture_output=True, text=True)

    def test_standard_and_empty_features(self):
        self.assertEqual(self.run_script().returncode, 0)
        self.assertTrue((self.root / 'lib/app/di').is_dir())
        self.assertTrue((self.root / 'lib/core/storage').is_dir())
        self.assertFalse(any(p.is_dir() for p in (self.root / 'lib/features').iterdir()))
        self.assertEqual(self.run_script('--feature', 'user_profile').returncode, 0)
        feature = self.root / 'lib/features/user_profile'
        self.assertTrue((feature / 'presentation/cubit').is_dir())
        self.assertTrue((feature / 'data/repositories').is_dir())
        self.assertFalse((feature / 'domain').exists())
        self.assertFalse(list(self.root.rglob('*.dart')))

    def test_clean_and_repeat_preserve_content(self):
        self.assertEqual(self.run_script('--layout', 'clean', '--feature', 'profile').returncode, 0)
        for part in ('entities', 'repositories', 'usecases'):
            self.assertTrue((self.root / 'lib/features/profile/domain' / part).is_dir())
        (self.root / 'lib/main.dart').write_text('existing source')
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(self.run_script('--layout', 'clean', '--feature', 'profile').returncode, 0)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_preview_makes_no_destination(self):
        result = self.run_script('--layout', 'clean', '--feature', 'profile', '--dry-run')
        self.assertEqual(result.returncode, 0)
        self.assertIn('domain/entities', result.stdout)
        self.assertFalse(self.root.exists())

    def test_invalid_arguments_make_no_destination(self):
        for args in (('--feature', '../escape'), ('--feature', 'Bad Name'), ('--layout', 'unknown')):
            self.assertNotEqual(self.run_script(*args).returncode, 0)
            self.assertFalse(self.root.exists())

    def test_legacy_layout_refused_before_writing(self):
        (self.root / 'lib/features/profile/ui').mkdir(parents=True)
        self.assertNotEqual(self.run_script('--feature', 'profile').returncode, 0)
        self.assertFalse((self.root / 'lib/app').exists())

    def test_file_collision_preflight(self):
        self.root.mkdir()
        (self.root / 'assets').write_text('existing')
        self.assertNotEqual(self.run_script().returncode, 0)
        self.assertFalse((self.root / 'lib').exists())

    def test_symlink_refused(self):
        outside = self.base / 'outside'
        outside.mkdir()
        self.root.symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.run_script().returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
