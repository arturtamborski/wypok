from markdown import markdown


def markup(text):
    return markdown(text, output_format='html5', extensions=[
        #'fenced_code',
        #'footnotes',
        #'tables',
        #'smart_strong',
        #'admonition',
        #'headerid',
        #'nl2br',
        #'sane_lists',
        #'smarty',
    ])
