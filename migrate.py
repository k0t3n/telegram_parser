from database.models import db, Source, Message

db.connect()
db.create_tables([Source, Message])

print('Success!')
