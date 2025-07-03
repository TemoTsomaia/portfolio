class Sun:
    obj = None


    @classmethod
    def inst(cls):
        if cls.obj is None:
            cls.obj = cls()

        return cls.obj

