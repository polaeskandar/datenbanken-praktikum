from app import socketio, app

if __name__ == "__main__":
    # TODO CHANGE `allow_unsafe_werkzeug` TO FALSE AND SETUP EVENT BUS IN PRODUCTION!
    socketio.run(app, host="0.0.0.0", port=8000, allow_unsafe_werkzeug=True, debug=True)
