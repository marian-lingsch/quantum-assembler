def data_result_to_set(result):
    res_set = set()
    for r in result:
        res_set.add((frozenset([(k, v) for k, v in r[0].items()]), r[1], r[2]))
    return res_set
