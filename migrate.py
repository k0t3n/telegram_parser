from database.models import db, Channel, ChannelMessage

db.connect()
db.create_tables([Channel, ChannelMessage])

print('Success!')
