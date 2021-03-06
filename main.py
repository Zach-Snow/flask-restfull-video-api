from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import *

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Only run once at the start to create the database
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"


# db.create_all() --This should be run only once at the start of the app, commented out because if ran each time, db will reinitialize each time.

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="View of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="likes of the video is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="View of the video is required")
video_update_args.add_argument("likes", type=int, help="likes of the video is required")

video_delete_args = reqparse.RequestParser()
video_delete_args.add_argument("name", type=str, help="Name of the video is required")
video_delete_args.add_argument("views", type=int, help="View of the video is required")
video_delete_args.add_argument("likes", type=int, help="likes of the video is required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Videos(Resource):
    @marshal_with(resource_fields)
    def get(self):
        try:
            result = VideoModel.query.all()
            if not result:
                result = abort(404, "There is no videos here.....")
            return result
        except ValueError:
            pass


class Video(Resource):

    @marshal_with(resource_fields)
    def get(self, video_id):
        try:
            result = VideoModel.query.filter_by(id=video_id).first()
            if not result:
                result = abort(404, "There is no result in this id.....")
            return result

        except ValueError:
            pass

    @marshal_with(resource_fields)
    def put(self, video_id):
        try:
            args = video_put_args.parse_args()
            result = VideoModel.query.filter_by(id=video_id).first()
            if result:
                abort(409, "Video id already exists......")

            video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
            db.session.add(video)
            db.session.commit()
            return video, 201

        except ValueError:
            pass

    @marshal_with(resource_fields)
    def patch(self, video_id):
        try:
            args = video_update_args.parse_args()
            result = VideoModel.query.filter_by(id=video_id).first()
            if not result:
                abort(404, "Video does not exist, cannot update!")
            if args['name']:
                result.name = args['name']
            if args['views']:
                result.views = args['views']
            if args['likes']:
                result.views = args['likes']

            db.session.commit()

            return result

        except ValueError:
            pass

    @marshal_with(resource_fields)
    def delete(self, video_id):
        try:
            args = video_delete_args.parse_args()
            result = VideoModel.query.filter_by(id=video_id).first()
            if not result:
                abort(404, "Video does not exist, cannot delete!")
            db.session.delete(result)
            db.session.commit()
            return result, 202

        except ValueError:
            pass


api.add_resource(Video, "/video/<int:video_id>")
api.add_resource(Videos, "/videos")


if __name__ == "__main__":
    app.run(debug=True)
