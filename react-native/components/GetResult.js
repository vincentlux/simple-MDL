export const getResult = (name) => {
    let query = name;
    const URL = `http://167.99.3.111:5001/simple`;
    return fetch(URL, query)
            .then((res) => {console.log(res)});
}