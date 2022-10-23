"""
Copyright 2019, University of Freiburg
Hannah Bast <bast@cs.uni-freiburg.de>
Claudius Korzen <korzen@cs.uni-freiburg.de>
Patrick Brosi <brosi@cs.uni-freiburg.de>
Natalie Prange <prange@cs.uni-freiburg.de>
"""

import os
import re
import sys

class InvertedIndex:
    """
    A simple inverted index as explained in lecture 1.
    """

    def __init__(self):
        """
        Creates an empty inverted index.
        """
        self.inverted_lists = {}  # The inverted lists of record ids.

    def build_from_file(self, file_name):
        """
        Constructs the inverted index from given file in linear time (linear in
        the number of words in the file). The expected format of the file is
        one record per line, in the format
        <title>TAB<description>TAB<num_ratings>TAB<rating>TAB<num_sitelinks>
        You can ignore the last three columns for now, they will become
        interesting for exercise sheet 2.

        TODO: Make sure that each inverted list contains a particular record id
        at most once, even if the respective word occurs multiple times in the
        same record.

        >>> ii = InvertedIndex()
        >>> ii.build_from_file("example.tsv")
        >>> sorted(ii.inverted_lists.items())
        [('a', [1, 2]), ('doc', [1, 2, 3]), ('film', [2]), ('movie', [1, 3])]
        """
        self.file_name = file_name
        with open(file_name, "r", encoding="utf8", newline="\n") as file:
            record_id = 0
            for line in file:
                line = line.strip()
                record_id += 1
                added_words = set()

                for word in re.split("[^A-Za-z]+", line):
                    word = word.lower().strip()

                    # Ignore the word if it is empty.
                    if len(word) == 0:
                        continue

                    if word not in self.inverted_lists:
                        # The word is seen for first time, create a new list.
                        self.inverted_lists[word] = []
                    if word not in added_words:
                        self.inverted_lists[word].append(record_id)
                        added_words.add(word)

    def intersect(self, list1, list2):
        """
        Computes the intersection of the two given inverted lists in linear
        time (linear in the total number of elements in the two lists).

        >>> ii = InvertedIndex()
        >>> ii.intersect([1, 5, 7], [2, 4])
        []
        >>> ii.intersect([1, 2, 5, 7], [1, 3, 5, 6, 7, 9])
        [1, 5, 7]
        """
        pass  # TODO: add your code here

        res = []
        index1 = 0
        index2 = 0
        while index1 != len(list1) and index2 != len(list2):
            if list1[index1] > list2[index2]:
                index2 += 1
                continue
            if list1[index1] < list2[index2]:
                index1 += 1
                continue

            res.append(list1[index1])
            index1 += 1
            index2 += 1
        return res

    def process_query(self, keywords):
        """
        Processes the given keyword query as follows: Fetches the inverted list
        for each of the keywords in the given query and computes the
        intersection of all inverted lists (which is empty, if there is a
        keyword in the query which has no inverted list in the index).

        >>> ii = InvertedIndex()
        >>> ii.build_from_file("example.tsv")
        >>> ii.process_query([])
        []
        >>> ii.process_query(["doc"])
        [1, 2, 3]
        >>> ii.process_query(["doc", "movie"])
        [1, 3]
        >>> ii.process_query(["doc", "movie", "comedy"])
        []
        """
        pass  # TODO: add your code here
        invertedLists = list(map(lambda keyword: self.getInvertedList(keyword), keywords))
        return self.intersectMultiple(invertedLists)

    def getInvertedList(self, keyword):
        clean_keyword = keyword.lower().strip()
        if clean_keyword in self.inverted_lists:
            return self.inverted_lists[clean_keyword]
        return []

    def intersectMultiple(self, listOfLists):
        """
        Computes the intersection of multiple given inverted lists
        """
        if len(listOfLists) == 0:
            return []

        sorted_lists_by_length = sorted(listOfLists, key=lambda list: len(list))
        res = sorted_lists_by_length[0]
        for i, list in enumerate(sorted_lists_by_length, start=1):
            if len(res) == 0:
                break
            res = self.intersect(res, list)
        return res

    def getMoviesByRecordIds(self, record_ids):
        found_movies = []
        record_ids_set = set(record_ids)
        with open(self.file_name, "r", encoding="utf8", newline="\n") as file:
            record_id = 0
            for line in file:
                record_id += 1
                if (record_id not in record_ids_set):
                    continue
                movie = self.parseMovie(line)
                found_movies.append(movie)
                if (len(found_movies) == len(record_ids)):
                    break
        return found_movies

    def parseMovie(self, line):
        columns = re.split("\t", line.strip())
        return Movie(columns[0], columns[1])

    def search(self, search_phrase, count):
        keywords = re.split("[^A-Za-z]+", search_phrase.strip())
        records_ids = self.process_query(keywords)
        return self.getMoviesByRecordIds(records_ids[0:count])

class Movie:
  def __init__(self, title, description):
    self.title = title
    self.description = description

def main():
    """
    Constructs an inverted index from a given text file, then asks the user in
    an infinite loop for keyword queries and outputs the title and description
    of up to three matching records.
    """
    # Parse the command line arguments.
    if len(sys.argv) != 2:
        print("Usage: python3 %s <file>" % sys.argv[0])
        sys.exit()

    file_name = sys.argv[1]

    # Create a new inverted index from the given file.
    print("Reading from file '%s'." % file_name)
    ii = InvertedIndex()
    ii.build_from_file(file_name)

    # TODO: add your code here
    while True:
        print(f'{os.linesep}Please type search query (e.g. "Love story"):')
        search_phrase = str(input())
        movies = ii.search(search_phrase, 3)
        if len(movies) == 0:
            print('Movies with given query not found.')
            continue
        for movie in movies:
            print(f'Movie title: "{movie.title}". Description: "{movie.description}"')

if __name__ == "__main__":
    main()
