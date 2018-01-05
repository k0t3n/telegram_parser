from database.models import db, Source, Message, User

db.connect()
db.create_tables([Source, Message, User])

print('Success!')
