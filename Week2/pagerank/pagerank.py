import os
import random
import re
import sys
import copy
import numpy as np

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probability = {}
    num_links = len(corpus[page])
    if num_links != 0:
        for link in corpus:
            probability[link] = (1 - damping_factor) / len(corpus)
        for link in corpus[page]:
            probability[link] += damping_factor / num_links
    else: # if no outgoing links
        for link in corpus:
            probability[link] = 1 / len(corpus)
    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probability = {}
    for i in corpus:
        probability[i] = 0
    

    # first sample random
    page, _ = random.choice(list(corpus.items()))
    probability[page] += (1/n)
    for i in range(1, n):
        temp_probability = transition_model(corpus, page, damping_factor)
        next_page = []
        weight = []
        for key, value in temp_probability.items():
            next_page.append(key)
            weight.append(value)
        
        page = random.choices(next_page, weight)[0]
        probability[page] += (1/n)
    return probability
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
   
    num = len(corpus)

    # pages with no links
    for page, links in corpus.items():
        if len(links) == 0:
            # links to every pages including itself
            corpus[page] = list(corpus.keys())

    # initialize
    rank = {}
    for i in corpus:
        rank[i] = 1 / num
    # initialize a reversed dictionary containing links to the certain page
    copied = {}
    for page in corpus:
        copied[page] = []
    for page, links in corpus.items():
        for link in links:
            copied[link].append(page)
    previous = np.array(list(rank.values()))
    while True:
        for page in corpus:
            sum_ = 0
            # index through the reversed dic to find totla number linked to the page
            for index in copied[page]:
                sum_ += rank[index] / len(corpus[index])
            # compute the ranking 
            rank[page] = (1 - damping_factor) / num + damping_factor * sum_
        now = np.array(list(rank.values()))
        # if converge
        if (abs(previous - now) <= 0.001).all():
            return rank
        else:
            # update and implement new iteration based on current rank
            previous = now

if __name__ == "__main__":
    main()
