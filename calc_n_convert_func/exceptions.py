class FormatError(ValueError):
    def __int__(self, *args):
        if args:
            self.message = args
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'FormatError: {self.message}'
        else:
            return 'FormatError has been raised'


class SizeError(ValueError):
    def __int__(self, *args):
        if args:
            self.message = args
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'SizeError: {self.message}'
        else:
            return 'SizeError has been raised'
