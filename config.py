class Config(object):
    # 服务器参数
    host: str = "0.0.0.0"
    port: int = 7860

    def __init__(self):
        pass

    def get_server_argparse(self):
        return {
            'host': self.host,
            'port': self.port
        }
