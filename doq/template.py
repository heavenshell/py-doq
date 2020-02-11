from jinja2 import (
    Environment,
    FileSystemLoader,
)


class Template:
    def __init__(self, paths):
        self.env = Environment(
            loader=FileSystemLoader(paths),
            autoescape=False,
            auto_reload=False,
        )

    def load(self, params, filename=None):
        filename = filename or 'def.txt'
        template = self.env.get_template(filename)
        return template.render(**params)
