# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# ! /usr/bin/env python
import sys


class Subject:
    # initialized name and value
    def __init__(self, name="", value=0):
        self.name = name
        self.value = value

    # comparison (if needed)
    def __eq__(self, other):
        if (isinstance(other, Subject)):
            return self.name == other.name and self.value == other.value

    # sets name of subject
    def set_name(self, name):
        self.name = name

    # sets value of subject
    def set_value(self, value):
        self.value = value

    # returns current name
    def get_name(self):
        return self.name

    # returns current value
    def get_value(self):
        return self.value


class Object:
    # initialized name and value
    def __init__(self, name="", value=0):
        self.name = name
        self.value = value

    # comparison (if needed)
    def __eq__(self, other):
        if (isinstance(other, Object)):
            return self.name == other.name and self.value == other.value


    # sets name of object
    def set_name(self, name):
        self.name = name

    # sets value of object
    def set_value(self, value):
        self.value = value

    # returns current name
    def get_name(self):
        return self.name

    # returns current value
    def get_value(self):
        return self.value


class ReferenceMonitor:

    # initializes list of subjects and objects as a dictionary
    def __init__(self):
        self.subList = []
        self.objList = []

    # adds subject to list and validates input
    def add_subject(self, sub_cmd, full_cmd):

        if (len(sub_cmd) != 3) or (sub_cmd[2] != 'HIGH' and sub_cmd[2] != 'MEDIUM' and sub_cmd[2] != 'LOW'):
            print("BAD INSTRUCTION   :    " + full_cmd.rstrip())
        else:
            sub = Subject(sub_cmd[1], 0)
            self.subList.append((sub,sub_cmd[2]))
            print("Subject Added    :    " + full_cmd.rstrip())

    # adds object to list and validates input
    def add_object(self, sub_cmd, full_cmd):

        if (len(sub_cmd) != 3) or (sub_cmd[2] != 'HIGH' and sub_cmd[2] != 'MEDIUM' and sub_cmd[2] != 'LOW'):
            print("BAD INSTRUCTION   :    " + full_cmd.rstrip())

        else:
            obs = Object(sub_cmd[1], 0)
            self.objList.append((obs,sub_cmd[2]))
            print("Object Added     :    " + full_cmd.rstrip())

    def read(self, sub_cmd, full_cmd):
        if (len(sub_cmd) != 3):
            print("BAD INSTRUCTION  : " + full_cmd.rstrip())
        else:
            sub_breakage = len(self.subList)-1
            obj_breakage = len(self.objList)-1
            i = 0
            j = 0

            for c in self.subList:
                if (c[0].get_name() == sub_cmd[1]):
                    for g in self.objList:
                        if (g[0].get_name() == sub_cmd[2]):

                            # both subject and object confirmed to be in the list
                            # subject with HIGH clearance can read EVERYTHING
                            if (c[1] == 'HIGH'):
                                index = self.subList.index(c)
                                new_val = c[0]
                                new_val.set_value(g[0].get_value())
                                old = c[1]

                                self.subList[index] = (new_val, old)
                                print("ACCESS GRANTED   :     " + sub_cmd[1] + " reads " + sub_cmd[2])
                                break

                            # subject with MEDIUM clearance can read everything but HIGH clearance objects
                            elif (c[1] == 'MEDIUM'):
                                if (g[1] == 'HIGH'):
                                    print("ACCESS DENIED    :      read " + sub_cmd[1] + " " + sub_cmd[2])
                                else:
                                    index = self.subList.index(c)
                                    new_val = c[0]
                                    new_val.set_value(g[0].get_value())
                                    old = c[1]
                                    print(new_val.get_value())
                                    self.subList[index] = (new_val, old)
                                    print("ACCESS GRANTED   :     " + sub_cmd[1] + " reads " + sub_cmd[2])
                                    break

                            # subject with a LOW clearance can ONLY read LOW clearance objects
                            elif (c[1] == 'LOW'):
                                if (g[1] == 'LOW'):
                                    index = self.subList.index(c)
                                    new_val = c[0]
                                    new_val.set_value(g[0].get_value())
                                    print(new_val.get_value())
                                    old = c[1]
                                    self.subList[index] = (new_val, old)
                                    print("ACCESS GRANTED   :     " + sub_cmd[1] + " reads " + sub_cmd[2])
                                    break
                                else:
                                    print("ACCESS DENIED    :      read " + sub_cmd[1] + " " + sub_cmd[2])
                                    break

                            # if instruction is somehow bad at this point
                            else:
                                print("BAD INSTRUCTION  :    " + full_cmd.rstrip())
                                break
                        # if no object with given name exists
                        elif (j == obj_breakage):
                            print("BAD INSTRUCTION  :    " + full_cmd.rstrip())

                        else:
                            j += 1

                # if no subject with given name exists
                elif (i == sub_breakage):
                    print("BAD INSTRUCTION  :     " + full_cmd.rstrip())

                else:
                    i += 1

    def write(self, sub_cmd, full_cmd):
        # validate input
        if (len(sub_cmd) != 4 or not((sub_cmd[3]).isdigit())):
            print("BAD INSTRUCTION    :      " + full_cmd.rstrip())

        # iterate through the object/subject list to find
        else:
            sub_breakage = len(self.subList)-1
            obj_breakage = len(self.objList)-1
            i = 0
            j = 0
            for c in self.subList:
                if (c[0].get_name() == sub_cmd[1]):
                    for g in self.objList:

                        if (g[0].get_name() == sub_cmd[2]):

                            # subject and object are confirmed to be in the lists
                            # if subject clearance level is HIGH then they can ONLY write to HIGH objects
                            if (c[1] == 'HIGH'):
                                if (g[1] != 'HIGH'):
                                    print("ACCESS DENIED    :      write " + sub_cmd[1] + " " + sub_cmd[2])
                                    break
                                else:
                                    index = self.objList.index(g)
                                    newval = g[0]
                                    newval.set_value(sub_cmd[3])
                                    old = g[1]
                                    self.objList[index] = (newval,old)
                                    print("ACCESS GRANTED   :     " + sub_cmd[1] + " writes " + sub_cmd[2])
                                    break

                            # if subject clearance level is MEDIUM then they cant write to LOW objects
                            elif (c[1] == 'MEDIUM'):
                                if (g[1] != 'LOW'):
                                    index = self.objList.index(g)
                                    newval = g[0]
                                    newval.set_value(sub_cmd[3])
                                    old = g[1]
                                    self.objList[index] = (newval, old)
                                    print("ACCESS GRANTED   :     " + sub_cmd[1] + " writes value " + sub_cmd[3]+ " to "+ sub_cmd[2])
                                    break
                                else:
                                    print("ACCESS DENIED    :      write " + sub_cmd[1] + " " + sub_cmd[2])
                                    break

                            # if subjects clearance level is LOW then they can write to any object
                            elif (c[1] == 'LOW'):
                                index = self.objList.index(g)
                                newval = g[0]
                                newval.set_value(sub_cmd[3])
                                old = g[1]
                                self.objList[index] = (newval, old)

                                print("ACCESS GRANTED   :     " + sub_cmd[1] + " writes " + sub_cmd[2])
                                break

                            # if instructions are some how bad break
                            else:
                                print("BAD INSTRUCTION   :  " + full_cmd)
                                break
                        # if no object with given name exists
                        elif(j == obj_breakage):
                            print("BAD INSTRUCTION   : " + full_cmd.rstrip())
                            break

                        else:
                            j += 1
                # if no subject with given name exists
                elif(i == sub_breakage):
                    print("BAD INSTRUCTION  :    " + full_cmd.rstrip())
                    break
                else:
                    i += 1

    def show_status(self, sub_cmd, full_cmd):
        if(len(sub_cmd) != 1):
            print("BAD INSTRUCTION  :     " + full_cmd.rstrip())
        else:
            print("+--------current state--------+")
            print("|-subject-|--level--|--value--|")

            for i in self.subList:
                print("| " + i[0].get_name() + " |  "+ str(i[1]).ljust(7) + "|  " + str(i[0].get_value()).rjust(7) + "|")
            print("|--object-|--level--|--value--|")
            for j in self.objList:
                print("| " + j[0].get_name() + " |  "+ str(j[1]).ljust(7) + "|  " + str(j[0].get_value()).rjust(7) + "|")
            print("+-----------------------------+")


def read_my_file(args):
    v = ReferenceMonitor()
    try:
        f = open(args, "r")
        for x in f.readlines():
            k = x.split()
            if (k[0] == "addsub"):
                v.add_subject(k, x)
            elif (k[0] == "addobj"):
                v.add_object(k, x)
            elif (k[0] == "read"):
                v.read(k, x)
            elif (k[0] == "write"):
                v.write(k, x)
            elif (k[0] == "status"):
                v.show_status(k, x)
            else:
                print("BAD INSTRUCTION  :  " + x.rstrip())

    except FileNotFoundError:
        print("could not open "+args)
    return True


def main(args):
    read_my_file(args)


if __name__ == '__main__':
    main(sys.argv[1:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
