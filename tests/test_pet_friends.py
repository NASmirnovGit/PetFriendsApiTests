from api import PetFriends
from settings import *
import os

pf = PetFriends()


# Positive test


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем что в ответе на запрос приходит статус 200 и в теле ответа есть key"""
    status, result = pf.get_api_key(email, password)

    # Проверка ответа: статус 200 и в теле ответа есть key
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_valid_key(filter=''):
    """Проверяем возможность получения списка питомцев. Статус 200 и список питомцев"""

    # Получаем ключ auth_key и запрашиваем список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверка ответа: Статус 200 и список питомцев
    print(result)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_pet_without_photo_valid(
        name=pet_without_photo['name'], animal_type=pet_without_photo['animal_type'], age=pet_without_photo['age']
):
    """Проверяем возможность добавления питомца без фото.
    Статус 200 в теле ответа есть добаленый питомец с указанным именем"""

    # Получаем ключ auth_key и добавляем нового питомца без фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_without_photo(auth_key, name, animal_type, age)

    # Проверка ответа: Статус 200 в теле ответа есть питомец с указанным именем
    assert status == 200
    assert result['name'] == pet_without_photo['name']


def test_post_pet_with_photo_valid(
        name=pet_without_photo['name'],
        animal_type=pet_without_photo['animal_type'],
        age=pet_without_photo['age'],
        pet_photo='images\Cat.jpeg'
):
    """Проверяем возможность добавления питомца с фото, статус 200  и в теле ответа есть значение pеt_photo"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и добавляем питомца с фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    # Проверка ответа: Статус 200 и в теле ответа есть значение pеt_photo
    assert status == 200
    assert len(result['pet_photo']) > 0


def test_put_new_info_valid(
        name=pet_new_info['name'],
        animal_type=pet_new_info['animal_type'],
        age=pet_new_info['age']):
    """Проверяем возможность изменения информации о питомце"""
    # Получаем ключ auth_key, pet_id, которого будем менять, меняем данный питомца с pet_id
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')
    status, result = pf.put_new_info(auth_key, name, animal_type, age, pet_id['pets'][0]['id'])

    # Проверка ответа: статус 200 и в теле ответа новое имя
    assert status == 200
    assert result['name'] == pet_new_info['name']


def test_post_new_foto_for_pet_valid(pet_photo='images\Dog.jpeg'):
    """Проверяем возможность добавления или изменения фото питомцу,
    статус 200 и в теле ответа есть значение pеt_photo"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key, id питомца и добавляем фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')
    status, result = pf.post_new_foto_for_pet(auth_key, pet_id['pets'][0]['id'], pet_photo)

    # Проверка ответа: Статус 200 и в теле ответа есть значение pеt_photo
    assert status == 200
    assert len(result['pet_photo']) > 0


def test_delete_pet_pass():
    """Проверяем возможность удаления существующего питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(pet_id['pets']) == 0:
        pf.status, result = pf.post_pet_without_photo(auth_key, 'Bill', 'Dog', '4')
        _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    status, result = pf.delete_pet(auth_key, pet_id['pets'][0]['id'])

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    '''Проверяем, что статус ответа равен 200, в списке питомцев нет id удалённого питомца, так же что ответ пустой,
    т.к. пока нет уведомления'''
    assert status == 200
    assert pet_id['pets'][0]['id'] not in my_pets.values()
    assert len(result) == 0


# Negative test


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверяем статус 403 и сообщение, что пользователь не найден"""
    status, result = pf.get_api_key(email, password)

    # Проверка ответа: статус 403 и сообщение об ошибке ( текст ошибки нужно поправить)
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result


def test_get_list_of_pets_invalid_key(filter=''):
    """Проверяем возможность получения списка питомцев c невалидным auth_key. Статус 403 и сообщение"""

    # Получаем ключ auth_key и запрашиваем список всех питомцев
    auth_key = {'key': ''}
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверка ответа: Статус 403 и сообщение об ошибке ( текст ошибки нужно поправить)
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27; Header' in result


def test_post_new_pet_with_empty_data(name='', animal_type='', age=''):
    """Проверяем возможность добавления c пустыми данными.
    Статус 400 в теле ответа сообщение что поля name, animal_type, age обязательные"""

    # Получаем ключ auth_key и добавляем нового питомца без фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_without_photo(auth_key, name, animal_type, age)

    # Проверка ответа: Статус 400, что поля name, animal_type, age обязательные
    assert status == 400
    assert 'Name, animal_type, age is required' in result


def test_delete_not_my_pet_pass():
    """Проверяем возможность удаления чужого питомца"""
    # Получаем ключ auth_key, и проверяем есть ли свои питомцы
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')
    """Проверяем - если список своих питомцев не пустой,
    то удаляем всех своих питомцев, что бы они не попали во общий список"""
    if len(pet_id['pets']) != 0:
       for i in range(len(pet_id['pets'])):
            _, result = pf.delete_pet(auth_key, pet_id['pets'][i]['id'])

    # Берём id первого питомца из общего списка и отправляем запрос на удаление
    _, pet_id = pf.get_list_of_pets(auth_key, '')
    status, result = pf.delete_pet(auth_key, pet_id['pets'][0]['id'])

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    '''Проверяем, что статус ответа равен 200, в общем списке питомцев нет id удалённого питомца'''
    assert status == 200
    assert pet_id['pets'][0]['id'] not in my_pets.values()
