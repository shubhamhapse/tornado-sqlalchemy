from tornado.httpserver import HTTPServer
from tornado.options import define, options
from tornado.web import Application
from tornado.ioloop import IOLoop
import views
import config
import os
import dbhandler



def main():
    """Construct and serve the tornado application."""

    # create tables if not exists
    dbhandler.create_tables()

    app = Application([
        ('/api/v1/student',views.Student),
        ('/api/v1/class',views.Lecture),
        ('/api/v1/attendees',views.Attendees)
    ])

    http_server = HTTPServer(app)
    http_server.listen(config.application_port)
    print("serving on port",config.application_port)
    IOLoop.current().start()

if __name__ == "__main__":
    main()