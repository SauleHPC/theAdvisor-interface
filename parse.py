import gzip
import xml.etree.ElementTree as ET
import sys
import os
import json

class Paper:
    def __init__(self):
        self.paper_id = None
        self.author = []
        self.doi = None
        self.year = None
        self.pages = None
        self.title = None
        self.url = None
        self.published_through = None
        self.citation_count = None
        self.file_source = None
        self.line_number = 0

common_doi_prefixes = ['https://doi.org/',\
                       'http://www.crcnetbase.com/doi/abs/',\
                       'http://doi.ieeecomputersociety.org/',\
                       'https://doi.ieeecomputersociety.org/',\
                       'https://dl.acm.org/doi/',\
                       'https://www.tandfonline.com/doi/full/',\
                       'http://www.tandfonline.com/doi/book/',\
                       'http://doi.acm.org/',\
                       'http://journals.sagepub.com/doi/full/',\
                       'http://www.emeraldinsight.com/doi/full/',\
                       'http://journals.sagepub.com/doi/pdf/',\
                       'http://www.crcnetbase.com/doi/book/',\
                       'https://www.tandfonline.com/doi/abs/',\
                       'http://www.worldscinet.com/doi/abs/',\
                       'http://www.mitpressjournals.org/doi/abs/',\
                       'http://www.tandfonline.com/doi/pdf/',\
                       'http://eudl.eu/doi/']

DBLP_line_count_freq=-1

'''
@brief: used to parse through DBLP and MAG datasets. DBLP being in XML format and MAG being in txt but uses CSV

@author: Davis Spradling
'''

'''
used to parse through DBLP

@param: file_path - file path to access DBLP

@param: callback - methods you want to be executed everytime a paper is parsed

@param: count_to - paper number you want to quit performing callbacks on

@param: start_paper - paper to start performing callbacks on

since values are being parsed using xml it is suggested to make sure that you pass in 0 as the start_paper
'''
        
def parse_DBLP_file(callback, start_paper: int,count_to: int):
    current_paper = None
    paper_title_arr = []
    print (f"in parse_DBLP_FILE {start_paper} {count_to}")
    if(start_paper>=count_to):
        print("Error: Start paper is greater then or equal to end paper. Adjust so that start paper is less then the end paper.")
        sys.stdout.flush()

    with gzip.open('dblp.xml.gz', 'rt', encoding='utf-8') as gz_file:
        count_line = 0
        pap = []
        i = 0
        current_paper = None
        #help us keep track of if we are inside a paper currently
        inside_paper = False
        for current_line in gz_file:
            if i > count_to:
                return paper_title_arr
            
            #check for closing tag first for cases such as
            #</incollection><incollection mdate="2017-07-12" key="reference/cn/Prinz14" publtype="encyclopedia">
            if '</article>' in current_line or '</inproceedings>' in current_line or '</incollection>' in current_line or '</book>' in current_line:
                inside_paper = False
                if current_paper is not None and current_paper.title is not None and current_paper.paper_id is not None:
                    #print("Paper is an Object")
                    #for i in range(len(pap)):
                    #   print(pap[i])
                    if(start_paper<=i):
                        for fnction in callback:
                            fnction(current_paper)
                        paper_title_arr.append(current_paper.title) #do we need to store all that?

                    current_paper = None

                    i+=1

            #check for an opening tag to make a new Paper object
            if '<article' in current_line or '<inproceedings' in current_line or '<incollection' in current_line or '<book' in current_line:
                if not inside_paper:
                    current_paper = Paper()
                    current_paper.file_source = "DBLP"
                    inside_paper = True

            if current_paper:
                if '<author>' in current_line:
                    current_paper.author.append(current_line.replace('<author>', '').replace('</author>', '').strip())
                elif '<year>' in current_line:
                    current_paper.year = current_line.replace('<year>', '').replace('</year>', '').strip()
                elif '<pages>' in current_line:
                    current_paper.pages = current_line.replace('<pages>', '').replace('</pages>', '').strip()
                elif '<ee' in current_line: #DBLP does not have a proper doi field; but lots of DOI in ee
                    doi_value = current_line.replace('<ee', '').replace('</ee>', '').strip()
                    if doi_value.find("doi") != -1 or doi_value.find("DOI") != -1 :
                        start_at = doi_value.find('http') #input validation
                        if start_at != -1:
                            doi_value = doi_value[start_at:]
                        for common_prefix in common_doi_prefixes:
                            doi_value = doi_value.replace(common_prefix, '')
                        
                        current_paper.doi = doi_value
                elif '<title>' in current_line:
                    current_paper.title = current_line.replace('<title>', '').replace('</title>', '').strip()
                elif '<url>' in current_line:
                    current_paper.url = current_line.replace('<url>', '').replace('</url>', '').strip()
                elif 'key="' in current_line:
                    key_start = current_line.find('key="') + 5
                    #end is the parenthesis that close the key
                    key_end = current_line.find('"', key_start)
                    #if a valid key
                    if key_start != -1 and key_end != -1:
                        current_paper.paper_id = current_line[key_start:key_end]

                pap.append(current_line)
                count_line += 1

    return paper_title_arr


'''
used to parse through MAG

@param: callback - methods you want to be executed everytime a paper is parsed

@param: count_to - paper number you want to quit performing callbacks on

@param: start_line - paper to start performing callbacks on
'''

def parse_MAG_file(callback,start_line, count_to):
    cwd = os.getcwd()
    print(cwd)
    file_path = 'Papers.txt.gz'
    line_counter = 0

    if(start_line>=count_to):
        print("Error: Start paper is greater then or equal to end paper. Adjust so that start paper is less then the end paper.")
        sys.stdout.flush()

    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            line_counter += 1
            if(start_line <=line_counter):
                line = line.encode('utf-8', errors='replace').decode('utf-8')
                if(line_counter > count_to):
                    return

                fields = line.strip().split('\t')
                current_paper = Paper()
                # field[0] = the paper's MAG ID
                paper_identification, doi_num, paper_title,year_published, publisher = fields[0], fields[2], fields[4],fields[7], fields[9]
                current_paper.paper_id = paper_identification
                current_paper.published_through = publisher
                current_paper.year = year_published
                current_paper.line_number = line_counter


                if doi_num is not None:
                    current_paper.doi = doi_num
                else:
                    current_paper.doi = None

                current_paper.title = paper_title

                current_paper.file_source = "MAG"
                for fnction in callback:
                        fnction(current_paper)
    return line_counter


'''
Used to parse through files that have already been matched between MAG and DBLP

@param: file_path - file path to where the matched file is

@param: callback - callbacks that you want to be applied when defintion is called
'''

def parse_matching_file(file_path,callback):
    with open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:

            line = line.encode('utf-8', errors='replace').decode('utf-8')

            fields = line.strip().split(',')
            current_paper = Paper()
            dblp_paper_id = fields[4]
            current_paper.paper_id = dblp_paper_id

            current_paper.file_source = "MAG"
            for fnction in callback:
                    fnction(current_paper)



'''
Used to parse through citeseer file

@param: file_path - file path where citeseer is located

@param: callback - callback to be applied when definition is called
'''

def parse_citeseer(file_path,callback, paper_limit):
    current_paper = Paper()
    i = 0
    with gzip.open(file_path, 'rt', encoding='utf-8') as gz_file:
        for line in gz_file:
            if(i>paper_limit):
                return

            line = line.encode('utf-8', errors='replace').decode('utf-8')
            fields = line.strip().split(',')

            if(len(fields)==3):
                current_paper = Paper()
                citeseer_id = fields[0]
                citeseer_cluster = fields[1]
                citeseer_title = fields[2]
                current_paper.paper_id = (citeseer_id,citeseer_cluster)
                current_paper.title = citeseer_title    

                current_paper.file_source = "Citeseer"
                for fnction in callback:
                        fnction(current_paper)
                i+=1
