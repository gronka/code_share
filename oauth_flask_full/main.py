from app import app, socketio
import routes
import sroutes


if __name__ == '__main__':
    # TODO: Enable encryption by running server on HTTPS
    socketio.run(app, debug=True)
