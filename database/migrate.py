from database.models import db, Channel, Message

db.connect()
db.create_tables([Channel, Message])
