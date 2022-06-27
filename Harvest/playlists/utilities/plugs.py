import random as rand

def random(dataset, previous_choices = None):
    """
        random(dataset, previous_choices)

        returns a completely random choice in the dataset, possibly repeating
        the previous values. The +previous_choices+ argument is just a
        placeholder to equalize the call with the exclusive_random() one (see
        below). It can be safely set to None because it is not used here.
    """
    return rand.choice(dataset)

def exclusive_random(dataset, previous_choices):
    remaining_dataset = [d for d in dataset if not d in previous_choices]
    if len(remaining_dataset) < 1:
        remaining_dataset = dataset
    return random(remaining_dataset)
