import requests
import tornado
import tornado.web
import tornado.options
import json
import urllib
import base64
import time
import changeinput
import alexjudge


class Handlers(tornado.web.RequestHandler):
    def get(self):
        print("233post")

    def post(self):
        """
        获取post的内容
        """
        filename = "./img/" + str(int(time.time() * 1000)) + ".jpg"
        st = self.request.body
        j = json.loads(st)
        basestr = j["jas"]
        imgdata = base64.b64decode(basestr)
        file = open(filename, 'wb')
        file.write(imgdata)
        file.close()
        """
        压缩图像至450
        """
        changeinput.changes(filename)
        global net
        ans = net.judge(filename)

        self.write(ans)


if __name__ == "__main__":
    net = alexjudge.Alexjudge()
    app = tornado.web.Application([(r"/finger", Handlers)])
    app.listen(1025)
    tornado.ioloop.IOLoop.current().start()
