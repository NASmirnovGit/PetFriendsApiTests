from api import PetFriends
from settings import valid_password, valid_email, pet_without_photo
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_pet_without_photo_valid(
        name= pet_without_photo['name'], animal_type= pet_without_photo['animal_type'], age= pet_without_photo['age']
        ):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_without_photo(auth_key, name, animal_type,age)
    assert status == 200
    assert result['name'] == pet_without_photo['name']


def test_post_pet_with_photo_valid(
        name= pet_without_photo['name'],
        animal_type= pet_without_photo['animal_type'],
        age= pet_without_photo['age'],
        pet_photo= 'images\Cat.jpeg'
        ):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == pet_without_photo['name']


def test_put_new_info_valid(name= 'Bill'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')
    status, result = pf.put_new_info(auth_key, name, pet_id['pets'][0]['id'])
    assert status == 200
    assert result['name'] == 'Bill'

def test_delete_pet_pass():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()