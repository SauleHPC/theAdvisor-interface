//returns a promise that contains the DBLP object (as stored in theadvisor)
//for dblpid
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

//returns a promise that contains the DBLP object (as stored in theadvisor)
//for dblpid
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
	    try {
		const obj = JSON.parse(text);
		return obj;
	    } catch (s) { //JSON.parse throws SyntaxError on illegal JSON
		return null;
	    }
	});
}

//returns a promise that contains the DBLP object (as stored in theadvisor)
//for dblpid.
//
// That object could be null if the paper can't be fetched for some reason
//
// src should define ['src'] and ['id']
export async function fetchTheAdvisorBySrc(src) {
    const loading = async() => {
	const response = await fetch("/api/v1/fetch/theAdvisor_bysrc", 	{
	    method: "POST",
	    body: JSON.stringify(src),
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
	    r.textContent="Could not fetch theadvisor for "+JSON.stringify(src);
	    deb.appendChild(r);
	    return Promise.reject(error);
	})
	.then(text =>{
	    //console.log(dblpid+" "+text);
	    return JSON.parse(text);
	});
}


//returns an array of promises that contains the different papers requested in theadvisorids.
//typically resolve them with Promise.all
export function fetchAllTheAdvisor(theadvisorids) {
    let all_promise = []
    for (let a in theadvisorids) {
	let my_a = theadvisorids[a]
	//console.log(my_a);
	all_promise.push(fetchTheAdvisor(my_a));
    }
    return all_promise;
}

export function fetchAllTheAdvisorBySrc(srcs) {
    let all_promise = []
    for (let a in srcs) {
	let src = srcs[a]
	console.log(src);
	let prom = fetchTheAdvisorBySrc(src);
	console.log(prom);
	all_promise.push(prom);
    }
    return all_promise;
}
