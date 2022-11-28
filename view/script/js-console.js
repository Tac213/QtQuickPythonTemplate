const scope = {
    // our custom scope injected into our function evaluation
};

function call(msg) {
    const exp = msg.toString();
    const data = {
        expression: msg,
        result: '',
        error: '',
    };
    try {
        const fun = new Function(`return (${exp})`);
        data.result = JSON.stringify(fun.call(scope), null, 2);
        console.log(data.result);
    } catch (e) {
        data.error = e.toString();
        console.error(data.error);
    }
    return data;
}
