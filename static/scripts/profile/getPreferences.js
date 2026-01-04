/**
 * @param {Element} preferences_container
 * @returns {Array}
 */
function getPreferences(preferences_container) {
    let preferences = [];
    let preferences_lis = preferences_container.querySelectorAll('li');

    preferences_lis.forEach(li => {
        preferences.push(li.dataset.content);
    });

    return preferences;
}