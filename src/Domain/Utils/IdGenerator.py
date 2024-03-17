class IdGenerator:
    _id = 0

    @staticmethod
    def generate_id():
        IdGenerator._id += 1
        return IdGenerator._id