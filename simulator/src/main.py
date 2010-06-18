
class Car(object):
    __slots__ = [
        'num_tanks',
        'main_chambers',
        'aux_chambers',
        ]
    # ***_chamers is list of chambers
    # each chamber is pair of lists (pipes)
    # each pipe is list of integer (tank numbers starting from 0)

    def __init__(self, num_tanks):
        self.num_tanks = num_tanks
        self.main_chambers = []
        self.aux_chambers = []

    def testFuel(self, fuels):
        # fuels is list of matrices
        
        assert len(fuels) == self.num_tanks
        
        #n = fuels[0].size()
        #pass

def main():
    pass

if __name__ == '__main__':
    main()