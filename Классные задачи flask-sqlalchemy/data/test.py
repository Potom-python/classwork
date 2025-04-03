from requests import get, post, delete

print(get('http://localhost:8080/api/jobs').json())
print(get('http://localhost:8080/api/jobs/1').json())
print(get('http://localhost:8080/api/jobs/999').json())
print(get('http://localhost:8080/api/jobs/q').json())

print(post('http://localhost:8080/api/jobs', json={}).json())  # пустой запрос
print(post('http://localhost:8080/api/jobs',
           json={'job': 'installation of radiation protection'}).json())  # неполный список ключей
print(post('http://localhost:8080/api/jobs',
           json={'job': 'installing a long-distance communication antenna', 'team_leader': 4, 'work_size': 5,
                 'collaborators': '6, 3', 'is_finished': True}).json())  # верный запрос

print(delete('http://localhost:8080/api/jobs/999').json())

print(delete('http://localhost:8080/api/jobs/5').json())

print(get('http://localhost:8080/api/v2/users').json())
print(get('http://localhost:8080/api/v2/users/1').json())

print(post('http://localhost:8080/api/v2/users').json())
print(post('http://localhost:8080/api/v2/users',
           json={'id': 6, 'user': 'bor'}).json())
print(post('http://localhost:8080/api/v2/users',
           json={'id': 1, 'surname': 'borov', 'name': 'bor', 'age': 47, 'email': 'borov@gmail.com'}).json())
print(post('http://localhost:8080/api/v2/users',
           json={'id': 6, 'surname': 'borov', 'name': 'bor', 'age': 47, 'email': 'borov@gmail.com'}).json())

print(delete('http://localhost:8080/api/v2/users/6'))
print(delete('http://localhost:8080/api/v2/users/0'))

