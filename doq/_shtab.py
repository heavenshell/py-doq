from argparse import Action

FILE = DIR = {}


class PrintCompletionAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print('Please install shtab firstly!')  # noqa: T001 print found
        parser.exit(0)


def add_argument_to(parser, *args, **kwargs):
    Action.complete = None  # type: ignore
    parser.add_argument(
        '--print-completion',
        choices=['bash', 'zsh', 'tcsh'],
        action=PrintCompletionAction,
        help='print shell completion script',
    )
    return parser
