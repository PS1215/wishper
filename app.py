from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

rooms = {}


def generate_unique_code(length):
    while True:
        code = "".join(random.choice(ascii_uppercase) for _ in range(length))
        if code not in rooms:
            return code


@app.route("/", methods=["GET", "POST"])
def home():
    session.clear()

    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template(
                "home.html",
                error="Please enter a name.",
                code=code,
                name=name
            )

        if join and not code:
            return render_template(
                "home.html",
                error="Please enter a room code.",
                code=code,
                name=name
            )

        room = code

        if create:
            room = generate_unique_code(4)
            rooms[room] = {
                "members": 0,
                "messages": []
            }

            print(f"Created room: {room}")

        elif code not in rooms:
            return render_template(
                "home.html",
                error="Room does not exist.",
                code=code,
                name=name
            )

        session["room"] = room
        session["name"] = name

        print(f"Session created -> Name: {name}, Room: {room}")

        return redirect(url_for("room"))

    return render_template("home.html")


@app.route("/room")
def room():
    room = session.get("room")

    if (
        room is None
        or session.get("name") is None
        or room not in rooms
    ):
        print("Room page denied")
        return redirect(url_for("home"))

    return render_template(
        "room.html",
        code=room,
        messages=rooms[room]["messages"]
    )


@socketio.on("connect")
def handle_connect():
    room = session.get("room")
    name = session.get("name")

    print("\n=== CONNECT EVENT ===")
    print("Name:", name)
    print("Room:", room)
    print("Available rooms:", list(rooms.keys()))

    if not room or not name:
        print("Missing room or name")
        return

    if room not in rooms:
        print("Room not found")
        return

    join_room(room)

    send(
        {
            "name": name,
            "message": "has entered the room"
        },
        to=room
    )

    rooms[room]["members"] += 1

    print(f"{name} joined {room}")
    print("Members:", rooms[room]["members"])


@socketio.on("message")
def handle_message(data):
    room = session.get("room")
    name = session.get("name")

    print("\n=== MESSAGE EVENT ===")
    print("Name:", name)
    print("Room:", room)
    print("Data:", data)

    if room not in rooms:
        print("Room not found!")
        return

    content = {
        "name": name,
        "message": data["data"]
    }

    send(content, to=room)

    rooms[room]["messages"].append(content)

    print("Message broadcasted:", content)


@socketio.on("disconnect")
def handle_disconnect():
    room = session.get("room")
    name = session.get("name")

    print("\n=== DISCONNECT EVENT ===")
    print("Name:", name)
    print("Room:", room)

    if room:
        leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1

        send(
            {
                "name": name,
                "message": "has left the room"
            },
            to=room
        )

        if rooms[room]["members"] <= 0:
            del rooms[room]
            print(f"Deleted room: {room}")

    print(f"{name} disconnected")


if __name__ == "__main__":
    socketio.run(app, debug=True)
