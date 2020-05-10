from yacs import _VALID_TYPES


class Parameter:
    def __init__(self, value, value_type=None, description=''):
        self.value = value
        self.description = description
        if value_type is not None:
            assert value_type in _VALID_TYPES, ""
            self.type = value_type
        else:
            self.type = type(value)
        self.required = False

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class Required(Parameter):
    def __init__(self, value_type, description=''):
        super(Required, self).__init__(None, value_type=value_type, description=description)
        self.required = True

    def __repr__(self):
        return 'required({})'.format(self.type.__name__)

    def __str__(self):
        return 'required({})'.format(self.type.__name__)
