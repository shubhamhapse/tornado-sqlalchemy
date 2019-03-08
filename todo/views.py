from tornado.web import RequestHandler
import dbhandler
import json
import tornado

class Student(RequestHandler):
    """DB handlar class to handle db operations on student table"""

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self):
        jsonData=dbhandler.list_students()
        self.write(json.dumps({'info':jsonData,'status':'200'}))

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        dbhandler.insert_student(data['name'],data['lastname'])

        # TODO(Shubham): need to check for errors and return appropriate error-code
        self.write(json.dumps({'info':'student added','status':'200'}))

    def put(self):
        data = tornado.escape.json_decode(self.request.body)
        dbhandler.change_student_name(data['student_id'],data['name'])

        # TODO(Shubham): need to check for errors and return appropriate error-code
        self.write(json.dumps({'info':'student updated','status':'200'}))


class Lecture(RequestHandler):
    """DB handlar class to handle db operations on lecture table"""

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self):
        jsonData=dbhandler.list_lectures()
        self.write(json.dumps({'info':jsonData,'status':'200'}))

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        dbhandler.insert_lecture(data['class_name'],data['subject'])

        # TODO(Shubham): need to check for DB errors
        self.write(json.dumps({'info':'class added','status':'200'}))


class Attendees(RequestHandler):
    """DB handlar class to handle db operations on junction table between student and lecture"""

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self):
        jsonData=dbhandler.get_attendance()
        self.write(json.dumps({'info':jsonData,'status':'200'}))

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        dbhandler.assign_student_to_lecture(data['student_id'],data['lecture_id'])

        # TODO(Shubham): need to check for DB errors
        self.write(json.dumps({'info':'Done','status':'200'}))