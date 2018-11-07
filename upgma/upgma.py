#!/usr/bin/env/python

import sys

class cluster:
    pass

def make_clusters(species):
    clusters = {}
    id = 1
    for s in species:
        c = cluster()
        c.id = id
        c.data = s
        c.size = 1
        c.height = 0
        clusters[c.id] = c
        id = id + 1
    return clusters

def find_min(clu, d):
    mini = None
    i_mini = 0
    j_mini = 0
    for i in clu:
        for j in clu:
            if j>i:
                tmp = d[j -1 ][i -1 ]
                if not mini:
                    mini = tmp
                if tmp <= mini:
                    i_mini = i
                    j_mini = j
                    mini = tmp
    return (i_mini, j_mini, mini)

def regroup(clusters, dist):
    i, j, dij = find_min(clusters, dist)
    ci = clusters[i]
    cj = clusters[j]
    # create new cluster
    k = cluster()
    k.id = max(clusters) + 1
    k.data = (ci, cj)
    k.size = ci.size + cj.size
    k.height = dij / 2.
    # remove clusters
    del clusters[i]
    del clusters[j]
    # compute new distance values and insert them
    dist.append([])
    for l in range(0, k.id -1):
        dist[k.id-1].append(0)
    for l in clusters:
        dil = dist[max(i, l) -1][min(i, l) -1]
        djl = dist[max(j, l) -1][min(j, l) -1]
        dkl = (dil * ci.size + djl * cj.size) / float (ci.size + cj.size)
        dist[k.id -1][l-1] = dkl
    # insert the new cluster
    clusters[k.id] = k

    if len(clusters) == 1:
        return list(clusters.values())[0]
    else:
        return regroup(clusters, dist)

def pprint(tree, len):
    if tree.size > 1:
        sys.stdout.write('[')
        pprint(tree.data[0], tree.height)
        sys.stdout.write('-')
        pprint(tree.data[1], tree.height)
        sys.stdout.write("]:%2.1f" % (len - tree.height)),
    else :
        sys.stdout.write("%s:%2.1f" % (tree.data, len)),

def test():
    species = [ "species 1", "species 2", "species 3", "species 4"]
    matr = [ [ 0., 41., 6., 10.],
             [ 41., 0., 14., 3.],
             [ 6., 14., 0., 11.],
             [ 10., 3., 11., 0.] ]
    clu = make_clusters(species)
    tree = regroup(clu, matr)
    pprint(tree, tree.height)


def main():
    test()

if __name__=="__main__":
    main()