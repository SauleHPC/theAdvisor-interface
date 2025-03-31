
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
