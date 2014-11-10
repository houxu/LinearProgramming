# https://class.coursera.org/linearprogramming-002/assignment/view?assignment_id=5
import copy

def readDictDataFromFile(input_file):
    """ Read the data from the dictionary file and format the data
    """
    with open(input_file) as f:
        data_list = f.read().strip().split("\n")

        # split the every line
        data_list = [line.strip().split() for line in data_list]

        # get the m and n
        m, n = [int(x) for x in data_list[0]]

        # get the basic indices m integers and sort the order
        B = [int(x) for x in data_list[1]]

        # get N -- the non-basic indices n integers
        N = [int(x) for x in data_list[2]]

        # get b
        b = [float(x) for x in data_list[3]]

        # get row coefficients
        a = []
        for row in xrange(4, 4 + m):
            a.append([float(x) for x in data_list[row]])

        # get objective coefficients
        z0 = float(data_list[-1][0])
        c = [float(x) for x in data_list[-1][1:]]

        return (m, n, B, N, b, a, z0, c)


class PL_Dictionary(object):
    """ Represent the dictionary in the Simplex pivoting algorithm
    """
    def __init__(self, m, n, B, N, b, a, z0, c):
        self.m = m
        self.n = n
        self.B = B
        self.N = N
        self.b = b
        self.a = a
        self.z0 = z0
        self.c = c

    def __repr__(self):
        """ print out as the same as input
        """
        stringList = []
        stringList.append(" ".join([str(self.m), str(self.n)]) + "\n")
        stringList.append(" ".join([str(x) for x in self.B]) + "\n")
        stringList.append(" ".join([str(x) for x in self.N]) + "\n")

        for rowList in self.a:
            stringList.append(" ".join([str(x) for x in rowList]) + "\n")

        stringList.append(str(self.z0) + " " + " ".join([str(x) for x in self.c]))
        return "".join(stringList)

    def __str__(self):
        return self.__repr__()

    def sortDict(self):
        """ Order the dictionary by the indices
        """
        # sort B
        tmpSortedB = sorted(enumerate(self.B), key = lambda x: x[1])
        self.B = [x[1] for x in tmpSortedB]
        indexB = [x[0] for x in tmpSortedB]

        # sort N
        tmpSortedN = sorted(enumerate(self.N), key = lambda x: x[1])
        self.N = [x[1] for x in tmpSortedN]
        indexN = [x[0] for x in tmpSortedN]

        # sort b according to B
        tmp_b = copy.copy(self.b)
        self.b = [tmp_b[i] for i in indexB]

        # sort a according to B and N
        # sorted by B
        tmp_a = copy.deepcopy(self.a)
        tmp_a_by_B = [tmp_a[i] for i in indexB]
        # sorted by N
        self.a = []
        for rowList in tmp_a_by_B:
            self.a.append([rowList[i] for i in indexN])

        # sort c by N
        tmp_c = copy.copy(self.c)
        self.c = [tmp_c[i] for i in indexN]

    def pivotStep1(self):
        """ the pivot in the Simplex algorithm
            @ return
            ID of entering variable 
            ID of leaving variable 
            Objective Value in Next Dictionary
        """
        # determine the enter variable
        flagEnter = False
        for index, value in enumerate(self.c):
            if value > 0:
                flagEnter = True
                indexEnter = index
                EnterVariable = self.N[indexEnter]
                break

        if flagEnter is False: # There is no enter variable
            return "No Entering Variable"

        else: # there is an entering variable to find leaving variable
            # get the col of indexEnter
            col_a_indexEnter = [(self.a[row][indexEnter], row) for row in xrange(len(self.a))]
            # get the item which is < 0 in col_a_indexEnter
            col_a_indexEnter_filter = [(x[0], x[1]) for x in col_a_indexEnter if x[0] < 0] 
            # print col_a_indexEnter_filter
            if len(col_a_indexEnter_filter) == 0:
                # there is no leaving variable
                return "UNBOUNDED"

            else:
                # get the lower bound for all potential enter variable
                a_LowerBound_indexEnter = [(self.b[i] / (-1 * v), i) for (v, i) in col_a_indexEnter_filter]
                # print a_LowerBound_indexEnter
                # target leaving 
                targetLeaving = min(a_LowerBound_indexEnter)
                leavingIndex = targetLeaving[1]
                leavingVariable = self.B[leavingIndex]
        
        lowerBound = targetLeaving[0]
        new_z0 = self.z0 + lowerBound * self.c[indexEnter]
        return "\n".join([str(EnterVariable), str(leavingVariable), str(new_z0)])



# def main():
#     (m, n, B, N, b, a, z0, c) = readDictDataFromFile('./assignmentParts/part1.dict')
#     tmpDic = PL_Dictionary(m, n, B, N, b, a, z0, c)

def test():
    input_files = ["./unitTests/dict" + str(i) for i in xrange(1, 11)]
    for input_file in input_files:
        (m, n, B, N, b, a, z0, c) = readDictDataFromFile(input_file)
        tmpDic = PL_Dictionary(m, n, B, N, b, a, z0, c)
        tmpDic.sortDict()
        print tmpDic.pivotStep1()
        print "**", input_file
        test_file = input_file + '.output'
        with open(test_file) as f:
            print f.read()

        print "--------------\n"
        # input_file = "./unitTests/dict5"
        # (m, n, B, N, b, a, z0, c) = readDictDataFromFile(input_file)
        # tmpDic = PL_Dictionary(m, n, B, N, b, a, z0, c)
        # tmpDic.sortDict()
        # print tmpDic.pivotStep1()


def main():
    input_files = ["./assignmentParts/part" + str(i) + ".dict" for i in xrange(1, 6)]
    for f in input_files:
        (m, n, B, N, b, a, z0, c) = readDictDataFromFile(f)
        tmpDic = PL_Dictionary(m, n, B, N, b, a, z0, c)
        tmpDic.sortDict()
        resStr = tmpDic.pivotStep1()

        # write the result to a new file
        file_name = f + ".output"
        with open(file_name, 'w') as ff:
            ff.write(resStr)



if __name__ == '__main__':
    # test()
    main()

