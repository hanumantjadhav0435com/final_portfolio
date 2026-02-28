// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function () {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 70;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(33, 37, 41, 0.98)';
        } else {
            navbar.style.background = 'rgba(33, 37, 41, 0.95)';
        }
    });

    // Active navigation link highlighting
    const sections = document.querySelectorAll('section[id]');
    const navLinksArray = Array.from(document.querySelectorAll('.navbar-nav .nav-link'));

    window.addEventListener('scroll', function () {
        const scrollPos = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                navLinksArray.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });

    // Form validation and enhancement
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            const formData = new FormData(this);
            const name = formData.get('name');
            const email = formData.get('email');
            const subject = formData.get('subject');
            const message = formData.get('message');

            // Basic validation
            if (!name || !email || !subject || !message) {
                e.preventDefault();
                alert('Please fill in all fields.');
                return;
            }

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                alert('Please enter a valid email address.');
                return;
            }

            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
            submitBtn.disabled = true;

            // Note: The form will be submitted normally to Flask backend
            // This is just for UX enhancement
        });
    }

    // Hero section is now handled with CSS animations for the profile image

    // 3D tilt hover effects for cards and sections
    const tiltCards = document.querySelectorAll('.tilt-card');

    const maxTilt = 12; // degrees

    function handleTiltMove(e) {
        const card = e.currentTarget;
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const midX = rect.width / 2;
        const midY = rect.height / 2;

        const rotateY = ((x - midX) / midX) * maxTilt;
        const rotateX = ((midY - y) / midY) * maxTilt;

        const mx = (x / rect.width) * 100;
        const my = (y / rect.height) * 100;

        card.style.setProperty('--mx', `${mx}%`);
        card.style.setProperty('--my', `${my}%`);
        card.style.transform = `rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateZ(8px)`;
        card.classList.add('is-tilting');
    }

    function handleTiltLeave(e) {
        const card = e.currentTarget;
        card.style.transform = 'rotateX(0deg) rotateY(0deg) translateZ(0)';
        card.classList.remove('is-tilting');
    }

    tiltCards.forEach(card => {
        card.addEventListener('mousemove', handleTiltMove);
        card.addEventListener('mouseleave', handleTiltLeave);
    });
});

// Utility functions
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

// Add resize event listener with debouncing
window.addEventListener('resize', debounce(() => {
    // Recalculate positions on resize
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        navbar.style.background = window.scrollY > 50 ?
            'rgba(33, 37, 41, 0.98)' : 'rgba(33, 37, 41, 0.95)';
    }
}, 250));
