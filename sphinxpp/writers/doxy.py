from docutils import nodes, writers
from sphinx.writers.text import TextWrapper, TextWriter, TextTranslator
from docutils.utils import column_width
from sphinx.locale import admonitionlabels, _
from sphinx import addnodes

import os
from itertools import zip_longest
import re
from docutils.nodes import Text

class DoxyWriter(TextWriter):
    supported = ('doxy',)
    settings_spec = ('No options here.', '', ())
    settings_defaults = {}

    output = None

    def __init__(self, builder):
        writers.Writer.__init__(self)
        self.builder = builder
        self.translator_class = self.builder.translator_class or DoxyTranslator

MAXWIDTH = 120
STDINDENT = 4

def my_wrap(text, width=MAXWIDTH, **kwargs):
    w = TextWrapper(width=width, **kwargs)
    return w.wrap(text)

class DoxyTranslator(TextTranslator):
    
    section_title = ['\page',
                     '\section',
                     '\subsection',
                     '\subsubsection',
                     '\paragraph'
                     ]
    
    def __init__(self, document, builder):
        TextTranslator.__init__(self, document, builder)
        self.next_figure_ids = set()
        self.next_section_ids = set()
        self.document = document
        self.builder = builder
        self.document.settings.env.config['doxymain_visited'] = False
        
#         self.title = document.settings.env.config['doxy_title']
#         if self.title:
#             self.sectionlevel = 1
#         else:
#             self.sectionlevel = 0
    
    def is_inline(self, node):
        """Check whether a node represents an inline element."""
        return isinstance(node.parent, nodes.TextElement)

    def latex_image_length(self, width_str):
        match = re.match('(\d*\.?\d*)\s*(\S*)', width_str)
        if not match:
            # fallback
            return width_str
        res = width_str
        amount, unit = match.groups()[:2]
        if not unit or unit == "px":
            # pixels: let LaTeX alone
            return None
        elif unit == "%":
            res = "%.3f\\linewidth" % (float(amount) / 100.0)
        return res
    
    def pop_state(self):
        self.stateindent.pop()
        return self.states.pop()
    
#     def dispatch_visit(self, node):
#         print(node)
#         super().dispatch_visit(node)

#     def visit_reference(self, node):
#         print(node)
    
    def visit_document(self, node):
        self.new_state(0)
        self.add_text('/*!')
#         self.add_text('\mainpage ' + self.title)
#         self.add_text('# The document title #      {#index}')
#         if self.title:
#             self.add_text('# ' + self.title + ' #')
            
    
#     def visit_number_reference(self, node):
#         print(node)
#         print(node['secnumber'])
#         if node.get('refid'):
#             ref = self.curfilestack[-1] + ':' + node['refid']
#         else:
#             ref = node.get('refuri', '')[1:].replace('#', ':')
# 
#         title = node.get('title', '%s')
#         hyperref = '\\hyperref[%s]{%s}' % (ref, title % ref)
#         print(hyperref)
#         self.add_text(hyperref)
#         raise nodes.SkipNode
        
        
    def depart_number_reference(self, node):
        pass

#     def visit_section(self, node):
#         self.next_section_ids.add(node)
    
#     def visit_title(self, node):
#         node.children += [Text('proba')]
#         TextTranslator.visit_title(self, node)
#         for id in self.next_section_ids:
#             print(id.__dict__) 
#             print(node.__dict__)
    
#     def depart_title(self, node):
#         if isinstance(node.parent, nodes.section):
#             char = self._title_char
#         else:
#             char = '^'
#         text = ''.join(x[1] for x in self.states.pop() if x[0] == -1)
#         
#         title_refs = ''
#         
#         print(node.parent.__dict__)
#         
#         for id in node.parent.attributes['ids']:
#             title_refs += '{#' + id + '}'
#         
#         self.stateindent.pop()
#         self.states[-1].append(
#             (0, ['', text + '    ' + title_refs, '%s' % (char * column_width(text)), '']))
#         print(node.__dict__)
    
    def visit_emphasis(self, node):
        self.add_text('<em>')

    def depart_emphasis(self, node):
        self.add_text('</em>')

    def visit_literal_emphasis(self, node):
        self.add_text('<em>')

    def depart_literal_emphasis(self, node):
        self.add_text('</em>')

    def visit_strong(self, node):
        self.add_text('<b>')

    def depart_strong(self, node):
        self.add_text('</b>')

    def visit_literal_strong(self, node):
        self.add_text('<b>')

    def depart_literal_strong(self, node):
        self.add_text('</b>')
    
    def visit_figure(self, node):
        self.new_state()
#         self.new_state()
        
#         ids = ''
#         for id in self.next_figure_ids:
#             ids += self.hypertarget(id, anchor=False)
#             
#         if any(isinstance(child, nodes.caption) for child in node):
#             self.add_text('\\capstart\n')
#         self.add_text(ids + '\\end{figure}\n')

    def depart_figure(self, node):
        items = self.pop_state()

        for target in ['html', 'latex']:
            self.new_state()
            text_out = []    
#             self.add_text('\n')
            text_out.append('\\image')
            text_out.append(target)
            text_out.append(items[0][1]) # First the image path was added
            try:
                if items[2][1]:              # Then the caption is added
                    text_out.append('"' + items[2][1] + '"')
            except IndexError:
                pass
                
            text_out.append(items[1][1]) # Then the options were added
        
            self.add_text(' '.join(text_out))
            
            self.end_state(wrap=False)
        
    def visit_image(self, node):
#         if 'alt' in node.attributes:
#             self.add_text(_('[image: %s]') % node['alt'])
        
        attrs = node.attributes
        pre = []                        # in reverse order
        post = []
        include_graphics_options = []
        is_inline = self.is_inline(node)
        
#         if 'scale' in attrs:
#             # Could also be done with ``scale`` option to
#             # ``\includegraphics``; doing it this way for consistency.
#             pre.append('\\scalebox{%f}{' % (attrs['scale'] / 100.0,))
#             post.append('}')
        if 'width' in attrs:
            w = self.latex_image_length(attrs['width'])
            if w:
                include_graphics_options.append('width=%s' % w)
#         if 'height' in attrs:
#             h = self.latex_image_length(attrs['height'])
#             if h:
#                 include_graphics_options.append('height=%s' % h)
#         if 'align' in attrs:
#             align_prepost = {
#                 # By default latex aligns the top of an image.
#                 (1, 'top'): ('', ''),
#                 (1, 'middle'): ('\\raisebox{-0.5\\height}{', '}'),
#                 (1, 'bottom'): ('\\raisebox{-\\height}{', '}'),
#                 (0, 'center'): ('{\\hfill', '\\hfill}'),
#                 # These 2 don't exactly do the right thing.  The image should
#                 # be floated alongside the paragraph.  See
#                 # http://www.w3.org/TR/html4/struct/objects.html#adef-align-IMG
#                 (0, 'left'): ('{', '\\hfill}'),
#                 (0, 'right'): ('{\\hfill', '}'),
#             }
#             try:
#                 pre.append(align_prepost[is_inline, attrs['align']][0])
#                 post.append(align_prepost[is_inline, attrs['align']][1])
#             except KeyError:
#                 pass
        if not is_inline:
            pre.append('\n')
            post.append('\n')
        pre.reverse()
#         if node['uri'] in self.builder.images:
#             uri = self.builder.images[node['uri']]
#         else:
#             # missing image!
#             if self.ignore_missing_images:
#                 return
#             uri = node['uri']
#         if uri.find('://') != -1:
#             # ignore remote images
#             return
#         self.add_text(''.join(pre))
#         self.add_text(_('\\image latex '))

        self.add_text(_(node['uri']))
        options = []
        if include_graphics_options:
            options.append('%s' % ','.join(include_graphics_options))
        
        self.add_text(' '.join(options))
            
            
    def depart_image(self, node):
        pass
#         self.new_state()
#         raise nodes.SkipNode

    def visit_entry(self, node):
#         if 'morerows' in node or 'morecols' in node:
#             print(node)
#             
        self.new_state(0)

    def depart_entry(self, node):
        text = self.nl.join(self.nl.join(x[1]) for x in self.states.pop())
        self.stateindent.pop()
        self.table[-1].append(text)
        if 'morecols' in node:
            self.table[-1].extend(['']*node['morecols'])

#     def visit_colspec(self, node):
#         self.table[0].append(node['colwidth'])
#         print('Colspec ', self.table[0])
#         raise nodes.SkipNode

    def depart_table(self, node):
#         print(node.__dict__)
        lines = self.table[1:]
        fmted_rows = []
        colwidths = self.table[0]
        realwidths = colwidths[:]
        separator = 0
        # don't allow paragraphs in table cells for now
        for line in lines:
            if line == 'sep':
                separator = len(fmted_rows)
            else:
                cells = []
                for i, cell in enumerate(line):
                    par = my_wrap(cell, width=1000)
                    if par:
                        maxwidth = max(column_width(x) for x in par)
                    else:
                        maxwidth = 0 

                    realwidths[i] = max(realwidths[i], maxwidth)
                    cells.append(par)
                fmted_rows.append(cells)
                
        def writesep(char='-'):
            out = ['|']
            for width in realwidths:
                out.append(char * (width+2))
                out.append('|')
            self.add_text(''.join(out) + self.nl)

        def writerow(row):
            lines = zip_longest(*row)
            for line in lines:
                out = ['|']
                for i, cell in enumerate(line):
                    if cell:
                        adjust_len = len(cell) - column_width(cell)
                        out.append(' ' + cell.ljust(
                            realwidths[i] + 1 + adjust_len))
                    else:
                        out.append(' ' * (realwidths[i] + 2))
                    out.append('|')
                self.add_text(''.join(out) + self.nl)

        self.add_text('\n')
        for i, row in enumerate(fmted_rows):
            if separator and i == separator:
                writesep('-')
#             else:
#                 writesep('')
            writerow(row)
#         writesep('-')
        self.table = None
        self.end_state(wrap=False)
        
    def visit_title(self, node):
        self.new_state(0)

    def depart_title(self, node):
        if isinstance(node.parent, nodes.section):
            state = self.pop_state()
            text = ''.join(x[1] for x in state if x[0] == -1)
            if not self.document.settings.env.config['doxymain_visited']:
                title_markdown = '\mainpage'
                self.document.settings.env.config['doxymain_visited'] = True
                title_name = ''
            else:
                title_markdown = self.section_title[self.sectionlevel-1]
                title_name = 'sec_' + ''.join(e for e in text if e.isalnum() or e == ' ').replace(' ', '_').lower()
           
#             title_name = text.replace(' ', '_').lower()
            self.states[-1].append((0, ['', title_markdown + ' ' + title_name + ' ' + text, '']))
        elif isinstance(node.parent, nodes.table):
            text = ''.join(x[1] for x in self.states[-1] if x[0] == -1)
            self.states[-1] = [(0, ['<b>' + text + '</b>'])]
            self.end_state()
#             self.states[-1].append((0, ['', title_markdown + ' ' + title_name + ' ' + text, '']))
        else:
            self.pop_state()
        

    def depart_list_item(self, node):
        if self.list_counter[-1] == -1:
            self.end_state(first='- ', end=[])
        elif self.list_counter[-1] == -2:
            pass
        else:
            self.end_state(first='%s. ' % self.list_counter[-1], end=[])
    
    def depart_bullet_list(self, node):
        super().depart_bullet_list(node)
        self.add_text('\n')
        
    def depart_enumerated_list(self, node):
        super().depart_enumerated_list(node)
        self.add_text('\n')
    
    def visit_literal_block(self, node):
        self.add_text('\code{.unparsed}')
        self.new_state()

    def depart_literal_block(self, node):
        self.end_state(wrap=False)
        self.add_text('\endcode')
    
    def depart_document(self, node):
        self.add_text('*/')
        TextTranslator.depart_document(self, node)

def setup(app):
    app.set_translator('doxy', DoxyTranslator)
#     app.add_config_value('doxy_title', None, True)
