from views import *

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=HomePage, name='home'),
    webapp2.Route(r'/login', handler=LoginPage, name='login'),
    webapp2.Route(r'/settings', handler=EditProfilePage, name='settings'),
    webapp2.Route(r'/search', handler=SearchPage, name='search'),
    webapp2.Route(r'/profile/<profile_username:\w+>', handler=ProfilePage, name='profile'),
    webapp2.Route(r'/.*', handler=NotFoundPage, name='not_found_page'),
], debug=True)
