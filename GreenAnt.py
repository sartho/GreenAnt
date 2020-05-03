from Myna import Myna, db
from Myna.models import User, Post

@Myna.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
