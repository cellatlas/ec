from collections import defaultdict


def write_markers(fname, markers):
    with open(fname, "w") as f:
        for k, v in markers.items():
            f.write(f"{k}\t")
            n = len(v)
            for idx, i in enumerate(v):
                f.write(f"{i}")
                if idx < n - 1:
                    f.write(",")
            f.write("\n")


def read_markers_str(fname, markers=defaultdict(list)):
    with open(fname, "r") as f:
        for idx, line in enumerate(f.readlines()):
            ct_id, gene_ids = line.strip().split("\t")
            markers[ct_id] = [i for i in gene_ids.split(",")]


def merge(ecs1, ecs2):
    m = defaultdict(set)

    uniq = set(list(ecs1.keys()) + list(ecs2.keys()))
    for k in uniq:
        m[k].update(ecs2.get(k, []))
        m[k].update(ecs1.get(k, []))

    # convert from set to list
    m = dict(zip(m.keys(), map(list, m.values())))
    return m


def ec_merge(ec_a_fn, ec_b_fn, ec_merge_fn):
    ec_a = defaultdict(list)
    read_markers_str(ec_a_fn, ec_a)

    ec_b = defaultdict(list)
    read_markers_str(ec_b_fn, ec_b)

    m = merge(ec_a, ec_b)

    write_markers(ec_merge_fn, m)
