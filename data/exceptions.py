class UserNotFoundException(Exception):
    def __str__(self):
        return 'User with given id not found in database'
