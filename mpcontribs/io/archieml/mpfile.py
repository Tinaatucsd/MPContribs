from __future__ import unicode_literals, print_function
import six, archieml, warnings, pandas
from mpcontribs.config import mp_level01_titles
from ..core.mpfile import MPFileCore
from ..core.recdict import RecursiveDict
from ..core.utils import nest_dict, normalize_root_level
from ..core.utils import read_csv, pandas_to_dict, make_pair

class MPFile(MPFileCore):
    """Object for representing a MP Contribution File in ArchieML format."""

    @staticmethod
    def from_string(data):
        # use archieml-python parse to import data
        mpfile = MPFile.from_dict(RecursiveDict(archieml.loads(data)))
        # post-process internal representation of file contents
        for key in mpfile.document.keys():
            is_general, root_key = normalize_root_level(key)
            if is_general:
                # make part of shared (meta-)data, i.e. nest under `general` at
                # the beginning of the MPFile
                if mp_level01_titles[0] not in mpfile.document:
                    mpfile.document.insert_before(
                        mpfile.document.keys()[0],
                        (mp_level01_titles[0], RecursiveDict())
                    )
                mpfile.document.rec_update(nest_dict(
                    mpfile.document.pop(key),
                    [ mp_level01_titles[0], root_key ]
                ))
            else:
                # normalize identifier key (pop & insert)
                # using rec_update since we're looping over all entries
                # also: support data in bare tables (marked-up only by
                #       root-level identifier) by nesting under 'data'
                value = mpfile.document.pop(key)
                keys = [ root_key ]
                if isinstance(value, list): keys.append('table')
                mpfile.document.rec_update(nest_dict(value, keys))
                # Note: CSV section is marked with 'data ' prefix during iterate()
                for k,v in mpfile.document[root_key].iterate():
                    if isinstance(k, six.string_types) and \
                       k.startswith(mp_level01_titles[1]):
                        # k = table name (incl. data prefix)
                        # v = csv string from ArchieML free-form arrays
                        table_name = k[len(mp_level01_titles[1]+' '):]
                        pd_obj = read_csv(v)
                        mpfile.document[root_key].pop(table_name)
                        mpfile.document[root_key].rec_update(nest_dict(
                            pandas_to_dict(pd_obj), [k]
                        ))
                        # make default plot (add entry in 'plots') for each
                        # table, first column as x-column
                        mpfile.document[root_key].rec_update(nest_dict(
                            {'x': pd_obj.columns[0], 'table': table_name},
                            [mp_level01_titles[2], 'default {}'.format(k)]
                        ))
        return mpfile

    def get_string(self):
        lines, scope = [], []
        table_start = mp_level01_titles[1]+' '
        for key,value in self.document.iterate():
            if key is None and isinstance(value, dict):
                pd_obj = pandas.DataFrame.from_dict(value)
                csv_string = pd_obj.to_csv(index=False, float_format='%g')[:-1]
                lines += csv_string.split('\n')
            else:
                level, key = key
                # truncate scope 
                level_reduction = bool(level < len(scope))
                if level_reduction: del scope[level:]
                # append scope and set delimiters
                if value is None:
                    is_table = key.startswith(table_start)
                    if is_table:
                        # account for 'data ' prefix
                        key = key[len(table_start):]
                        start, end = '\n[+', ']'
                    else:
                        start, end = '\n{', '}'
                    scope.append(key.replace(' ', '_'))
                # correct scope to omit internal 'general' section
                scope_corr = scope
                if scope[0] == mp_level01_titles[0]:
                    scope_corr = scope[1:]
                # insert scope line
                if (value is None and scope_corr)or \
                   (value is not None and level_reduction):
                    lines.append(start+'.'.join(scope_corr)+end)
                # insert key-value line
                if value is not None:
                    lines.append(make_pair(key.replace(' ', '_'), value))
        return '\n'.join(lines) + '\n'

MPFileCore.register(MPFile)
