export const getResult = (name) => {
    const query = {query: name};
    console.log(JSON.stringify(query))
    const URL = `http://167.99.3.111:5001/simple`;
    return fetch(URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify(query)
    })
            .then((res) => {console.log(JSON.parse(res._bodyInit))});
}