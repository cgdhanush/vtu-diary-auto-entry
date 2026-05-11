import asyncio
import uvicorn

from backend import app

class UvicornServer(uvicorn.Server):

    def run(self, sockets=None):
        # Proper way: use asyncio to run the server
        asyncio.run(self.serve(sockets=sockets))


if __name__ == "__main__":

    uvconfig = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        use_colors=False,
        ws_ping_interval=None,
    )

    try:
        server = UvicornServer(uvconfig)

        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
        )
    except Exception:
        print("API server failed to start")
        raise
