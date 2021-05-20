import logging

logger = logging.getLogger(__name__)

enabled = True

def pr(n):
    for i in range(2,int(n**(1/2))+1):
        if n%i==0:
            return False
    return (True if n>1 else False)

def get_size(bytes, suffix):
    factor = 1000
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return "{:.1f} {}{}".format(bytes,unit,suffix)
        bytes /= factor

class Conversation:
    def __init__(self, game, engine, xhr, version, challenge_queue):
        self.game = game
        self.engine = engine
        self.xhr = xhr
        self.version = version
        self.challengers = challenge_queue

    command_prefix = "!"

    def react(self, line, game):
        logger.info("*** {} [{}] {}: {}".format(self.game.url(), line.room, line.username, line.text.encode("utf-8")))
        if (line.text[0] == self.command_prefix):
            self.command(line, game, line.text[1:].lower())

    def command(self, line, game, cmd):
        if cmd == "commands" or cmd == "help":
            self.send_reply(line, "Supported commands: !wait, !name, !howto, !eval, !queue")
        elif cmd == "wait" and game.is_abortable():
            game.ping(60, 120)
            self.send_reply(line, "Waiting 60 seconds...")
        elif cmd == "name":
            name = game.me.name
            self.send_reply(line, "{} running {}".format(name, self.engine.name()))
        elif cmd == "howto":
            self.send_reply(line, "Google is your friend.")
        elif cmd == "eval":
            stats = self.engine.get_stats()
            self.send_reply(line, ", ".join(stats))
        elif cmd == "queue":
            if self.challengers:
                challengers = ", ".join(["@" + challenger.challenger_name for challenger in reversed(self.challengers)])
                self.send_reply(line, "Challenge queue: {}".format(challengers))
            else:
                self.send_reply(line, "No challenges queued.")

    def send_reply(self, line, reply):
        self.xhr.chat(self.game.id, line.room, reply)


class ChatLine:
    def __init__(self, json):
        self.room = json.get("room")
        self.username = json.get("username")
        self.text = json.get("text")
