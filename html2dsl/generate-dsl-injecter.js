const generateDSL = () => {
    return JSON.stringify({
        "type": "div",
        "children": [
            {
                "type": "h1",
                "children": ["Hello, World!"]
            }
        ]
    });
}