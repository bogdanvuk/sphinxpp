# -*- coding: utf-8 -*-
import sphinx.writers.latex

# remove usepackage for sphinx here, we add it later in the preamble in conf.py
#sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('\usepackage{sphinx}', '')

BaseTranslator = sphinx.writers.latex.LaTeXTranslator

class DocTranslator(BaseTranslator):

    def __init__(self, *args, **kwargs):
        BaseTranslator.__init__(self, *args, **kwargs)

    def depart_row(self, node):
        self.body.append('\\\\\n')
        if any(self.remember_multirow.values()):
            linestart = 1
            col = self.table.colcount
            for col in range(1, self.table.col + 1):
                if self.remember_multirow.get(col):
                    if linestart != col:
                        linerange = str(linestart) + '-' + str(col - 1)
                        self.body.append('\\cline{' + linerange + '}')
                    linestart = col + 1
                    if self.remember_multirowcol.get(col, 0):
                        linestart += self.remember_multirowcol[col]
            if linestart <= col:
                linerange = str(linestart) + '-' + str(col)
                self.body.append('\\cline{' + linerange + '}')
        else:
            if 'hline' in node.attributes:
                self.body.append('\\hline')
        self.table.rowcount += 1

    def depart_table(self, node):
        if self.table.rowcount > 30:
            self.table.longtable = True
        self.popbody()
        if not self.table.longtable and self.table.caption is not None:
            self.body.append('\n\n\\begin{threeparttable}\n'
                             '\\capstart\\caption{')
            for caption in self.table.caption:
                self.body.append(caption)
            self.body.append('}')
            for id in self.pop_hyperlink_ids('table'):
                self.body.append(self.hypertarget(id, anchor=False))
            if node['ids']:
                self.body.append(self.hypertarget(node['ids'][0], anchor=False))
        if self.table.longtable:
            self.body.append('\n\\begin{longtable}')
            endmacro = '\\end{longtable}\n\n'
        elif self.table.has_verbatim:
            self.body.append('\n\\noindent\\begin{tabular}')
            endmacro = '\\end{tabular}\n\n'
        elif self.table.has_problematic and not self.table.colspec:
            # if the user has given us tabularcolumns, accept them and use
            # tabulary nevertheless
            self.body.append('\n\\noindent\\begin{tabular}')
            endmacro = '\\end{tabular}\n\n'
        else:
            self.body.append('\n\\noindent\\begin{tabulary}{\\linewidth}')
            endmacro = '\\end{tabulary}\n\n'
        if self.table.colspec:
            self.body.append(self.table.colspec)
        else:
            if self.table.has_problematic:
                colspec = ('*{%d}{p{\\dimexpr(\\linewidth-\\arrayrulewidth)/%d'
                           '-2\\tabcolsep-\\arrayrulewidth\\relax}|}' %
                           (self.table.colcount, self.table.colcount))
                self.body.append('{|' + colspec + '}\n')
            elif self.table.longtable:
                self.body.append('{|' + ('l|' * self.table.colcount) + '}\n')
            else:
                self.body.append('{|' + ('L|' * self.table.colcount) + '}\n')
        if self.table.longtable and self.table.caption is not None:
            self.body.append(u'\\caption{')
            for caption in self.table.caption:
                self.body.append(caption)
            self.body.append('}')
            for id in self.pop_hyperlink_ids('table'):
                self.body.append(self.hypertarget(id, anchor=False))
            self.body.append(u'\\\\\n')
        if self.table.longtable:
            self.body.append('\\hline\n')
            self.body.append('\\toprule\n')
            self.body.extend(self.tableheaders)
            self.body.append('\\endfirsthead\n\n')
            self.body.append('\\multicolumn{%s}{c}%%\n' % self.table.colcount)
            self.body.append(r'{{\tablecontinued{\tablename\ \thetable{} -- %s}}} \\'
                             % ('continued from previous page'))
            self.body.append('\n\\hline\n')
            self.body.append('\\toprule\n')
            self.body.extend(self.tableheaders)
            self.body.append('\\midrule\n')
            self.body.append('\\endhead\n\n')
            self.body.append(r'\hline \multicolumn{%s}{|r|}{{\tablecontinued{%s}}} \\ \hline'
                             % (self.table.colcount,
                                ('Continued on next page')))
            self.body.append('\n\\endfoot\n\n')
            self.body.append('\\endlastfoot\n\n')
        else:
            # self.body.append('\\hline\n')
            self.body.append('\\toprule\n')
            self.body.extend(self.tableheaders)

        self.body.append('\\midrule\n')
        self.body.extend(self.tablebody)
        self.body.append('\\bottomrule\n')

        self.body.append(endmacro)
        if not self.table.longtable and self.table.caption is not None:
            self.body.append('\\end{threeparttable}\n\n')
        self.unrestrict_footnote(node)
        self.table = None
        self.tablebody = None

sphinx.writers.latex.LaTeXTranslator = DocTranslator
