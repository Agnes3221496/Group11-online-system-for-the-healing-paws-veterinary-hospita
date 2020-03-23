<<<<<<< HEAD
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from blogapp import app
from tornado.ioloop import IOLoop

s = HTTPServer(WSGIContainer(app))
s.listen(5000)
IOLoop.current().start()
=======
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from blogapp import app
from tornado.ioloop import IOLoop

s = HTTPServer(WSGIContainer(app))
s.listen(5000)
IOLoop.current().start()
>>>>>>> 91a64aee0455ce9262321357b25f9663ca67a86e
