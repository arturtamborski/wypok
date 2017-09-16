from markdown import markdown


def markup(text):
    extensions = [
        #'fenced_code',
        #'footnotes',
        #'tables',
        #'smart_strong',
        #'admonition',
        #'headerid',
        #'nl2br',
        #'sane_lists',
        #'smarty',
    ]
    return markdown(text, output_format='html5', extensions=extensions)
