def unload_candidates(new_modules : set):
    return {x for x in new_modules if is_candidate_for_reload(x)}

def is_candidate_for_reload(x):
    return not x.startswith('_pytest') and not x.startswith('py.')