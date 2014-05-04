

def decode_token(token):
    try:
        from time import strptime
        li = token.split("andsignedat")
        name = li[0].replace("-iam", "")
        stime = li[1].replace("-", "")
        return name, strptime(stime, "%d%b%Y%H:%M:%S")
    except Exception:
        raise Exception("Token parse error")


class User():

    def __init__(self, username, password):
        self.token = None
        self.username = username
        self.password = password

    def create_token(self):
        from time import gmtime, strftime
        n = strftime("%d%b%Y%H:%M:%S", gmtime())
        self.token = t = "-iam{0}andsignedat{1}-".format(self.username, n)
        return t

    def is_token_valid(self, t):
        # TODO: verify expiration
        return self.token == t

    def to_json(self):
        return {}

    def from_json(self, d):
        pass
