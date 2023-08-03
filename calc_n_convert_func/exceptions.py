class FormatError(ValueError):
    """
    FormatError is raised if the input data does not match the given pattern.
    """
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
    """
    SizeError is raised if the size of the input data exceeds the allowed size.
    """
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
