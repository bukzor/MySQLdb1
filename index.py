

def make_html_list_from_dir(dirname, filter=lambda f:True, format=lambda f:f):
    from os import listdir
    result = '<ul>'
    for fname in listdir(dirname):
        if not filter(fname):
            continue

        result += '\n    <li><a href="%s/%s">' % (dirname, fname)
        result += '\n        %s' % format(fname)
        result += '\n    </a></li>'

    result += '\n</ul>'
    return result


def html_filter(fname):
    return fname.endswith('.html')

def format_refcount_errors(fname):
    first, second = fname.split('.c.')
    second = second.replace('-refcount-errors.html', '')

    return '%s.c %s' % (first, second)


def main():
    import sys
    for dirname in sys.argv[1:]:
        print make_html_list_from_dir(dirname, html_filter, format_refcount_errors)


if __name__ == '__main__':
    exit(main())
