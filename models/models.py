from mongoengine import *

connect('testing_task_db')

class Payment(Document):
    currency = StringField(max_lenght=7)
    amount = FloatField(min_value=0)
    date_time = DateTimeField()
    description = StringField(max_lenght=1024)
    identeficate = StringField(max_lenght=1024)

