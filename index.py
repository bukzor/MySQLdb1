#!/usr/bin/env python


def make_html_list_from_dir(dirname, filter=lambda f:True, format=lambda f:f):
    from os import listdir
    result = '<ul>'
    for fname in sorted(listdir(dirname)):
        if not filter(fname):
            continue

        result += '\n    <li><a href="%s/%s">' % (dirname, fname)
        result += '\n        %s' % format(fname)
        result += '\n    </a></li>'

    result += '\n</ul>'
    return result


def suffix_filter(suffixes):
    def filter(fname):
        return any(fname.endswith(suffix) for suffix in suffixes)
    return filter


def format_refcount_errors(fname):
    if '.c.' not in fname:
        return fname

    first, second = fname.split('.c.')
    second = second.replace('-refcount-errors.html', '')
    second = second.replace('-refcount-errors.v2.html', ' v2')

    return '%s.c %s' % (first, second)


def main():
    import sys
    for dirname in sys.argv[1:]:
        print make_html_list_from_dir(
            dirname,
            suffix_filter(('.json', '.html')),
            format_refcount_errors,
        )


if __name__ == '__main__':
    exit(main())
