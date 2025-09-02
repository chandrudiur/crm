// ===== GLOBAL VARIABLES =====
let sidebarPinned = localStorage.getItem('sidebarPinned') === 'true';
let sidebarHoverTimeout;
let chartInstances = {};

// ===== DOCUMENT READY =====
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeTooltips();
    initializePopovers();
    initializeCharts();
    initializeFormValidation();
    initializeTableSorting();
    initializeSearchFilters();
    
    // Initialize any other components
    console.log('Myndwell Admin Application initialized');
});

// ===== SIDEBAR FUNCTIONALITY =====
function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const mainContent = document.getElementById('main-content');
    
    if (!sidebar || !sidebarToggle) return;
    
    // Set initial state
    if (sidebarPinned) {
        sidebar.classList.add('pinned', 'expanded');
        updateToggleIcon(true);
    }
    
    // Toggle button click handler
    sidebarToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleSidebarPin();
    });
    
    // Hover handlers
    sidebar.addEventListener('mouseenter', function() {
        if (!sidebarPinned) {
            clearTimeout(sidebarHoverTimeout);
            sidebarHoverTimeout = setTimeout(() => {
                sidebar.classList.add('expanded');
            }, 300);
        }
    });
    
    sidebar.addEventListener('mouseleave', function() {
        if (!sidebarPinned) {
            clearTimeout(sidebarHoverTimeout);
            sidebar.classList.remove('expanded');
        }
    });
    
    // Click outside to collapse (if not pinned)
    document.addEventListener('click', function(e) {
        if (!sidebarPinned && !sidebar.contains(e.target)) {
            sidebar.classList.remove('expanded');
        }
    });
    
    // Update active nav link
    updateActiveNavLink();
}

function toggleSidebarPin() {
    const sidebar = document.getElementById('sidebar');
    sidebarPinned = !sidebarPinned;
    
    localStorage.setItem('sidebarPinned', sidebarPinned.toString());
    
    if (sidebarPinned) {
        sidebar.classList.add('pinned', 'expanded');
    } else {
        sidebar.classList.remove('pinned', 'expanded');
    }
    
    updateToggleIcon(sidebarPinned);
}

function updateToggleIcon(pinned) {
    const toggleIcon = document.querySelector('#sidebar-toggle i');
    if (toggleIcon) {
        toggleIcon.className = pinned ? 'bi bi-pin-angle-fill' : 'bi bi-pin-angle';
    }
}

function updateActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// ===== BOOTSTRAP COMPONENTS =====
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            delay: { show: 500, hide: 100 }
        });
    });
}

function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// ===== CHART INITIALIZATION =====
function initializeCharts() {
    // Initialize any charts that exist on the page
    const chartElements = document.querySelectorAll('canvas[id$="Chart"]');
    
    chartElements.forEach(canvas => {
        if (canvas.id && !chartInstances[canvas.id]) {
            // Chart will be initialized by specific page scripts
            console.log(`Chart element found: ${canvas.id}`);
        }
    });
}

// ===== FORM VALIDATION =====
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Real-time validation for specific fields
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', validateEmail);
    });
    
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', validatePassword);
    });
}

function validateEmail(event) {
    const input = event.target;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (input.value && !emailRegex.test(input.value)) {
        input.setCustomValidity('Please enter a valid email address');
        input.classList.add('is-invalid');
    } else {
        input.setCustomValidity('');
        input.classList.remove('is-invalid');
        if (input.value) input.classList.add('is-valid');
    }
}

function validatePassword(event) {
    const input = event.target;
    const minLength = 8;
    const hasUpper = /[A-Z]/.test(input.value);
    const hasLower = /[a-z]/.test(input.value);
    const hasNumber = /\d/.test(input.value);
    
    let isValid = input.value.length >= minLength && hasUpper && hasLower && hasNumber;
    
    if (input.value && !isValid) {
        input.setCustomValidity('Password must be at least 8 characters with uppercase, lowercase, and number');
        input.classList.add('is-invalid');
    } else {
        input.setCustomValidity('');
        input.classList.remove('is-invalid');
        if (input.value) input.classList.add('is-valid');
    }
}

// ===== TABLE FUNCTIONALITY =====
function initializeTableSorting() {
    const sortableHeaders = document.querySelectorAll('th[data-sortable]');
    
    sortableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            sortTable(header);
        });
    });
}

function sortTable(header) {
    const table = header.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    const currentOrder = header.getAttribute('data-order') || 'asc';
    const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
    
    // Clear all sort indicators
    table.querySelectorAll('th').forEach(th => {
        th.removeAttribute('data-order');
        const icon = th.querySelector('.sort-icon');
        if (icon) icon.remove();
    });
    
    // Set new sort order
    header.setAttribute('data-order', newOrder);
    const sortIcon = document.createElement('i');
    sortIcon.className = `bi bi-arrow-${newOrder === 'asc' ? 'up' : 'down'} ms-2 sort-icon`;
    header.appendChild(sortIcon);
    
    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Try to parse as numbers
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return newOrder === 'asc' ? aNum - bNum : bNum - aNum;
        } else {
            return newOrder === 'asc' 
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        }
    });
    
    // Reorder DOM
    rows.forEach(row => tbody.appendChild(row));
    
    // Add animation
    tbody.style.opacity = '0.7';
    setTimeout(() => {
        tbody.style.opacity = '1';
    }, 150);
}

// ===== SEARCH AND FILTER =====
function initializeSearchFilters() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[placeholder*="Search"], input[placeholder*="search"]');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(function() {
            performSearch(input);
        }, 300));
    });
}

function performSearch(input) {
    const searchTerm = input.value.toLowerCase();
    const targetSelector = input.getAttribute('data-search-target') || '.searchable-item';
    const container = input.closest('.card') || document;
    const items = container.querySelectorAll(targetSelector);
    
    let visibleCount = 0;
    
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        const isVisible = text.includes(searchTerm);
        
        item.style.display = isVisible ? '' : 'none';
        if (isVisible) visibleCount++;
    });
    
    // Show/hide empty state
    const emptyState = container.querySelector('.empty-search-state');
    if (emptyState) {
        emptyState.style.display = visibleCount === 0 && searchTerm ? 'block' : 'none';
    }
    
    // Update results count
    const resultsCount = container.querySelector('.search-results-count');
    if (resultsCount) {
        resultsCount.textContent = `${visibleCount} result${visibleCount !== 1 ? 's' : ''}`;
    }
}

// ===== UTILITY FUNCTIONS =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    } else {
        return num.toString();
    }
}

function formatDate(date, format = 'short') {
    const options = {
        short: { month: 'short', day: 'numeric', year: 'numeric' },
        long: { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
        time: { hour: '2-digit', minute: '2-digit' }
    };
    
    return new Intl.DateTimeFormat('en-US', options[format]).format(new Date(date));
}

function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        return new Promise((resolve, reject) => {
            document.execCommand('copy') ? resolve() : reject();
            textArea.remove();
        });
    }
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 500px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-dismiss
    if (duration > 0) {
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    }
    
    return notification;
}

function showConfirmModal(title, message, onConfirm, onCancel = null) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>${message}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger confirm-btn">Confirm</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    const modalInstance = new bootstrap.Modal(modal);
    
    modal.querySelector('.confirm-btn').addEventListener('click', () => {
        modalInstance.hide();
        if (onConfirm) onConfirm();
    });
    
    modal.addEventListener('hidden.bs.modal', () => {
        modal.remove();
        if (onCancel) onCancel();
    });
    
    modalInstance.show();
    
    return modalInstance;
}

// ===== LOADING STATES =====
function showLoading(element, text = 'Loading...') {
    element.classList.add('loading');
    element.setAttribute('data-original-content', element.innerHTML);
    element.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>${text}`;
    element.disabled = true;
}

function hideLoading(element) {
    element.classList.remove('loading');
    const originalContent = element.getAttribute('data-original-content');
    if (originalContent) {
        element.innerHTML = originalContent;
        element.removeAttribute('data-original-content');
    }
    element.disabled = false;
}

// ===== API HELPERS =====
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, mergedOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API request failed:', error);
        showNotification('An error occurred. Please try again.', 'danger');
        throw error;
    }
}

// ===== CHART HELPERS =====
function createChart(canvasId, config) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    
    // Destroy existing chart if it exists
    if (chartInstances[canvasId]) {
        chartInstances[canvasId].destroy();
    }
    
    // Apply default styling
    const defaultConfig = {
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    };
    
    const mergedConfig = mergeDeep(defaultConfig, config);
    
    chartInstances[canvasId] = new Chart(canvas, mergedConfig);
    return chartInstances[canvasId];
}

function updateChart(canvasId, newData) {
    const chart = chartInstances[canvasId];
    if (chart) {
        chart.data = newData;
        chart.update();
    }
}

function mergeDeep(target, source) {
    const output = Object.assign({}, target);
    if (isObject(target) && isObject(source)) {
        Object.keys(source).forEach(key => {
            if (isObject(source[key])) {
                if (!(key in target))
                    Object.assign(output, { [key]: source[key] });
                else
                    output[key] = mergeDeep(target[key], source[key]);
            } else {
                Object.assign(output, { [key]: source[key] });
            }
        });
    }
    return output;
}

function isObject(item) {
    return item && typeof item === 'object' && !Array.isArray(item);
}

// ===== FORM HELPERS =====
function serializeForm(form) {
    const formData = new FormData(form);
    const object = {};
    
    formData.forEach((value, key) => {
        if (object[key]) {
            if (Array.isArray(object[key])) {
                object[key].push(value);
            } else {
                object[key] = [object[key], value];
            }
        } else {
            object[key] = value;
        }
    });
    
    return object;
}

function resetForm(form) {
    form.reset();
    form.classList.remove('was-validated');
    
    // Remove validation classes
    form.querySelectorAll('.is-valid, .is-invalid').forEach(input => {
        input.classList.remove('is-valid', 'is-invalid');
    });
}

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"], input[placeholder*="Search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) modalInstance.hide();
        });
    }
    
    // Ctrl/Cmd + S to save forms
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const activeForm = document.querySelector('form:focus-within');
        if (activeForm) {
            const submitButton = activeForm.querySelector('button[type="submit"], input[type="submit"]');
            if (submitButton) submitButton.click();
        }
    }
});

// ===== EXPORT FUNCTIONS =====
window.MyndwellAdmin = {
    sidebar: {
        toggle: toggleSidebarPin,
        pin: () => toggleSidebarPin(true),
        unpin: () => toggleSidebarPin(false)
    },
    notifications: {
        show: showNotification,
        confirm: showConfirmModal
    },
    loading: {
        show: showLoading,
        hide: hideLoading
    },
    api: {
        request: apiRequest
    },
    charts: {
        create: createChart,
        update: updateChart,
        instances: chartInstances
    },
    utils: {
        debounce,
        throttle,
        formatNumber,
        formatDate,
        copyToClipboard,
        serializeForm,
        resetForm
    }
};

// Log initialization
console.log('Myndwell Admin JavaScript initialized');
console.log('Available methods:', Object.keys(window.MyndwellAdmin));
