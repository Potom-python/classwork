from data.db_session import global_init, create_session
from data.users import User
from data.jobs import Jobs


name_bd = input()
global_init(name_bd)
db_sess = create_session()
for user in db_sess.query(User).filter((User.address == 'module_1'), (User.age >= 21)).all():
    user.address = 'module_3'
    db_sess.commit()