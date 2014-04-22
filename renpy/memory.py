# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file contains functions used to help debug memory leaks. They aren't
# called by default, but can be used when problems occur.

old_memory = { }

def memory_profile():
    """
    Calling this function displays the change in the number of instances of
    each type of object.
    """

    print "- Memory Profile ---------------------------------------------------"

    import gc
    gc.collect()

    objs = gc.get_objects()

    c = { } # count

    for i in objs:
        t = type(i)
        c[t] = c.get(t, 0) + 1

    results = [ (count, ty) for ty, count in c.iteritems() ]
    results.sort()

    for count, ty in results:
        diff = count - old_memory.get(ty, 0)
        old_memory[ty] = count
        if diff:
            print diff, ty

    del objs


def find_parents(cls):
    """
    Finds the parents of every object of type `cls`.
    """

    # GC to save memory.
    import gc
    import types
    gc.collect()

    objs = gc.get_objects()

    def print_path(o):

        prefix = ""

        seen = set()
        queue = [ ]

        for _i in range(30):

            print prefix + str(id(o)), type(o),

            try:
                if isinstance(o, dict) and "__name__" in o:
                    print o["__name__"],
                print repr(o)#[:1000]
            except:
                print "Bad repr."

            found = False

            for i in gc.get_referrers(o):

                if i is objs:
                    continue

                if id(i) in seen:
                    continue

                if isinstance(i, types.FrameType):
                    continue

                seen.add(id(i))
                queue.append((i, prefix + "  "))
                found = True
                break

            if not queue:
                break

            if not found:
                print "<no parent, popping>"

            o, prefix = queue.pop()

    for o in objs:
        if isinstance(o, cls):
            print
            print_path(o)
