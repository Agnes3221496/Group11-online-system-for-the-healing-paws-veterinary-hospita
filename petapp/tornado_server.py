
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from petapp import app
from tornado.ioloop import IOLoop

s = HTTPServer(WSGIContainer(app))
s.listen(5000)
IOLoop.current().start()

from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from blogapp import app
from tornado.ioloop import IOLoop

s = HTTPServer(WSGIContainer(app))
s.listen(5000)
IOLoop.current().start()


from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from blogapp import app
from tornado.ioloop import IOLoop

s = HTTPServer(WSGIContainer(app))
s.listen(5000)
IOLoop.current().start()

from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from blogapp import app
from tornado.ioloop import IOLoop

s = HTTPServer(WSGIContainer(app))
s.listen(5000)
IOLoop.current().start()

