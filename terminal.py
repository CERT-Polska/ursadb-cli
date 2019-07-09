import readline


class SimpleCompleter(object):
    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [
                    s for s in self.options if s and s.startswith(text)
                ]
            else:
                self.matches = self.options[:]

        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


def setup_terminal():
    keywords = [
        "index ",
        "select ",
        "compact",
        "with ",
        "gram3",
        "text4",
        "hash4",
        "wide8",
    ]
    readline.set_completer(SimpleCompleter(keywords).complete)
    readline.parse_and_bind("tab: complete")
