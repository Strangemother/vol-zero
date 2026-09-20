"""Assembly program readers."""


class Reader:
    """Resolve a recorded program into flat assembly text."""

    def __init__(self, asm):
        self.asm = asm
        self.total = 0
        self.resolved_lines = ""

    def as_list(self):
        r = []
        for item, args, kwargs in self.asm._lines:
            r.append(item.resolve(args, kwargs))
        return r

    def flat_resolve(self):
        resolved_lines = self.as_list()
        self.total = len(resolved_lines)
        self.resolved_lines = "\n".join(resolved_lines)
        return self.resolved_lines
