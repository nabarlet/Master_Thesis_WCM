import re

class PlotRange:
    """
        PlotRange:

        PlotRange is an object that manages ranges in matrix plots.
        Such plots require four numbers to define an actual plot slice:
        * row_start
        * row_end
        * col_start
        * col_end
    """
    def __init__(self, source = None, rstart = 0, rend = None, cstart = 0, cend = None):
        self.source        = source
        self.row_start     = rstart
        self.row_end       = rend
        self.col_start     = cstart
        self.col_end       = cend
        if not self.source:
            rend = cend = ''
            if self.row_end:
                rend = self.row_end
            if self.col_end:
                cend = self.col_end
            self.source = "%s:%sx%s:%s" % (str(self.row_start), str(rend), str(self.col_start), str(cend))

    __RE_RC_SPLITTER__ = re.compile('[xX]')
    @classmethod
    def create(cls, string):
        """
            create(string):

            creates a PlotRange object out of a string observing the following
            format:
            * [row_start][:row_end]x[col_start][:col_end]

            The 'x' character is mandatory, everything else is optional and it
            it going to opt out to defaults (0:end for both dimensions)
        """
        (rows, cols) = cls.__RE_RC_SPLITTER__.split(string)
        (r_start, r_end) = PlotRange.split_dimensions(rows)
        (c_start, c_end) = PlotRange.split_dimensions(cols)
        return cls(string, r_start, r_end, c_start, c_end)
        
    __RE_DIM_SPLITTER__ = re.compile(':')
    @staticmethod
    def split_dimensions(substring):
        start = 0
        end   = None
        if substring:
            unpacked = PlotRange.__RE_DIM_SPLITTER__.split(substring)
            if len(unpacked) == 1:
                start = int(unpacked[0])
            if len(unpacked) == 2:
                if len(unpacked[0]) > 0:
                    start = int(unpacked[0])
                if len(unpacked[1]) > 0:
                    end = int(unpacked[1])
        return [start, end]

    def to_list(self, size = ()):
        (r_end, c_end) = (self.row_end, self.col_end)
        if len(size) == 2:
            (tr_end, tc_end) = size
            if not r_end:
                r_end = tr_end
            if not c_end:
                c_end = tc_end
        return (self.row_start, r_end, self.col_start, c_end)
