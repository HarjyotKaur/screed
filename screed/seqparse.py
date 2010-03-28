# Copyright (c) 2008-2010, Michigan State University

"""
seqparse contains custom sequence parsers for extending screed's
functionality to arbitrary sequence formats. An example 'hava'
parser is included for API reference
"""

import dbConstants
import os
from createscreed import create_db
from openscreed import screedDB
from fastq import fqiter
from fasta import faiter

def read_fastq_sequences(filename):
    """
    Function to parse text from the given FASTQ file into a screed database
    """
    FASTQFIELDTYPES = ('name', 'annotations', 'sequence', 'accuracy')

    # Will raise an exception if the file doesn't exist
    theFile = open(filename, 'rb')

    # Setup the iterator function
    iterfunc = fqiter(theFile)

    # Create the screed db
    create_db(filename, FASTQFIELDTYPES, iterfunc)

    theFile.close()

    return screedDB(filename)

def read_fasta_sequences(filename):
    """
    Function to parse text from the given FASTA file into a screed database
    """

    FASTAFIELDTYPES = ('name', 'description', 'sequence')
    
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Setup the iterator function
    iterfunc = faiter(theFile)

    # Create the screed db
    create_db(filename, FASTAFIELDTYPES, iterfunc)
    
    theFile.close()

    return screedDB(filename)

# Parser for the fake 'hava' sequence
def read_hava_sequences(filename):
    """
    Function to parse text from the given HAVA file into a screed database
    """
    def havaiter(handle):
        """
        Iterator over a 'hava' sequence file, returning records. handle
        is a handle to a file opened for reading
        """
        data = {}
        line = handle.readline().strip()
        while line:
            data['hava'] = line
            data['quarzk'] = handle.readline().strip()
            data['muchalo'] = handle.readline().strip()
            data['fakours'] = handle.readline().strip()
            data['selimizicka'] = handle.readline().strip()
            data['marshoon'] = handle.readline().strip()

            line = handle.readline().strip()
            yield data

    fields = ('hava', 'quarzk', 'muchalo', 'fakours', 'selimizicka', 'marshoon')
        
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Setup the iterator function
    iterfunc = havaiter(theFile)

    # Create the screed db
    create_db(filename, fields, iterfunc)
    theFile.close()

    return screedDB(filename)
