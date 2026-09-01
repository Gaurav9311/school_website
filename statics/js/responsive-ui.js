/**
 * Responsive UI Components
 * Handles accordion toggle, collapse/expand animations, and mobile-friendly UI
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeAccordions();
});

/**
 * Initialize accordion functionality
 */
function initializeAccordions() {
    const accordionHeaders = document.querySelectorAll(
        '.accordion-header-custom, .calendar-accordion-header'
    );

    accordionHeaders.forEach(header => {
        header.addEventListener('click', function(e) {
            e.preventDefault();
            toggleAccordion(this);
        });

        // Allow keyboard navigation (Enter/Space)
        header.setAttribute('role', 'button');
        header.setAttribute('tabindex', '0');
        
        header.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleAccordion(this);
            }
        });
    });
}

/**
 * Toggle accordion open/closed state
 */
function toggleAccordion(headerElement) {
    const isActive = headerElement.classList.contains('active');
    
    // Close all accordions in the same group
    const allHeaders = headerElement.parentElement.parentElement.querySelectorAll(
        '.accordion-header-custom, .calendar-accordion-header'
    );
    
    allHeaders.forEach(h => {
        if (h !== headerElement) {
            h.classList.remove('active');
            const content = h.nextElementSibling;
            if (content) {
                content.classList.remove('show');
            }
        }
    });

    // Toggle current accordion
    headerElement.classList.toggle('active');
    const contentElement = headerElement.nextElementSibling;
    
    if (contentElement) {
        contentElement.classList.toggle('show');
    }
}

/**
 * Open specific accordion by index
 */
function openAccordionByIndex(containerSelector, index) {
    const headers = document.querySelectorAll(
        `${containerSelector} .accordion-header-custom, ${containerSelector} .calendar-accordion-header`
    );
    
    if (headers[index]) {
        headers[index].click();
    }
}

/**
 * Close all accordions in a container
 */
function closeAllAccordions(containerSelector) {
    const headers = document.querySelectorAll(
        `${containerSelector} .accordion-header-custom, ${containerSelector} .calendar-accordion-header`
    );
    
    headers.forEach(header => {
        if (header.classList.contains('active')) {
            header.click();
        }
    });
}

/**
 * Make table responsive by converting to card layout on mobile
 * Call this for any table that needs mobile responsiveness
 */
function makeTableResponsive(tableSelector) {
    const table = document.querySelector(tableSelector);
    if (!table) return;

    // Get table headers
    const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());

    // Convert each row to a card-like structure (handled by CSS in responsive breakpoints)
    // This function ensures data attributes are set for CSS ::before pseudo-elements
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach((row, rowIndex) => {
        const cells = row.querySelectorAll('td');
        cells.forEach((cell, cellIndex) => {
            cell.setAttribute('data-label', headers[cellIndex] || '');
        });
    });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize smooth scroll on page load
initSmoothScroll();

// Export functions for external use
window.ResponsiveUI = {
    toggleAccordion,
    openAccordionByIndex,
    closeAllAccordions,
    makeTableResponsive,
    initializeAccordions
};
