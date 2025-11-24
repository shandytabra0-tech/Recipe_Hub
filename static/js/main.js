// Enhanced Recipe Hub Interactions
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Recipe card hover effects with sound simulation
    const recipeCards = document.querySelectorAll('.recipe-card');
    recipeCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.02)';
            
            // Add sparkle effect
            const sparkle = document.createElement('div');
            sparkle.innerHTML = '✨';
            sparkle.style.position = 'absolute';
            sparkle.style.top = '10px';
            sparkle.style.right = '10px';
            sparkle.style.fontSize = '1.5rem';
            sparkle.style.animation = 'sparkle 1s ease-out';
            sparkle.style.pointerEvents = 'none';
            this.style.position = 'relative';
            this.appendChild(sparkle);
            
            setTimeout(() => sparkle.remove(), 1000);
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });

    // Search input enhancement
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.boxShadow = '0 0 30px rgba(102, 126, 234, 0.3)';
        });
        
        searchInput.addEventListener('blur', function() {
            this.parentElement.style.transform = '';
            this.parentElement.style.boxShadow = '';
        });
    }

    // Animated counter for recipe stats (if any numbers are present)
    function animateNumbers() {
        const numbers = document.querySelectorAll('.animate-number');
        numbers.forEach(num => {
            const target = parseInt(num.textContent);
            let current = 0;
            const increment = target / 50;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                num.textContent = Math.floor(current);
            }, 20);
        });
    }

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe recipe cards for scroll animations
    recipeCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });

    // Add floating particles effect
    function createFloatingParticle() {
        const particle = document.createElement('div');
        particle.innerHTML = ['🍳', '🥘', '🍰', '🥗', '🍕'][Math.floor(Math.random() * 5)];
        particle.style.position = 'fixed';
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.top = '100vh';
        particle.style.fontSize = '2rem';
        particle.style.opacity = '0.3';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '-1';
        particle.style.animation = 'floatUp 8s linear forwards';
        document.body.appendChild(particle);
        
        setTimeout(() => particle.remove(), 8000);
    }

    // Create particles periodically
    setInterval(createFloatingParticle, 3000);

    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes sparkle {
            0% { transform: scale(0) rotate(0deg); opacity: 1; }
            50% { transform: scale(1) rotate(180deg); opacity: 0.8; }
            100% { transform: scale(0) rotate(360deg); opacity: 0; }
        }
        
        @keyframes floatUp {
            0% { transform: translateY(0) rotate(0deg); opacity: 0.3; }
            50% { opacity: 0.6; }
            100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
        }
        
        .recipe-card {
            will-change: transform;
        }
    `;
    document.head.appendChild(style);

    // Enhanced button interactions
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.05)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
        
        btn.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(0) scale(0.98)';
        });
        
        btn.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-2px) scale(1.05)';
        });
    });
});