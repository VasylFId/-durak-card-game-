// app/static/js/animations.js
document.addEventListener('DOMContentLoaded', function() {
    // Animate elements as they scroll into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        elements.forEach(element => {
            const position = element.getBoundingClientRect();
            
            // Check if element is in viewport
            if(position.top < window.innerHeight && position.bottom >= 0) {
                element.classList.add('animated');
            }
        });
    };
    
    // Add animation classes to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.classList.add('animate-on-scroll');
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add animation classes to steps
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        step.classList.add('animate-on-scroll');
        step.style.animationDelay = `${index * 0.2}s`;
    });
    
    // Run on load
    animateOnScroll();
    
    // Run on scroll
    window.addEventListener('scroll', animateOnScroll);
    
    // Hero section parallax effect
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.scrollY;
            heroSection.style.backgroundPositionY = `${scrollPosition * 0.5}px`;
        });
    }
});