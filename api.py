import requests
import json
from requests_toolbelt import MultipartEncoder

class PetFriends:
    """Апи библиотека к веб приложению PetFriends"""
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и password"""
        headers = {'email': email, 'password': password}
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter:str = '') -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON со списком питемцев, фильтр пустой, можено указать фильтр "my_pets"
        , тогда в списке будут только мои питомцы"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_pet_without_photo(self, auth_key: json, name: str, animal_type:str, age: str) -> json:
        """Метод делает запрос к API сервера на добавления питомца без фото и возвращает статус запроса и результат
        в формате JSON с информацией о добавленом питомце"""
        data = MultipartEncoder(fields={'name': name, 'animal_type': animal_type, 'age': age})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def post_pet_with_photo(self, auth_key: json, name: str, animal_type:str, age: str, pet_photo: str) -> json:
        """Метод делает запрос к API сервера на добавление питомца с фото и возвращает статус запроса и результат
        в формате JSON с информацией о добаленом питомце"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def put_new_info(self, auth_key: json, name: str, animal_type:str, age: str, pet_id: str) -> json:
        """Метод делает запрос к API сервера на изменение имени пиомца по указаному ИД и возвращает статус запроса
        и результат в формате JSON с информацией об измененном питомце, фото не меняется"""
        data = MultipartEncoder(
            fields={'name': name, 'animal_type': animal_type, 'age': age})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод делает запрос к API сервера на удаление пиомца по указаному ИД и возвращает статус запроса
        и результат в формате JSON с уведомлением. Уведомления пока нет, приходит пустой JSON"""

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except :
            result = res.text
        return status, result