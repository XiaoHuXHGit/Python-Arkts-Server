import uvicorn
from fastapi import FastAPI

import ServerInterface
from config import Config

app = FastAPI()
# app 挂载
app.mount("/", ServerInterface.app)

if __name__ == '__main__':
    # server_argparse = Config()
    uvicorn.run(app, host=Config.host, port=Config.port)
