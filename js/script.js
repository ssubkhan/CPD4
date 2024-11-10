
console.log('Script loaded');

// Select buttons or switches for each mode toggle
const darkModeButton = document.getElementById('dark-mode');
const highContrastButton = document.getElementById('high-contrast-mode');
const normalModeButton = document.getElementById('normal-mode');

// Function to activate dark mode
function activateDarkMode() {
    document.body.classList.add('dark-mode');
    document.body.classList.remove('high-contrast'); // Remove high-contrast if active
    localStorage.setItem('theme', 'dark'); // Save theme to localStorage
}

// Function to activate high-contrast mode
function activateHighContrastMode() {
    document.body.classList.add('high-contrast');
    document.body.classList.remove('dark-mode'); // Remove dark mode if active
    localStorage.setItem('theme', 'high-contrast'); // Save theme to localStorage
}

// Function to revert to normal mode
function activateNormalMode() {
    document.body.classList.remove('dark-mode', 'high-contrast'); // Remove both modes
    localStorage.setItem('theme', 'normal'); // Save theme to localStorage
}

// Event listeners to toggle the modes when buttons are clicked
darkModeButton.addEventListener('click', activateDarkMode);
highContrastButton.addEventListener('click', activateHighContrastMode);
normalModeButton.addEventListener('click', activateNormalMode);

// Check localStorage for saved theme preference and apply it
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        activateDarkMode();
    } else if (savedTheme === 'high-contrast') {
        activateHighContrastMode();
    } else {
        activateNormalMode(); // Default to normal mode if no theme is saved
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
