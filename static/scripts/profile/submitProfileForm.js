/**
 * @param {HTMLFormElement} form
 * @param {Element} hiddenInputsContainer
 * @param {NodeList} allergies
 * @param {NodeList} preferences
 */
function submitProfileForm(form, hiddenInputsContainer) {
    const allergiesInput = hiddenInputsContainer.querySelector('input[name="allergies"');
    const preferencesInput = hiddenInputsContainer.querySelector('input[name="preferences"');

    let allergiesContainer = document.getElementById('allergies-list');
    let preferencesContainer = document.getElementById('preferences-list');

    allergiesInput.value = JSON.stringify(getListStrContent(allergiesContainer));
    preferencesInput.value = JSON.stringify(getListStrContent(preferencesContainer));

    console.log(`Allergies to save: ${allergiesInput.value}`);
    console.log(`Preferences to save: ${preferencesInput.value}`);

    form.requestSubmit();
}