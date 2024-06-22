from redis import Redis
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Helper:
   
   def __init__(self,redis_instance:Redis,uuid) -> None:
      self.redis = redis_instance
      self.pubsub = redis_instance.pubsub()
      self.uuid = uuid
   def join_room(self,room_name):
       self.pubsub.subscribe(room_name)

   def send_message(self,room_name,message):
       self.redis.publish(room_name,json.dumps({"message":f"{bcolors.OKBLUE} {message} {bcolors.ENDC}","sender":str(self.uuid)}))

