<<<<<<< HEAD

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

=======

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

>>>>>>> c1122cfb55214f1604deee58947c5a4bd3038adf
