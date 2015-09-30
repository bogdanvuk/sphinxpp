from docutils import nodes, writers
from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinxpp.writers.doxy import DoxyWriter
import os
import codecs
from docutils.io import StringOutput
from sphinx.builders.text import TextBuilder

class DoxyBuilder(TextBuilder):
    name = 'doxy'
    format = 'doxy'
    out_suffix = '.dox'
    allow_parallel = True
    
    def prepare_writing(self, docnames):
        self.writer = DoxyWriter(self)
    
def setup(app):
    app.add_builder(DoxyBuilder)
    app.add_config_value('doxy_title', None, True)
