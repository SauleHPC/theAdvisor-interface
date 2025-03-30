
export async function recommendationQuery(sources) {
    const loading = async() => {
	const response = await fetch("/api/v1/citation/recommend", 	{
	    method: "POST",
	    body: JSON.stringify(sources),
	});
	if (response.status != 200)
	    throw "no response";
	const my_json = await response.text();
	return my_json;
    }
    return loading()
	.catch(error => {
	    let deb = document.getElementById("debuginfo");
	    let r = document.createElement("p")
	    r.textContent="Could not get recommendation for " + JSON.stringify(sources);
	    deb.appendChild(r);
	    return Promise.reject(error);
	})
	.then(text =>{
	    //console.log(dblpid+" "+text);
	    return JSON.parse(text);
	});
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

    let authorspan = document.createElement("author");
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
    
    newp.appendChild(authorspan);    
    newp.appendChild(titlespan);
    newp.appendChild(yearspan);
    newp.appendChild(doi);

    if (investigatelink) {
	let invest = document.createElement("a");
	invest.text= "INVESTIGATE";
	invest.href = "investigate_theadvisor.html?id="+paper.theadvisor_id;
	
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

