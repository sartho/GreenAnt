from Myna import db
from Myna.models import User

u=User.query.filter_by(username='admin').first()
print (u.id)
db.session.delete(u)
db.session.commit()