const deleteInput = (inputId) => {
    const blankChildren = domObj => {
        if (domObj.tagName === 'input') {
            domObj.value = '<DELETED>'
        } else if (domObj.tagName === 'div') {
            domObj.children.foreach(blankChildren)
        }
    };
    let div = document.getElementById(inputId);
    blankChildren(div);
    div.hidden = true;
}