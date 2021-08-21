import json
import re


class BaseOutputter:
    def format(self, lines, docstrings, indent=None):
        raise NotImplementedError()


class StringOutptter(BaseOutputter):
    def detect_insert_point(self, lines, start, end):
        if lines[start - 1].endswith(':') or re.search(r'\):', lines[start - 1]):
            # Found end of signature
            return start
        else:
            for i, line in enumerate(lines[start:end]):
                if line.endswith('):'):
                    # Found end of signature without type
                    return start + i + 1
                elif re.search(r'\):|\)\s*:', line):
                    return start + i + 1
                elif re.search(r'\]:|\]\s*:', line):
                    # Found end of signature type
                    #   def foo(a, b) -> Tuple[
                    #       int,
                    #   ]:
                    #       pass
                    return start + i + 1
                elif re.search(r'->(.*):', line):
                    # Found end of signature with type
                    return start + i + 1

        return start

    def format(self, lines, docstrings, indent=None):
        for d in reversed(docstrings):
            col = d['start_col'] + indent
            ret = []
            for line in d['docstring'].split('\n'):
                if line == '':
                    ret.append('')
                else:
                    ret.append('{0}{1}'.format(' ' * col, line))

            lineno = self.detect_insert_point(
                lines,
                d['start_lineno'],
                d['end_lineno'],
            )

            lines.insert(lineno, '\n'.join(ret))

        return '\n'.join(lines)


class JSONOutputter(BaseOutputter):
    def format(self, lines, docstrings, indent=None):
        results = []
        for d in docstrings:
            col = d['start_col'] + indent
            ret = []
            for line in d['docstring'].split('\n'):
                if line == '':
                    ret.append('')
                else:
                    ret.append('{0}{1}'.format(' ' * col, line))

            results.append({
                'docstring': '\n'.join(ret),
                'start_col': col,
                'start_lineno': d['start_lineno'],
                'end_col': d['end_col'],
                'end_lineno': d['end_lineno'],
            })

        return json.dumps(results)
