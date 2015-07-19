# -*- coding: utf-8 -*-
import sphinx.writers.latex

# remove usepackage for sphinx here, we add it later in the preamble in conf.py
#sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('\usepackage{sphinx}', '')

BaseTranslator = sphinx.writers.latex.LaTeXTranslator

class DocTranslator(BaseTranslator):
    
    def __init__(self, *args, **kwargs):
        BaseTranslator.__init__(self, *args, **kwargs)

#     def visit_row(self, node):
#         if self.table.rowcount == 0:
#             self.body.append('\\\\\n')
#                 
#         if self.table.rowcount == 1:
#             self.body.append('\\\\\n')
#             self.body.append('\\hline')
#         
#         super().visit_row(node)

    def depart_row(self, node):
#         self.body.append('\\\\\n')
#         if any(self.remember_multirow.values()):
#             linestart = 1
#             for col in range(1, self.table.col + 1):
#                 if self.remember_multirow.get(col):
#                     if linestart != col:
#                         linerange = str(linestart) + '-' + str(col - 1)
#                         self.body.append('\\cline{' + linerange + '}')
#                     linestart = col + 1
#                     if self.remember_multirowcol.get(col, 0):
#                         linestart += self.remember_multirowcol[col]
#             if linestart <= col:
#                 linerange = str(linestart) + '-' + str(col)
#                 self.body.append('\\cline{' + linerange + '}')
#         else:
#             pass
#             #self.body.append('\\hline')
#             #self.body.append('\\\n')
#         self.table.rowcount += 1
        self.body.append('\\\\\n')
        self.table.rowcount += 1

    def depart_table(self, node):
        if self.table.rowcount > 30:
            self.table.longtable = True
        self.body = self._body
        if not self.table.longtable and self.table.caption is not None:
            self.body.append(u'\n\n\\begin{threeparttable}\n\\centering\n'
                             u'\\capstart\\caption{%s}\n' % self.table.caption)
            for id in self.next_table_ids:
                self.body.append(self.hypertarget(id, anchor=False))
            if node['ids']:
                self.body.append(self.hypertarget(node['ids'][0], anchor=False))
            self.next_table_ids.clear()
        if self.table.longtable:
            self.body.append('\n\\begin{longtable}')
            endmacro = '\\end{longtable}\n\n'
        elif self.table.has_verbatim:
            self.body.append('\n\\begin{tabular}')
            endmacro = '\\end{tabular}\n\n'
        elif self.table.has_problematic and not self.table.colspec:
            # if the user has given us tabularcolumns, accept them and use
            # tabulary nevertheless
            self.body.append('\n\\begin{tabular}')
            endmacro = '\\end{tabular}\n\n'
        else:
            self.body.append('\n\\begin{tabular}')
            endmacro = '\n\\end{tabular}\n'
        if self.table.colspec:
            self.body.append(self.table.colspec)
        else:
            if self.table.has_problematic:
                colwidth = 0.95 / self.table.colcount
                colspec = ('p{%.3f\\linewidth}|' % colwidth) * \
                    self.table.colcount
                self.body.append('{|' + colspec + '}\n')
            elif self.table.longtable:
                self.body.append('{|' + ('l|' * self.table.colcount) + '}\n')
            else:
                self.body.append('{|' + ('L|' * self.table.colcount) + '}\n')
        if self.table.longtable and self.table.caption is not None:
            self.body.append(u'\\caption{%s}' % self.table.caption)
            for id in self.next_table_ids:
                self.body.append(self.hypertarget(id, anchor=False))
            self.next_table_ids.clear()
            self.body.append(u'\\\\\n')
        if self.table.longtable:
            self.body.append('\\hline\n')
            self.body.extend(self.tableheaders)
            self.body.append('\\endfirsthead\n\n')
            self.body.append('\\multicolumn{%s}{c}%%\n' % self.table.colcount)
            self.body.append(r'{{\textsf{\tablename\ \thetable{} -- %s}}} \\'
                             % _('continued from previous page'))
            self.body.append('\n\\hline\n')
            self.body.extend(self.tableheaders)
            self.body.append('\\endhead\n\n')
            self.body.append(r'\hline \multicolumn{%s}{|r|}{{\textsf{%s}}} \\ \hline'
                             % (self.table.colcount,
                                _('Continued on next page')))
            self.body.append('\n\\endfoot\n\n')
            self.body.append('\\endlastfoot\n\n')
        else:
            self.body.append('\\toprule\n')
            self.body.extend(self.tableheaders)

        self.body.append('\\midrule\n')
        self.body.extend(self.tablebody)
        self.body.append('\\bottomrule\n')
        self.body.append(endmacro)
        
        if not self.table.longtable and self.table.caption is not None:
            self.body.append('\\end{threeparttable}\n\n')
        self.table = None
        self.tablebody = None

#     def visit_entry(self, node):
#     
#         if isinstance(node.parent.parent, nodes.thead):
# #            self.body.append('\\textsf{\\relax ')
#             self.body.append('\\relax ')
# #            context += '}'

sphinx.writers.latex.LaTeXTranslator = DocTranslator