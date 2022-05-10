class ReachedMaxNumberGroups(Exception):
    # def __init__(self, *args):
    #     if args:
    #         self.message = args[0]
    #     else:
    #         self.message = None

    def __str__(self):
        return "This user reached max number of groups."
