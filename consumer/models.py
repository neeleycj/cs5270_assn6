
class WidgetRequest:
    def __init__(self, request_id, widget_type, owner, label=None, description=None, other_attributes=None):
        self.request_id = request_id
        self.widget_type = widget_type
        self.widget_id= widget_type
        self.owner = owner
        self.label = label
        self.description = description
        self.other_attributes = other_attributes

    def from_dict(data):
        return WidgetRequest(
            request_id=data.get('request_id'),
            widget_type=data.get('widget_type'),
            owner=data.get('owner'),
            label=data.get('label'),
            description=data.get('description'),
            other_attributes=data.get('other_attributes')
        )

    def s3_key_generator(self):
        new_name = self.owner.replace(" ", "-").lower()
        key = f"widgets/{new_name}/{self.widget_id}"
        return key

    def dynamoDB_formatter(self):
        formatted_data = {}
        formatted_data['request_id'] = self.request_id
        formatted_data['owner'] = self.owner
        formatted_data['label'] = self.label
        formatted_data['description'] = self.description
        for key,  value  in self.other_attributes.items():
            formatted_data[key] = value
        return formatted_data
    