// Theme Switcher JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get the theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    
    // Check for saved theme preference or use the default theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    updateToggleIcon(savedTheme);
    
    // Add event listener to the toggle button
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Update the theme
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        
        // Save the preference
        localStorage.setItem('theme', newTheme);
        
        // Update the toggle icon
        updateToggleIcon(newTheme);
        
        // Add a transition effect
        document.body.classList.add('theme-transition');
        setTimeout(() => {
            document.body.classList.remove('theme-transition');
        }, 300);
    });
    
    // Function to update the toggle icon based on the current theme
    function updateToggleIcon(theme) {
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        } else {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }
}); 