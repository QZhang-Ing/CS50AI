import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data

def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    '''
    # People without gene
    zero_gene = set()
    for name in people.keys():
        if name not in one_gene and name not in two_genes:
            zero_gene.add(name)
    '''

    joint_prob = float(1)

    for p in people:
        prob = float(1)
        'one gene case'
        if p in one_gene:
            'first check if person has parents or not'
            if people[p]["mother"] == None:
                prob = PROBS["gene"][1] # unconditional prob
            else:
                m = people[p]["mother"]
                f = people[p]["father"]
                '1 gene from m, not f'
                # compute mother side: pass 1 gene
                if m in one_gene: 
                    prob1 = 0.5 # 0.5 to get the gene
                elif m in two_genes:
                    prob1 = 1 - PROBS["mutation"]
                else:
                    prob1 = PROBS["mutation"]
                # compute father side: pass 0 gene
                if f in one_gene:
                    prob1 *= 0.5
                elif f in two_genes:
                    prob1 *= PROBS["mutation"]
                else:
                    prob1 *= 1 - PROBS["mutation"]
                '1 gene from f, not m'
                'flap the previous case'
                if m in one_gene:
                    prob2 = 0.5
                elif m in two_genes:
                    prob2 = PROBS["mutation"]
                else:
                    prob2 = 1 -  PROBS["mutation"]
                if f in one_gene: 
                    prob2 *= 0.5 # 0.5 to get the gene
                elif f in two_genes:
                    prob2 *= 1 - PROBS["mutation"]
                else:
                    prob2 *= PROBS["mutation"]
                prob = prob1 + prob2
            'probability of trait given 1 gene'
            if p in have_trait:
                prob *= PROBS["trait"][1][True]
            else:
                prob *= PROBS["trait"][1][False]
            # add one gene case to the joint probability
        elif p in two_genes: # two genes case    
            'first check if person has parents or not'
            if people[p]["mother"] == None:
                prob = PROBS["gene"][2] # unconditional prob
            else:
                m = people[p]["mother"]
                f = people[p]["father"]
                'one from each case'
                if m in one_gene:
                    prob = 0.5
                elif m in two_genes:
                    prob = 1 - PROBS["mutation"]
                else: 
                    prob = PROBS["mutation"]
                
                if f in one_gene:
                    prob *= 0.5
                elif f in two_genes:
                    prob *= (1 - PROBS["mutation"])
                else: 
                    prob *= PROBS["mutation"]
            'check trait given two genes'
            if p in have_trait:
                prob *= PROBS["trait"][2][True]
            else:
                prob *= PROBS["trait"][2][False]
            # add one gene case to the joint probability
        else: # zero gene case
            'first check if person has parents or not'
            if people[p]["mother"] == None:
                prob = PROBS["gene"][0] # unconditional prob
            else:
                m = people[p]["mother"]
                f = people[p]["father"]
                'zero from parents'
                if m in one_gene:
                    prob = 0.5
                elif m in two_genes:
                    prob = PROBS["mutation"]
                else:
                    prob = 1 - PROBS["mutation"]
                if f in one_gene:
                    prob *= 0.5
                elif f in two_genes:
                    prob *= PROBS["mutation"]
                else:
                    prob *= 1 - PROBS["mutation"]
            'check trait given zero gene'
            if p in have_trait:
                prob *= PROBS["trait"][0][True]
            else:
                prob *= PROBS["trait"][0][False]

        joint_prob *= prob
    return joint_prob

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:

        # Sum
        gene_sum = sum(probabilities[person]['gene'].values())
        trait_sum = sum(probabilities[person]['trait'].values())

        # Normalize:
        probabilities[person]['gene'] = { genes: (value / gene_sum) for genes, value in probabilities[person]['gene'].items()}
        probabilities[person]['trait'] = { trait: (value / trait_sum) for trait, value in probabilities[person]['trait'].items()}


if __name__ == "__main__":
    main()
