counter = 0

def populate_dblp_mongo(paper, paper_docs):
    global counter
    
    # Paper document that has attributes that every paper needs to be associated with
    paper_document = {
        'paper_id': paper.paper_id,
        'title': paper.title,
        'authors': paper.author,
        'year': paper.year,
        'doi': paper.doi
    }

    paper_docs.append(paper_document)

    # Check if a paper with the same paper_id already exists
    # existing_paper = papers_collection.find_one({'paper_id': paper.paper_id})
    
    # if existing_paper is None:
    # If no paper with the same paper_id exists, insert the document
    #papers_collection.insert_one(paper_document)
    
    counter += 1
    if counter % 100000 == 0:
        print(counter)

    return paper_docs
   

    

    
