mermaid.initialize({ 
    startOnLoad: true,
    theme: document.body.classList.contains('dark-mode') ? 'dark' : 'default'
});

const sections = document.querySelectorAll('main section');
const navLinks = document.querySelectorAll('nav ul li a');

function setActiveLink() {
    let current = 'overview';
    const offset = 150;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        if (window.scrollY >= sectionTop - offset && window.scrollY < sectionTop + sectionHeight - offset) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

function updateMermaidTheme() {
    const isDarkMode = document.body.classList.contains('dark-mode');
    mermaid.initialize({ 
        startOnLoad: true,
        theme: isDarkMode ? 'dark' : 'default',
        themeVariables: {
            primaryColor: isDarkMode ? '#d35400' : '#e67e22',
            primaryTextColor: isDarkMode ? '#e4e4e7' : '#2c3e50',
            primaryBorderColor: isDarkMode ? '#f39c12' : '#e67e22',
            lineColor: isDarkMode ? '#f39c12' : '#e67e22',
            secondaryColor: isDarkMode ? '#2a2a2a' : '#fef5e7',
            tertiaryColor: isDarkMode ? '#1a1a1a' : '#ffffff'
        }
    });
    
    // Rerender mermaid diagrams
    const mermaidElements = document.querySelectorAll('.mermaid');
    mermaidElements.forEach((element, index) => {
        const graphDefinition = element.textContent;
        element.innerHTML = '';
        element.setAttribute('data-processed', 'false');
        mermaid.render(`mermaid-${index}`, graphDefinition, (svgCode) => {
            element.innerHTML = svgCode;
        });
    });
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    
    // Update button text and icon
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');
    
    if (isDarkMode) {
        themeIcon.textContent = '☀️';
        themeText.textContent = 'Light';
    } else {
        themeIcon.textContent = '🌙';
        themeText.textContent = 'Dark';
    }
    
    // Save preference (using in-memory storage as requested)
    window.darkModePreference = isDarkMode;
    
    // Update mermaid theme
    setTimeout(updateMermaidTheme, 100);
}

// Add smooth reveal animation on scroll
function revealOnScroll() {
    const reveals = document.querySelectorAll('section, table, pre, blockquote');
    
    reveals.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
}

// Add typing effect for code blocks
function addTypingEffect() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        block.addEventListener('mouseenter', () => {
            block.style.transform = 'scale(1.02)';
            block.style.transition = 'transform 0.2s ease';
        });
        
        block.addEventListener('mouseleave', () => {
            block.style.transform = 'scale(1)';
        });
    });
}

// Smooth scrolling for navigation links
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);
        if (targetSection) {
            const offsetTop = targetSection.offsetTop - 100;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Add progress indicator
function createProgressIndicator() {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, #e67e22, #f39c12);
        z-index: 9999;
        transition: width 0.3s ease;
    `;
    document.body.appendChild(progressBar);
    
    function updateProgress() {
        const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        progressBar.style.width = scrolled + '%';
    }
    
    window.addEventListener('scroll', updateProgress);
}

// Initialize everything
window.addEventListener('load', () => {
    setActiveLink();
    
    // Load saved theme preference from memory
    if (window.darkModePreference) {
        document.body.classList.add('dark-mode');
        document.getElementById('theme-icon').textContent = '☀️';
        document.getElementById('theme-text').textContent = 'Light';
    }
    
    updateMermaidTheme();
    revealOnScroll();
    addTypingEffect();
    createProgressIndicator();
    
    // Add welcome animation
    const logo = document.querySelector('.logo-icon svg');
    if (logo) {
        logo.style.animation = 'pulse 2s ease-in-out infinite';
    }
});

// Update active link on scroll with performance optimization
let ticking = false;
window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(() => {
            setActiveLink();
            revealOnScroll();
            ticking = false;
        });
        ticking = true;
    }
});

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.altKey) {
        switch(e.key) {
            case '1':
                document.getElementById('overview').scrollIntoView({ behavior: 'smooth' });
                break;
            case '2':
                document.getElementById('chapter1').scrollIntoView({ behavior: 'smooth' });
                break;
            case '3':
                document.getElementById('chapter2').scrollIntoView({ behavior: 'smooth' });
                break;
            case '4':
                document.getElementById('chapter3').scrollIntoView({ behavior: 'smooth' });
                break;
            case '5':
                document.getElementById('chapter4').scrollIntoView({ behavior: 'smooth' });
                break;
            case '6':
                document.getElementById('chapter5').scrollIntoView({ behavior: 'smooth' });
                break;
            case '7':
                document.getElementById('chapter6').scrollIntoView({ behavior: 'smooth' });
                break;
        }
    }
});

// Add floating action button for quick navigation
function createFloatingNav() {
    const fab = document.createElement('div');
    fab.innerHTML = '📋';
    fab.style.cssText = `
        position: fixed;
        bottom: 80px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #e67e22, #f39c12);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(230, 126, 34, 0.3);
        z-index: 1003;
        transition: all 0.3s ease;
    `;
    
    fab.addEventListener('click', () => {
        document.getElementById('overview').scrollIntoView({ behavior: 'smooth' });
    });
    
    fab.addEventListener('mouseenter', () => {
        fab.style.transform = 'scale(1.1) rotate(10deg)';
        fab.style.boxShadow = '0 6px 25px rgba(230, 126, 34, 0.4)';
    });
    
    fab.addEventListener('mouseleave', () => {
        fab.style.transform = 'scale(1) rotate(0deg)';
        fab.style.boxShadow = '0 4px 20px rgba(230, 126, 34, 0.3)';
    });
    
    document.body.appendChild(fab);
}

// Initialize floating navigation
window.addEventListener('load', createFloatingNav);