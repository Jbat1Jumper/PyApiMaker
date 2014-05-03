from flask import Flask, Response
from zipfile import ZipFile
import io
import os

app = Flask(__name__)


@app.route("/<res>")
def root(res):
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    with ZipFile("./resources.zip", "r") as z:
        with z.open(res, "r") as f:
            f = io.TextIOWrapper(f)
            m = mimetypes[(os.path.splitext(res)[1])]
            resp = Response(f.read(), mimetype=m)
            resp.headers["Access-Control-Allow-Origin"] = "localhost, "\
                                                          "localhost:16319"
            resp.headers["Access-Control-Allow-Methods"] = "POST, GET"
            return resp


if __name__ == "__main__":
    app.run(port=80, debug=True)
