from ..shema.user_shema import UserShema
def user_create_handler(body:UserShema):
    print(body.name)
    print(body.age)