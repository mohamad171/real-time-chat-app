import redis
import helper as h
import typer
import threading
import uuid
import json
import sys

app = typer.Typer()

r = redis.Redis()

user_id = uuid.uuid4()
helper = h.Helper(r,uuid=user_id)

def message_handler(pubsub):
    for message in pubsub.listen():
        if message["type"] == "message":
            j_message = json.loads(str(message['data'],encoding="utf-8"))
            if j_message["sender"] != str(user_id):
                if j_message["message"] == "\q":
                    print("User left the chat.")
                    break
                print(j_message["message"])

@app.command()
def join_room(name: str):
    helper.join_room(name,message_handler)
    threading.Thread(target=message_handler,args=(helper.pubsub,)).start()
    message = ""
    while message != "\q":
        message = input("")
        helper.send_message(name,message)
    print("Good bye")
    sys.exit(0)


if __name__ == "__main__":
    app()

