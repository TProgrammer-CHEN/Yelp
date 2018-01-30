# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 12:50:16 2017

@author: Iven
"""

import io
import ijson
from pprint import pprint


class Parser(object):
    """Iterative Parser
    
    Args: 
        file_path
    Usage:
        Users should call get_entries(num) where num
        is the number of lines one needs.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def _read_lines(self):
        """Private function"""
        with open(self.file_path, 'rb') as json_file:
            for line in json_file:
                yield line

    def get_entries(self, num=10):
        """Get `num` of entries. """
        counter = 0
        for line in self._read_lines():
            counter += 1
            for val in ijson.items(io.BytesIO(line), ""):
                val["text"]
                val[""]
            if counter >= num:
                break
                

def test_ijson_reader():
    """Testing ijson"""
    business = "../../data/testParser.json"
    parser = Parser(business)
    jsons = parser.read_lines()
    for i in parser.iter_parse(jsons):
        pprint(i)


def test_get_entries(file_path,l):
    """"""
    parser = Parser(file_path)
    for i in parser.get_entries(3):
        l.append(i)


if __name__ == "__main__":
    # To test the program, chancge the review_path below
    review_path = r"C:\Serious\1stterm\Compsci516\projects\review.json"
    text=[]
    test_get_entries(review_path,text)
    
    
    
    
    