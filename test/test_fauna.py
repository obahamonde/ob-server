from test import FQLModel
from uuid import uuid4
from names import get_first_name, get_last_name


class TestModel(FQLModel):
    id :str
    first_name :str
    last_name = str



def test_foo():
    assert True

def test_model():
    assert type(TestModel(id = str(uuid4()), first_name = get_first_name(), last_name = get_last_name())) == TestModel

def test_create():
    assert type(TestModel(id = str(uuid4()), first_name = get_first_name(), last_name = get_last_name()).create()) == dict

def test_save():
    assert type(TestModel(id = str(uuid4()), first_name = get_first_name(), last_name = get_last_name()).save()) == dict

def test_get():
    model_id = str(uuid4())
    TestModel(id = model_id, first_name = get_first_name(), last_name = get_last_name()).create()
    response = TestModel.get("id", model_id)
    assert response['id'] == model_id

def test_delete():
    model_id = str(uuid4())
    TestModel(id = model_id, first_name = get_first_name(), last_name = get_last_name()).create()
    model = TestModel.delete("id", model_id)
    assert model == None

def test_update():
    model_id = str(uuid4())
    TestModel(id = model_id, first_name = get_first_name(), last_name = get_last_name()).create()
    response = TestModel.update("id", model_id, {"first_name": get_first_name()})
    assert response['id'] == model_id