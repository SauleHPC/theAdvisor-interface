//return a DOM element representing a paper from DBLP (from theadvisor service)
export function make_dblp_paper_dom (paper) {
    let newp = document.createElement("p");

    let dblp = document.createElement("span");
    let dblp_a = document.createElement("a");
    dblp_a.text = paper.paper_id;
    dblp_a.href = "https://dblp.org/rec/"+paper.paper_id+".html";
    dblp.appendChild(dblp_a);

    
    let authorspan = document.createElement("span");
    for (let idx in paper.authors) {
	authorspan.innerHTML += paper.authors[idx]
	if (idx < paper.authors.length-1) {
		authorspan.innerHTML += ", ";
	}
	
    }
    authorspan.innerHTML += '. '
    
    let titlespan = document.createElement("span");
    titlespan.innerHTML = paper.title;

    let yearspan = document.createElement("span");
    yearspan.innerHTML = paper.year;

    let doi = document.createElement("span");
    let doi_a = document.createElement("a");
    doi_a.text = paper.doi;
    doi_a.href = "https://dx.doi.org/"+paper.doi;
    doi.appendChild(doi_a);

    let spacer = document.createElement("span");
    spacer.innerHTML = "&nbsp;";

    newp.appendChild(dblp);
    newp.appendChild(authorspan);
    newp.appendChild(spacer.cloneNode(true));
    newp.appendChild(titlespan);
    newp.appendChild(spacer.cloneNode(true));
    newp.appendChild(yearspan);
    newp.appendChild(spacer.cloneNode(true));
    newp.appendChild(doi);
    
    return newp;
}

export function render_dblp_papers(domelem, papers) {
    for (let idx in papers) {
	let pap = papers[idx];
	
	if (pap != null) { //papers could be null if can't be fetched properly
	    domelem.appendChild(make_dblp_paper_dom(pap));
	}
    }
}


//return a DOM element representing a paper from MAG (from theadvisor service)
export function make_mag_paper_dom (paper) {
    let newp = document.createElement("p");

    let mag = document.createElement("span");
    mag.innerText = paper.MAGid
    
    let titlespan = document.createElement("span");
    titlespan.innerHTML = paper.title;

    let yearspan = document.createElement("span");
    yearspan.innerHTML = paper.year;

    let doi = document.createElement("span");
    let doi_a = document.createElement("a");
    doi_a.text = paper.DOI;
    doi_a.href = "https://dx.doi.org/"+paper.DOI;
    doi.appendChild(doi_a);

    let spacer = document.createElement("span");
    spacer.innerHTML = "&nbsp;";

    newp.appendChild(mag);
    newp.appendChild(spacer.cloneNode(true));
    newp.appendChild(titlespan);
    newp.appendChild(spacer.cloneNode(true));
    newp.appendChild(yearspan);
    newp.appendChild(spacer.cloneNode(true));
    newp.appendChild(doi);
    
    return newp;
}



export function render_mag_papers(domelem, papers) {
    for (let idx in papers) {
	let pap = papers[idx];
	
	if (pap != null) { //papers could be null if can't be fetched properly
	    domelem.appendChild(make_mag_paper_dom(pap));
	}
    }
}



//error logging features
export function mylocallog(error) {
    //console.error(error);
    let deb = document.getElementById("debuginfo");
    let r = document.createElement("p")
    r.textContent="Something went wrong in processing data. Cause: "+error.toString();
    if ('stack' in error) {
	r.textContent+= ". stack: "+error.stack;
    }
    deb.appendChild(r);
}

//return a DOM element representing a paper from theadvisor
export function make_theadvisor_paper_dom (paper, investigatelink = false) {
    let newp = document.createElement("p");

    let authorspan = document.createElement("span");
    for (let idx in paper.authors) {
	authorspan.innerHTML += paper.authors[idx]
	if (idx < paper.authors.length-1) {
		authorspan.innerHTML += ", ";
	}
	
    }
    authorspan.innerHTML += '. '
    
    let titlespan = document.createElement("span");
    titlespan.innerHTML = paper.title;

    let yearspan = document.createElement("span");
    yearspan.innerHTML = paper.year;

    let doi = document.createElement("span");
    let doi_a = document.createElement("a");
    doi_a.text = paper.doi;
    doi_a.href = "https://dx.doi.org/"+paper.doi;
    doi.appendChild(doi_a);

    let spacer = document.createElement("span");
    spacer.innerHTML = "&nbsp;";
    
    newp.appendChild(authorspan);
    newp.appendChild(spacer.cloneNode(true));
    newp.appendChild(titlespan);
    newp.appendChild(spacer.cloneNode(true));
    newp.appendChild(yearspan);
    newp.appendChild(spacer.cloneNode(true));
    newp.appendChild(doi);

    if (investigatelink) {
	let invest = document.createElement("a");
	invest.text= "INVESTIGATE";
	invest.href = "investigate_theadvisor.html?id="+paper.theadvisor_id;

	newp.appendChild(spacer.cloneNode(true));
	newp.appendChild(invest);
    }
    
    return newp
}

//papers is an array of papers as formatted by theadvisor
//domelem is the DOM entry to add the papers to
export function render_theadvisor_papers(domelem, papers, investigatelink = false) {
    for (let idx in papers) {
	let pap = papers[idx];
	
	if (pap != null) { //papers could be null if can't be fetched properly
	    domelem.appendChild(make_theadvisor_paper_dom(pap, investigatelink));
	}
    }
    
}

