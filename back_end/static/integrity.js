//returns an  promise that resolves to an array suspicious papers
export async function get_multiple_mag() {
    const loading = async() => {
	const response = await fetch("/api/v1/integrity/multipleMAG");
	if (response.status != 200)
	    throw "no response";
	const my_json = await response.text();
	console.log(my_json);
	return my_json;
    }
    return loading()
	.catch(error => {
	    let deb = document.getElementById("debuginfo");
	    let r = document.createElement("p")
	    r.textContent="Could not fetch multipleMAG";
	    deb.appendChild(r);
	    return Promise.reject(error);
	})
	.then(text =>{
	    console.log(" "+text);
	    try {
		const obj = JSON.parse(text);
		return obj;
	    } catch (s) { //JSON.parse throws SyntaxError on illegal JSON
		return null;
	    }
	});
}
