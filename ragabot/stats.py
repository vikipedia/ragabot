import random

def histogram(data):
    """
    data is raga tune as a list of lines.
    every line is a list of swar from the tune.
    """
    hist = {}

    for line in data: #histogram of whats next item
        for i, item in enumerate(line[:-1]):
            itemd = hist.get(item, {})
            itemd[line[i+1]] = itemd.get(line[i+1], 0) + 1
            hist[item] = itemd
            
    return hist

def test_histogram():
    data = """Sa,Re,Ga,Ma,Pa$,Dha,Ni,SA
    SA,Ni,Dha$,Pa,Ma,Ga,Re,Sa
    """
    hist = histogram([line.strip().split(",") for line in data.strip().split("\n")])
    hist1 = {
            "Sa":{"Re":1},
            "Re":{"Sa":1,"Ga":1},
            "Ga":{"Re":1,"Ma":1},
            "Ma":{"Ga":1,"Pa$":1},
            "Pa$":{"Dha":1},
            "Dha":{"Ni":1},
            "Dha$":{"Pa":1},
            "Ni":{"SA":1,"Dha$":1},
            "SA":{"Ni":1},
            "Pa":{"Ma":1}}
    assert hist == hist1

def transition_probability(hist):
    prob = {}
    for k in hist:#compute probabilitis
        total  = sum(hist[k].values())
        prob[k] = {j: v/total for j,v in hist[k].items()}
    return prob

def sample(items, probs):
    r = random.random()
    index = 0
    while(r >= 0 and index < len(probs)):
        r -= probs[index]
        index += 1
    return items[index - 1]


def test_sample():
    probs = {'Pa': 0.40425531914893614,
             'SA': 0.3617021276595745,
             'Dha': 0.19148936170212766,
             'Re': 0.02127659574468085,
             'Ga': 0.02127659574468085}
    keys = [i for i in probs.keys()]
    pvalues = [probs[i] for i in keys]
    samples = [sample(keys, pvalues) for i in range(10000)]
    for item in probs:
        print(item, samples.count(item)/10000)
    assert abs(probs['Pa']-samples.count('Pa')/10000)<0.01
