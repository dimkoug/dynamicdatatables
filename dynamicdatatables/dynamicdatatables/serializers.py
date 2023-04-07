from rest_framework import serializers
class DynamicBaseSerializer(serializers.BaseSerializer):
    class Meta:
        fields = None

    def __init__(self, instance=None, data=None, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(instance, data, **kwargs)
        fields = []
        for key in self.request.query_params.dict().keys():
            if 'fields' in key:
                fields.append(self.request.query_params.get(key))
        if fields:
            self.Meta.fields = fields

    def to_representation(self, instance):
        output = {}
        for attribute_name in dir(instance):
            if attribute_name in self.Meta.fields:
                attribute = getattr(instance, attribute_name)
                if attribute_name.startswith('_'):
                    pass
                elif hasattr(attribute, '__call__'):
                     # Ignore methods and other callables.
                    pass
                elif isinstance(attribute, (str, int, bool, float, type(None))):
                    # Primitive types can be passed through unmodified.
                    output[attribute_name] = attribute
                elif isinstance(attribute, list):
                    # Recursively deal with items in lists.
                    try:
                        output[attribute_name] = [
                            self.to_representation(item) for item in attribute
                        ]
                    except:
                        pass
                elif isinstance(attribute, dict):
                    # Recursively deal with items in dictionaries.
                    try:
                        output[attribute_name] = {
                            str(key): self.to_representation(value)
                            for key, value in attribute.items() }
                    except:
                        pass
                else:
                    # Force anything else to its string representation.
                    output[attribute_name] = str(attribute)
        return output