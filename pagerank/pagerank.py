import os
import random
import re
import sys
import copy

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
    # corpus's keys consist of all pages, each key's value is a list of all pages that can be linked from key

    proba_dict = dict()
    for pg in corpus:
        proba_dict[pg] = 0
    pages_num = len(corpus)
    if corpus[page]:
        for pg in corpus:
            if pg == page:
                proba_dict[pg] += (1-damping_factor)/pages_num
                links_in_pg = len(corpus[pg])
                for p in corpus[pg]:
                    proba_dict[p] += damping_factor/links_in_pg
            else:
                proba_dict[pg] += (1-damping_factor)/pages_num
    else:
        for pg in corpus:
            proba_dict[pg] += damping_factor/pages_num

    return proba_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    current_page = random.choice(list(corpus.keys()))
    page_rank = dict()
    for pg in corpus:
        page_rank[pg] = 0

    sample_num = n

    while n > 0:
        proba = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(proba.keys()), weights=list(proba.values()), k=1)[0]
        page_rank[current_page] += 1/sample_num
        n -= 1
    print(proba)

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    # corpus = {'1': {'2'}, '2': {'1', '3'}, '3': {'2', '5', '4'}, '4': {'2', '1'}, '5': set()}
    for pg in corpus:
        page_rank[pg] = 1.0/len(corpus)

    page_rank, difference = update_rank(corpus, page_rank, damping_factor)
    while difference > 0.001:
        page_rank, difference = update_rank(corpus, page_rank, damping_factor)
    return page_rank


def update_rank(corpus, page_rank, damping_factor):
    d = damping_factor
    max_diff = 0
    rank = copy.deepcopy(page_rank)
    damping_value = (1-d)/len(corpus)
    for page in rank:
        new_value = damping_value
        for key, links in corpus.items():
            if page in links:
                new_value += d*(page_rank[key]/len(links))
            elif not links:
                new_value += d*(page_rank[key]/len(corpus))
        diff = abs(new_value - page_rank[page])
        if diff > max_diff:
            max_diff = diff
        page_rank[page] = new_value

    return page_rank, max_diff


if __name__ == "__main__":
    main()
