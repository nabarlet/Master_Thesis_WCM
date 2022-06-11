class Anniversary:
    def __init__(self, name, birth, death = None):
        self.name = name
        self.birth = birth
        self.death = death

    def inspect(self):
        res = "class Anniversary:\t%s, born: %s" % (self.name, self.birth)
        if self.death:
            res += " - dead: %s" % (self.death)
        return res
