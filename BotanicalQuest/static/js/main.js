/**
 * Plant Identification App - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Flash message auto-close
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        if (!message.classList.contains('alert-danger')) {
            setTimeout(() => {
                // Create fade out effect
                message.style.transition = 'opacity 1s';
                message.style.opacity = '0';
                
                // Remove element after transition
                setTimeout(() => {
                    message.remove();
                }, 1000);
            }, 5000);
        }
    });

    // Confirm delete actions
    const confirmDeletes = document.querySelectorAll('.confirm-delete');
    confirmDeletes.forEach(button => {
        button.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
                return false;
            }
            return true;
        });
    });

    // Image error handling
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            // Replace broken images with a placeholder
            this.src = 'https://via.placeholder.com/400x300?text=No+Image+Available';
            this.alt = 'No image available';
        });
    });

    // Fade in elements with .fade-in class
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100 * index);
    });

    // Mobile menu toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', () => {
            document.querySelector('.navbar-collapse').classList.toggle('show');
        });
    }

    // Smooth scroll to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70, // Account for fixed header
                    behavior: 'smooth'
                });
            }
        });
    });
});
