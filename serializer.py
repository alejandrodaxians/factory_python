import json
import xml.etree.ElementTree as et


class SerializerFactory:
    def get_serializer(self, format):
        try:
            if format == 'JSON':
                return JsonSerializer()
            elif format == 'XML':
                return XmlSerializer()
        except ValueError as ve:
            raise ve


factory = SerializerFactory()


class ObjectSerializer:
    def serialize(self, serializable, format):
        serializer = factory.get_serializer(format)
        serializable.serialize(serializer)
        return serializer.to_str()


class JsonSerializer:
    def __init__(self):
        self._current_object = None

    def start_object(self, object_name, object_id):
        self._current_object = {
            'id': object_id
        }

    def add_property(self, name, value):
        try:
            self._current_object[name] = value
        except TypeError as te:
            raise te

    def to_str(self):
        return json.dumps(self._current_object)


class XmlSerializer:
    def __init__(self):
        self.element = None

    def start_object(self, object_name, object_id):
        self._element = et.Element(object_name, attrib={'id': object_id})

    def add_property(self, name, value):
        prop = et.SubElement(self._element, name)
        prop.text = value

    def to_str(self):
        return et.tostring(self._element, encoding='unicode')
