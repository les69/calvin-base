import facebook
import json
import ast


#this should not be here
def get_attribute(json_file, property):
    js_object =json.loads(open(json_file).read())

    if js_object[property] is None:
        raise AttributeError("No property matching %s" % property)
    return js_object[property]


class FacebookPost(object):

    def __init__(self):
        self.name = None
        self.link = None
        self.caption = None
        self.description = None
        self.picture = None

    def _try(self, dict):
        try:
            return dict.__dict__
        except:
            return str(dict)

    def to_JSON(self):
        return ast.literal_eval(json.dumps(self, default=lambda val: self._try(val),
                          sort_keys=True, indent=0, separators=(',',':')).replace('\n', ''))


class FacebookUser(object):

    def __init__(self, config):
        #self.fb_user = facebook.GraphAPI(access_token=config['access_token'])
        self.fb_user = facebook.GraphAPI(access_token=get_attribute(config, 'access_token'))


    def post_message(self, message, attachment):
        self.fb_user.put_wall_post(message=message, attachment=attachment)

    def post_picture(self, picture, message, album = None):
        fb_picture = open(picture, 'rb')

        if album is None:
            self.fb_user.put_photo(image=fb_picture, message=message)
        else:
            self.fb_user.put_photo(image=fb_picture, message=message, album_id=album)

