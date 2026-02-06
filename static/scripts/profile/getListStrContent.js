/**
 * @param {Element} list
 * @returns {Array}
 */
function getListStrContent(list) {
    if (list) {
        let strContent = [];
        let allergies_lis = list.querySelectorAll('li');
    
        allergies_lis.forEach(li => {
            strContent.push(li.dataset.content);
        });
    
        return strContent;
    }
}