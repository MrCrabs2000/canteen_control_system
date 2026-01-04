/**
 * @param {Element} allergies_container
 * @returns {Array}
 */
function getAllergies(allergies_container) {
    let allergies = [];
    let allergies_lis = allergies_container.querySelectorAll('li');

    allergies_lis.forEach(li => {
        allergies.push(li.dataset.content);
    });

    return allergies;
}