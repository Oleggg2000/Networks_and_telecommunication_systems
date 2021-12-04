import datetime
import tornado.web
import tornado.ioloop
import tornado.websocket
import time
from xml.etree import ElementTree
import lxml.etree as ET

def parseHtml():
    dom = ET.parse("Source.xml")
    xslt = ET.parse("index.xslt")
    transform = ET.XSLT(xslt)
    newhtml = transform(dom)
    return ET.tostring(newhtml)

def feedbackTime():
    tree = ElementTree.parse("Source.xml")
    root = tree.getroot()
    timer = root.findall("timer")
    print(timer[0].text)
    timer[0].text = str(datetime.datetime.now())
    tree.write("Source.xml")
    return 2

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('webclient.html')

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    clients = []
    fl = True

    def go(self,client):
        if(self.fl):
            client.write_message(parseHtml())
            time.sleep(feedbackTime())
        self.go(client)

    def check_origin(self, origin):
        return True

    def open(self):
        self.clients.append(self)
        self.fl = True
        self.go(self)
        # def on_message(self, message):
        # print("Client message "+message)
    def on_close(self):
        self.fl = False
        self.clients.remove(self)

    def on_message(self, message):
        print(message)

if __name__ == "__main__":
    app = tornado.web.Application([(r"/ws", EchoWebSocket), (r'/', MainHandler)])
    app.listen(10556)
    tornado.ioloop.IOLoop.instance().start()
