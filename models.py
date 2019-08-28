from google.appengine.ext import ndb


def user_ancestor(user_id):
    """Constructs a Datastore key for a User entity."""
    return ndb.Key('UserParent', user_id)


class User(ndb.Model):
    """
    A model for representing a user.
    """
    # uniques username for user
    username = ndb.StringProperty(required=True)
    # fullname of user
    fullname = ndb.StringProperty(default='')
    # short description about the user
    bio = ndb.TextProperty(default='')
    # image of user
    photo = ndb.BlobProperty()
    # list of users following
    following = ndb.KeyProperty(kind='User', repeated=True)
    # list of users following user
    followers = ndb.KeyProperty(kind='User', repeated=True)
    # list of keys of tweets of user
    tweets = ndb.KeyProperty(kind='Tweet', repeated=True)


# ancestor(User)
class Tweet(ndb.Model):
    """
    A model for representing a tweet.
    """
    # tweet text
    tweet_text = ndb.TextProperty()
    # image of a tweet
    image = ndb.BlobProperty()
    # time tweet created
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    # time tweet updated
    updated_at = ndb.DateTimeProperty(auto_now=True)