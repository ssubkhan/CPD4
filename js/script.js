console.log('Script loaded');

// Select buttons or switches for each mode toggle
const darkModeButton = document.getElementById('dark-mode');
const highContrastButton = document.getElementById('high-contrast-mode');
const normalModeButton = document.getElementById('normal-mode');

// Function to set the mode based on a passed value ('dark', 'high-contrast', or 'normal')
function setMode(mode) {
    // Remove any active modes
    document.body.classList.remove('dark-mode', 'high-contrast');

    // Add the selected mode class
    if (mode === 'dark') {
        document.body.classList.add('dark-mode');
    } else if (mode === 'high-contrast') {
        document.body.classList.add('high-contrast');
    }

    // Save the selected mode to localStorage
    localStorage.setItem('theme', mode);
}

// Event listeners to toggle the modes when buttons are clicked
darkModeButton.addEventListener('click', function() {
    setMode('dark');
});
highContrastButton.addEventListener('click', function() {
    setMode('high-contrast');
});
normalModeButton.addEventListener('click', function() {
    setMode('normal');
});

// Check localStorage for saved theme preference and apply it
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setMode(savedTheme); // Apply saved theme
    } else {
        setMode('normal'); // Default to normal mode if no theme is saved
    }
}

// Load the saved theme on page load
window.addEventListener('load', loadTheme);


// Check for reduced motion preference
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (prefersReducedMotion) {
  // Add click event to toggle card flip in reduced motion mode
  document.querySelectorAll('.athlete-card').forEach(card => {
    card.addEventListener('click', () => {
      card.classList.toggle('clicked'); // Toggle flip when clicked
    });
  });
} else {
  // Default hover flip behavior for users without reduced motion preference
  document.querySelectorAll('.athlete-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.querySelector('.card-inner').style.transform = 'rotateY(180deg)';
    });
    card.addEventListener('mouseleave', () => {
      card.querySelector('.card-inner').style.transform = 'none';
    });
  });
}
