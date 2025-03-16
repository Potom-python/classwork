from data import db_session
from data.users import User
from data.jobs import Jobs


def main():
    db_session.global_init("db/jobs.db")
    db_sess = db_session.create_session()

    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.surname = "Karl"
    user.name = "Velikiy"
    user.age = 55
    user.position = "captain"
    user.speciality = "pilot"
    user.address = "module_2"
    user.email = "karl_chief@mars.org"
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.surname = "Pol"
    user.name = "Polov"
    user.age = 25
    user.position = "navigator"
    user.speciality = "admin"
    user.address = "module_3"
    user.email = "pol_admin@mars.org"
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.surname = "Kirill"
    user.name = "Ismagilov"
    user.age = 16
    user.position = "janitor"
    user.speciality = "programmer"
    user.address = "module_4"
    user.email = "kirill_janitor@mars.org"
    db_sess.add(user)
    db_sess.commit()

    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()


if __name__ == '__main__':
    main()
