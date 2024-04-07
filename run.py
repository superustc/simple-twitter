from simple_twitter import app, socketio

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, debug=True)
