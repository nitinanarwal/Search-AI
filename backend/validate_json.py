import json
from pathlib import Path


def main() -> None:
    json_path_candidates = [
        Path('../data/sample_data.json').resolve(),
        Path('..') / 'data' / 'sample_data.json',
        Path(__file__).resolve().parent.parent / 'data' / 'sample_data.json',
    ]

    json_path = None
    for candidate in json_path_candidates:
        if Path(candidate).exists():
            json_path = Path(candidate)
            break

    if json_path is None:
        print('ERROR: sample_data.json not found')
        raise SystemExit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
    except Exception as exc:
        print(f'ERROR: Failed to parse JSON: {exc}')
        raise SystemExit(1)

    businesses = data.get('businesses', [])
    print('OK')
    print(f'path={json_path}')
    print(f'business_count={len(businesses)}')
    print(f'keys={list(data.keys())}')


if __name__ == '__main__':
    main()
