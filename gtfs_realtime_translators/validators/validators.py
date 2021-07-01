class RequiredFieldValidator:
    @staticmethod
    def validate_field_value(fieldName, fieldValue):
        if fieldValue is None:
                raise ValueError('{} is required.'.format(fieldName))
