class MyCONFIG():
    def __init__(self) -> None:
        self.username = "root"
        self.password = "123456"
        self.host = "localhost"

    def get_host(self):
        return self.host
    
    def get_username(self):
        return self.username

    def get_pwd(self):
        return self.password