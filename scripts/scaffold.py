#!/usr/bin/env python3
"""Add a Flutter folder skeleton without overwriting project files."""
import argparse
from pathlib import Path
import re

APP = ('di', 'routing', 'theme')
CORE = ('network', 'errors', 'storage', 'widgets')
FEATURE = (
    'data/models', 'data/datasources', 'data/repositories',
    'presentation/cubit', 'presentation/screens', 'presentation/widgets',
)
DOMAIN = ('domain/entities', 'domain/repositories', 'domain/usecases')
ASSETS = ('pngs', 'svgs', 'gifs', 'fonts', 'translations', 'sound')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--feature', action='append', default=[])
    parser.add_argument('--layout', choices=('standard', 'clean'), default='standard')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing files')
    args = parser.parse_args()
    root = args.destination.absolute()
    for feature in args.feature:
        if not re.fullmatch(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)*', feature):
            parser.error('Feature names must be lowercase snake_case.')
    folders = [Path('lib/app') / part for part in APP]
    folders += [Path('lib/core') / part for part in CORE]
    folders += [Path('lib/features')]
    folders += [Path('assets') / part for part in ASSETS]
    for feature in dict.fromkeys(args.feature):
        feature_root = root / 'lib/features' / feature
        if any((feature_root / old).exists() for old in ('ui', 'cubit')):
            parser.error(f'Legacy feature layout detected: {feature_root}. Migration must be handled separately.')
        parts = FEATURE + (DOMAIN if args.layout == 'clean' else ())
        folders += [Path('lib/features') / feature / part for part in parts]
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
    if args.dry_run:
        print(f'Preview: {root} ({args.layout}); no files written.')
        for relative in folders:
            status = 'exists' if (root / relative).exists() else 'create'
            print(f'{status}: {relative}')
        return
    created = 0
    for relative in folders:
        target = root / relative
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)
            created += 1
        # Preserve existing files, including an existing marker.
        if not any(target.iterdir()):
            (target / '.gitkeep').touch(exist_ok=False)
    print(f'Scaffold complete: {root}; layout={args.layout}; {created} new target folders. Existing files preserved.')


if __name__ == '__main__':
    main()
