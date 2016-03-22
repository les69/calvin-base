from facebook_manager import FacebookPost,FacebookUser
from calvin.utilities.utils import absolute_filename
import ast

def absolute_filename(filename):
    """Test helper - get absolute name of file
    @TODO: Possibly not the best way of doing this
    """
    import os.path
    return os.path.join(os.path.dirname(__file__), filename)

post = FacebookPost()
post.name = 'Sad day for Bruxells'
post.caption = 'bruxells'
post.description = 'Today terrorists attacked Bruxelles, 11 dead up to now'
post.picture = 'http://www.international.gouv.qc.ca/Content/Users/Documents/FicheContenu/318.jpg'
post.link = 'localhost'

me = FacebookUser(absolute_filename('config'))
temp = post.to_JSON()
#me.post_message('sadness', temp)
#me.post_message('sadness', {'name' :  post.name, 'caption': post.caption, 'description' : post.description,
#                           'picture' : post.picture, 'link' : post.link })

me.post_picture(absolute_filename('image.jpg'), message= 'hello from pi')