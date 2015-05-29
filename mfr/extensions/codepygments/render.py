"""Code renderer module."""
import os
import pygments
import pygments.lexers
import pygments.lexers.special
import pygments.formatters
from pygments.util import ClassNotFound
from mako.lookup import TemplateLookup

from mfr.core import extension
from .configuration import defaults

class CodePygmentsRenderer(extension.BaseRenderer):

    DEFAULT_LEXER = pygments.lexers.special.TextLexer

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        with open(self.file_path) as fp:
            content = self._render_html(fp, self.extension)
            return self.TEMPLATE.render(base=self.assets_url, color=defaults.get('PYGMENTS_THEME'), body=content)

    @property
    def requires_file(self):
        return True

    def _render_html(self, fp, ext, *args, **kwargs):
        """Generate an html representation of the file
        :param fp: File pointer
        :return: Content html
        """
        formatter = pygments.formatters.HtmlFormatter(cssclass=defaults.get('CSS_CLASS'))
        content = fp.read()
        try:
            lexer = pygments.lexers.guess_lexer_for_filename(ext, content)
        except ClassNotFound:
            lexer = self.DEFAULT_LEXER()
        return pygments.highlight(content, lexer, formatter)
