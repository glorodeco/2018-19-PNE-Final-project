class Seq:
    """"A class for rpresenting sequences"""
    def __init__ (self, strbases):

        self.strbases = strbases

    def len(self):
        return len(self.strbases)

    def complement(self):
        complement_sequence=''

        for a in self.strbases:
            if a=='A':
                complement_sequence = complement_sequence+'T'
            elif a=='T':
                complement_sequence = complement_sequence + 'A'
            elif a == 'C':
                complement_sequence = complement_sequence + 'G'
            elif a == 'G':
                complement_sequence = complement_sequence + 'C'

        return complement_sequence

    def reverse(self):
        return self.strbases[::-1]

    def count(self, base):
        counter=self.strbases.count(base)
        return counter
    def perc(self,base):

        tl=len(self.strbases)
        counter=self.strbases.count(base)
        if tl>0:
            perc=round(100.0*counter/tl,1)
        else:
            perc=0

        return perc