export async function fetchDBLP(dblpid) {
    const loading = async() => {
	const response = await fetch("/api/v1/fetch/DBLP/"+dblpid);
	if (response.status != 200)
	    throw "no response";
	const my_json = await response.text();
	return my_json;
    }
    return loading()
	.catch(error => {
	    let deb = document.getElementById("debuginfo");
	    let r = document.createElement("p")
	    r.textContent="Could not fetch dblp for "+dblpid;
	    deb.appendChild(r);
	    return Promise.reject(error);
	})
	.then(text =>{
	    //console.log(dblpid+" "+text);
	    return JSON.parse(text);
	});
}

export async function fetchTheAdvisor(theadvisorid) {
    const loading = async() => {
	const response = await fetch("/api/v1/fetch/theAdvisor/"+theadvisorid);
	if (response.status != 200)
	    throw "no response";
	const my_json = await response.text();
	return my_json;
    }
    return loading()
	.catch(error => {
	    let deb = document.getElementById("debuginfo");
	    let r = document.createElement("p")
	    r.textContent="Could not fetch theadvisor for "+theadvisorid;
	    deb.appendChild(r);
	    return Promise.reject(error);
	})
	.then(text =>{
	    //console.log(dblpid+" "+text);
	    return JSON.parse(text);
	});
}

//returns an array of promises.
//typically resolve them with Promise.all
export function fetchAllTheAdvisor(theadvisorids) {
    let all_promise = []
    for (let a in theadvisorids) {
	let my_a = theadvisorids[a]
	console.log(my_a);
	all_promise.push(fetchTheAdvisor(my_a));
    }
    return all_promise;
}

export async function query(dblpid) {
    const loading = async() => {
	const response = await fetch("/"+dblpid+"");
	if (response.status != 200)
	    throw "no response";
	const xml = await response.text();
	return xml;
    }
    return loading()
	.catch(error => {
	    let deb = document.getElementById("debuginfo");
	    let r = document.createElement("p")
	    r.textContent="could not fetch dblp for "+dblpid;
	    deb.appendChild(r);
	    return Promise.reject(error);
	})
	.then(text =>{
	return parseXml(text);
    });
}

export function printpaper(dblppaper) {
    console.log(papertostring(dblppaper));
}

export function mylocallog(error) {
    console.error(error);
    let deb = document.getElementById("debuginfo");
    let r = document.createElement("p")
    r.textContent="Something went wrong in processing data. Cause: "+error.toString();
    if ('stack' in error) {
	r.textContent+= ". stack: "+error.stack;
    }
    deb.appendChild(r);
}


export function make_theadvisor_paper_p (paper) {
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
    return newp
}

export function render_theadvisor_papers(domelem, papers) {
    for (let idx in papers) {
	let pap = papers[idx];
	
	domelem.appendChild(make_theadvisor_paper_p(pap));
    }
}
