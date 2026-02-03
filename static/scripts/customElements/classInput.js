class ClassInput extends HTMLElement {
    static formAssociated = true;
    static observedAttributes = ['readonly', 'required', 'value'];
    
    constructor() {
        super();
        this.internals = this.attachInternals();
        
        this.numberInput = document.createElement('input');
        this.letterInput = document.createElement('input');
        this.readonlyInput = document.createElement('input');

        this.appendChild(this.numberInput);
        this.appendChild(this.letterInput);
        
        this.inputs = this.querySelectorAll('input');
    }
    
    
    get readOnly() {
        return this.hasAttribute('readonly');
    }
    
    set readOnly(value) {
        if (value) {
            this.setAttribute('readonly', '');
        } else {
            this.removeAttribute('readonly');
        }
    }
    
    
    get value() {
        return this.getAttribute('value');
    }
    
    set value(val) {
        this.setAttribute('value', val);
    }
    
    
    connectedCallback() {
        this.form = this.internals.form;
        
        this.numberInput.setAttribute('class', 'class-number');
        this.numberInput.setAttribute('type', 'number');
        this.numberInput.setAttribute('max', '11');
        this.numberInput.setAttribute('min', '1');
        this.numberInput.setAttribute('placeholder', '1');
        this.numberInput.addEventListener('input', this.updateValueOnInput.bind(this));
        this.numberInput.addEventListener('change', this.updateValueOnInput.bind(this));
        this.numberInput.addEventListener('blur', this.updateValueOnInput.bind(this));
        
        this.letterInput.setAttribute('class', 'class-letter');
        this.letterInput.setAttribute('maxlength', '1');
        this.letterInput.setAttribute('pattern', '[А-ЯЁ]*');
        this.letterInput.setAttribute('placeholder', 'А');
        this.letterInput.addEventListener('input', this.updateValueOnInput.bind(this));
        this.letterInput.addEventListener('change', this.updateValueOnInput.bind(this));
        this.letterInput.addEventListener('blur', this.updateValueOnInput.bind(this));
        
        const style = document.createElement('style');
        style.textContent = `
        class-input {
            display: flex;
            gap: 8px;
            min-width: fit-content;
            font-size: inherit;
        }

        .class-number {
            width: 2.4em;
            font-size: inherit;
        }

        .class-letter {
            width: 1em;
            font-size: inherit;
        }

        .readonly-class-input {
            font-size: inherit;
        }
        `

        this.appendChild(style);

        this.form.addEventListener('submit', this.handleFormSubmit.bind(this));

        this.inputs.forEach(input => {
            input.addEventListener('input', this.updateValidity.bind(this));
            input.addEventListener('change', this.updateValidity.bind(this));
            input.addEventListener('blur', this.updateValidity.bind(this));
        });

        this.updateValidity();

        if (this.hasAttribute('readonly')) {
            this.renderReadonlyChange();
        }
        if (this.hasAttribute('required')) {
            this.renderRequiredChange();
        }
    }


    attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'readonly') {
            this.renderReadonlyChange();
        }
        if (name === 'required') {
            this.renderRequiredChange();
        }
        if (name === 'value') {
            this.updateValue(newValue);
        }
    }   


    renderReadonlyChange() {
        if (this.children.length == 0) { 
            return;
        }

        if (this.readOnly === true) {
            this.numberInput.style.display = 'none';
            this.letterInput.style.display = 'none';

            this.readonlyInput.setAttribute('readonly', '');
            this.readonlyInput.setAttribute('class', 'readonly-class-input');
            this.readonlyInput.value = this.value;
            this.appendChild(this.readonlyInput);

        } else {
            this.readonlyInput.remove();

            this.numberInput.style.display = 'inline-block';
            this.letterInput.style.display = 'inline-block';

        }
    }


    renderRequiredChange() {
        if (this.children.length == 0) {
            return;
        }

        if (this.hasAttribute('required')) {
            this.inputs.forEach(input => {
                input.required = true;
            });
        } else {
            this.inputs.forEach(input => {
                input.required = false;
            });
        }
    }

    
    updateValue(val) {
        const splited = val.split(/(\d+)/);
        const cleanedResult = splited.filter(item => item.length > 0);

        this.numberInput.value = cleanedResult[0] ? cleanedResult[0] : 's';

        this.letterInput.value =  cleanedResult[1] ? cleanedResult[1] : '';
        this.internals.setFormValue(val);
    }


    updateValueOnInput() {
        const newValue = this.numberInput.value + this.letterInput.value;
        this.setAttribute('value', newValue);
    }
    

    updateValidity() {
        let anyChildInvalid = false;
        let validationMessage = '';

        for (const input of this.inputs) {
            if (!input.checkValidity()) {
                anyChildInvalid = true;
                validationMessage = input.validationMessage;
                break;
            }
        }

        this.internals.setValidity(
            anyChildInvalid ? { customError: true } : {},
            validationMessage
        );
    }


    handleFormSubmit(event) {
        if (!this.checkValidity()) {
            console.log('Form is invalid, preventing submission via JS handler');
            event.preventDefault();
            this.reportValidity();
        } else {
            console.log('Form is valid, submitting...');
        }
    }


    checkValidity() {
        return this.internals.checkValidity();
    }


    reportValidity() {
        return this.internals.reportValidity();
    }


}

customElements.define('class-input', ClassInput);