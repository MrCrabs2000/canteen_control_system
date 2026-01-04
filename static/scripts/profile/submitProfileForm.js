/**
 * @param {HTMLFormElement} form
 * @param {Element} hiddenInputsContainer
 * @param {NodeList} allergies
 * @param {NodeList} preferences
 */
function submitProfileForm(form, hiddenInputsContainer, allergiesContainer, preferencesContainer) {
    const allergiesInput = hiddenInputsContainer.querySelector('input[name="allergies"');
    const preferencesInput = hiddenInputsContainer.querySelector('input[name="preferences"');

    allergiesInput.value = JSON.stringify(getAllergies(allergiesContainer));
    preferencesInput.value = JSON.stringify(getPreferences(preferencesContainer));

    console.log(`Allergies to save: ${allergiesInput.value}`);
    console.log(`Preferences to save: ${preferencesInput.value}`);

    form.submit();
}