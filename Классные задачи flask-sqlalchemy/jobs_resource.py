import flask
from flask_restful import Resource, reqparse
from werkzeug.exceptions import abort

from data import db_session
from data.jobs import Jobs


def abort_if_user_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        abort(404, message=f"job {job_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('team_leader', required=True)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True, type=bool)


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_user_not_found(jobs_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(jobs_id)
        return flask.jsonify({'jobs': job.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'is_finished'))
        })

    def delete(self, jobs_id):
        abort_if_user_not_found(jobs_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(jobs_id)
        session.delete(job)
        session.commit()
        return flask.jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return flask.jsonify({'users': [item.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            id=args['id'],
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        session.add(jobs)
        session.commit()
        return flask.jsonify({'id': jobs.id})
