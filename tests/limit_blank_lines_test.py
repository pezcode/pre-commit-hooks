from __future__ import annotations

import pytest

from pre_commit_hooks.limit_blank_lines import main as limit_blank_lines


@pytest.mark.parametrize(
    ('max_lines', 'input_s', 'expected'),
    (
        (0, b'foobar', b'foobar'),
        (0, b'foo\n\nbar', b'foo\nbar'),
        (0, b'\n\nfoo\nbar\n\n\n', b'foo\nbar\n'),
        (1, b'foo\n\n\n\nbar', b'foo\n\nbar'),
        (1, b'foo\nbar', b'foo\nbar'),
        (2, b'foo\n\n\n\nbar', b'foo\n\n\nbar'),
        (2, b'\nfoo\nbar\n\n\n\n', b'\nfoo\nbar\n\n\n'),
    ),
)
def test_limit_blank_lines(max_lines, input_s, expected, tmp_path):
    path = tmp_path / 'file.txt'
    path.write_bytes(input_s)
    exitcode = 0 if input_s == expected else 1
    assert limit_blank_lines(
        ['--max-blank-lines', str(max_lines), str(path.resolve())],
    ) == exitcode
    assert path.read_bytes() == expected


def test_windows_line_endings(tmp_path):
    path = tmp_path / 'file.txt'
    path.write_bytes(b'\r\n\nfoo\n\n\r\nbar\r\n\n\n')
    assert limit_blank_lines([str(path.resolve())]) == 1
    assert path.read_bytes() == b'\r\nfoo\n\nbar\r\n\n'


@pytest.mark.parametrize(('arg'), ('', '--', 'a.b', 'a/b'))
def test_badopt(arg):
    with pytest.raises(SystemExit) as excinfo:
        limit_blank_lines(['--max-blank-lines', arg])
    assert excinfo.value.code == 2
