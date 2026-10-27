from consumer.models import WidgetRequest

def  test_widget_request_init():
    request = WidgetRequest(request_id=1, widget_type='type1', widget_id=1, owner='owner1', label='label1', description='desc1')
    assert request.request_id == 1
    assert request.widget_type == 'type1'
    assert request.widget_id  == 1
    assert request.owner == 'owner1'
    assert request.label == 'label1'
    assert request.description == 'desc1'
def test_from_dict():
    data = {
        'request_id': 1,
        'widget_type': 'type1',
        'widget_id': 1,
        'owner': 'owner1',
        'label': 'label1',
        'description': 'desc1',
        'other_attributes': {'attr1': 'value1'}
    }
    request = WidgetRequest.from_dict(data)
    assert request.request_id == 1
    assert request.widget_type == 'type1'
    assert request.widget_id  == 1
    assert request.owner == 'owner1'
    assert request.label == 'label1'
    assert request.description == 'desc1'

def test_s3_key_generator():
    request = WidgetRequest(request_id=1, widget_type='type1', widget_id=1, owner='owner 1', label='label1', description='desc1')
    key = request.s3_key_generator()
    assert key == "widgets/owner-1/1"