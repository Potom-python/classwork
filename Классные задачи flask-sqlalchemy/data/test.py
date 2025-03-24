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
# новости с id = 999 нет в базе

print(delete('http://localhost:8080/api/jobs/5').json())
