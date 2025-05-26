/**
 * Plant Identification App - Questionnaire JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    // Get form elements
    const questionnaireForm = document.getElementById('questionnaire-form');
    const hasFlowersSelect = document.getElementById('has_flowers');
    const flowerColorField = document.getElementById('flower_color_field');
    const hasDeciduous = document.getElementById('deciduous');
    const fallColorField = document.getElementById('fall_color_field');
    const hasFruitSelect = document.getElementById('has_fruit');
    const fruitTypeField = document.getElementById('fruit_type_field');

    // Handle conditional fields visibility
    function updateFieldVisibility() {
        // Flower color visibility based on has_flowers value
        if (hasFlowersSelect) {
            if (hasFlowersSelect.value === 'yes') {
                flowerColorField.classList.remove('d-none');
            } else {
                flowerColorField.classList.add('d-none');
            }
        }

        // Fall color visibility based on deciduous value
        if (hasDeciduous) {
            if (hasDeciduous.value === 'yes') {
                fallColorField.classList.remove('d-none');
            } else {
                fallColorField.classList.add('d-none');
            }
        }

        // Fruit type visibility based on has_fruit value
        if (hasFruitSelect) {
            if (hasFruitSelect.value === 'yes') {
                fruitTypeField.classList.remove('d-none');
            } else {
                fruitTypeField.classList.add('d-none');
            }
        }
    }

    // Set initial visibility
    updateFieldVisibility();

    // Add event listeners for field changes
    if (hasFlowersSelect) {
        hasFlowersSelect.addEventListener('change', updateFieldVisibility);
    }
    
    if (hasDeciduous) {
        hasDeciduous.addEventListener('change', updateFieldVisibility);
    }
    
    if (hasFruitSelect) {
        hasFruitSelect.addEventListener('change', updateFieldVisibility);
    }

    // Validate form before submission
    if (questionnaireForm) {
        questionnaireForm.addEventListener('submit', (e) => {
            // Count how many fields have been filled
            const formElements = questionnaireForm.querySelectorAll('select');
            let filledCount = 0;
            
            formElements.forEach(element => {
                if (element.value && element.value !== '' && element.value !== 'unknown' && !element.closest('.d-none')) {
                    filledCount++;
                }
            });
            
            // If fewer than 2 criteria are provided, show a warning
            if (filledCount < 2) {
                e.preventDefault();
                alert('Please fill out at least 2 identification criteria for better results.');
                return false;
            }
            
            return true;
        });
    }

    // Progress tracking
    const formSelects = document.querySelectorAll('#questionnaire-form select');
    const progressBar = document.querySelector('.progress-bar');
    
    if (formSelects.length && progressBar) {
        function updateProgress() {
            let filledCount = 0;
            let totalFields = 0;
            
            formSelects.forEach(select => {
                if (!select.closest('.d-none')) {
                    totalFields++;
                    if (select.value && select.value !== '') {
                        filledCount++;
                    }
                }
            });
            
            const progressPercent = totalFields > 0 ? (filledCount / totalFields) * 100 : 0;
            progressBar.style.width = `${progressPercent}%`;
            progressBar.setAttribute('aria-valuenow', progressPercent);
            
            // Update progress color based on percentage
            if (progressPercent < 30) {
                progressBar.classList.remove('bg-success', 'bg-warning');
                progressBar.classList.add('bg-danger');
            } else if (progressPercent < 70) {
                progressBar.classList.remove('bg-success', 'bg-danger');
                progressBar.classList.add('bg-warning');
            } else {
                progressBar.classList.remove('bg-warning', 'bg-danger');
                progressBar.classList.add('bg-success');
            }
        }
        
        // Initial progress calculation
        updateProgress();
        
        // Update progress when any select field changes
        formSelects.forEach(select => {
            select.addEventListener('change', updateProgress);
        });
    }
});
