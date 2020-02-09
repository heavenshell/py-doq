import re

import parso


def sort_by_lineno(key):
    if len(key['defs']):
        return key['defs'][0]['start_lineno']

    return key['start_lineno']


def get_return_type(line):
    matched = re.search(r'\)(.*)->(.*):', line)
    if matched:
        return_type = matched.group()[1:]
        return_type = re.sub(r':$', '', return_type).strip()
        return_type = return_type.replace('->', '').strip()
        return return_type

    return None


def parse_return_type(code, start_lineno, end_lineno):
    lines = code.strip().split('\n')
    lineno = end_lineno - start_lineno
    if lineno == 0:
        # Signature end
        return get_return_type(lines[0])

    for line in lines[0:lineno + 1]:
        return_type = get_return_type(line)
        if return_type:
            return return_type

    return None


def parse_defs(module, ignores=None):   # noqa C901
    if ignores is None:
        ignores = []

    results = []
    for d in module.iter_funcdefs():
        is_doc_exists = True if d.get_doc_node() else False

        (start_lineno, start_col) = d.start_pos
        (end_lineno, end_col) = d.end_pos

        name = d.name.value
        params = []
        is_classmethod = any(
            '@classmethod' in d.get_code() for d in d.get_decorators()
        )

        for i, p in enumerate(d.get_params()):
            if is_classmethod and i == 0:
                # Ignore first argument if method is `@classmethod`.
                continue

            if p.name.value in ignores and i == 0:
                # Method's first variable is maybe `self`.
                continue

            arguments = {'argument': None, 'annotation': None, 'default': None}
            arguments['argument'] = p.name.value
            if p.annotation:
                arguments['annotation'] = p.annotation.get_code().strip()
            if p.default:
                arguments['default'] = p.default.get_code().strip()

            params.append(arguments)

        # parso does not have return type. So parse from signature.
        next_node = d.get_suite().get_first_leaf().get_next_sibling()
        stmt_start_lineno = next_node.start_pos[0] if next_node else 2
        return_type = parse_return_type(
            code=d.get_code(),
            start_lineno=start_lineno,
            end_lineno=stmt_start_lineno - 1,
        )

        results.append({
            'name': name,
            'params': params,
            'return_type': return_type,
            'start_lineno': start_lineno,
            'start_col': start_col,
            'end_lineno': end_lineno,
            'end_col': end_col,
            'is_doc_exists': is_doc_exists,
        })

        nested = parse_defs(d)
        if len(nested):
            results += nested

        nested = parse_classdefs(d)
        if len(nested):
            results += nested

    return results


def parse_classdefs(module):
    results = []

    for c in module.iter_classdefs():
        is_doc_exists = True if c.get_doc_node() else False

        (start_lineno, start_col) = c.start_pos
        (end_lineno, end_col) = c.end_pos

        name = c.name.value
        defs = parse_defs(c, ignores=['self'])
        results.append({
            'name': name,
            'defs': defs,
            'start_lineno': start_lineno,
            'start_col': start_col,
            'end_lineno': end_lineno,
            'end_col': end_col,
            'is_doc_exists': is_doc_exists,
        })

        nested = parse_classdefs(c)
        if len(nested):
            results += nested

    results.sort(key=sort_by_lineno)

    return results


def parse(line, ignores=None):
    m = parso.parse(line)
    results = []
    if 'class' in line:
        results = parse_classdefs(m)

    results += parse_defs(m, ignores=ignores)

    return results
