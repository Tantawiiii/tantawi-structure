#!/usr/bin/env python3
"""Add a Flutter folder skeleton without overwriting project files."""
import argparse
from pathlib import Path
import re

CORE = (
    'constant', 'di', 'enums', 'extension', 'models', 'network', 'routing',
    'services', 'shared/bottom_sheets', 'shared/screens', 'shared/utils',
    'shared/widgets', 'theme', 'utils',
)
ASSETS = ('pngs', 'svgs', 'gifs', 'fonts', 'translations', 'sound')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--feature', action='append', default=[])
    args = parser.parse_args()
    root = args.destination.absolute()
    for feature in args.feature:
        if not re.fullmatch(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)*', feature):
            parser.error('Feature names must be lowercase snake_case.')
    folders = [Path('lib/core') / part for part in CORE]
    folders += [Path('lib/features')]
    folders += [Path('assets') / part for part in ASSETS]
    for feature in dict.fromkeys(args.feature):
        folders += [Path('lib/features') / feature / part
                    for part in ('data/models', 'cubit', 'ui/widgets')]
    # Preflight every path before making any changes.
    for relative in folders:
        target = root / relative
        for node in (target, *target.parents):
            if node.is_symlink():
                parser.error(f'Refusing symlink path: {node}')
            if node.exists() and not node.is_dir():
                parser.error(f'Expected directory: {node}')
        marker = target / '.gitkeep'
        if marker.is_symlink() or (marker.exists() and not marker.is_file()):
            parser.error(f'Invalid marker path: {marker}')
    created = 0
    for relative in folders:
        target = root / relative
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)
            created += 1
        # Preserve existing files, including an existing marker.
        if not any(target.iterdir()):
            (target / '.gitkeep').touch(exist_ok=False)
    print(f'Scaffold complete: {root}; {created} new target folders. Existing files preserved.')


if __name__ == '__main__':
    main()
