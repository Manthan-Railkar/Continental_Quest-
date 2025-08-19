// Continental Quest - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initNavigation();
    initEarthInteractions();
    initContinentCards();
    initModal();
    initScrollEffects();
    initProgressAnimations();
});

// Navigation functionality
function initNavigation() {
    const mobileMenu = document.getElementById('mobile-menu');
    const navMenu = document.querySelector('.nav-menu');

    mobileMenu.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        
        // Animate hamburger menu
        const bars = mobileMenu.querySelectorAll('.bar');
        bars.forEach((bar, index) => {
            bar.style.transform = navMenu.classList.contains('active') 
                ? `rotate(${index === 0 ? '45' : index === 1 ? '0' : '-45'}deg) translate(${index === 1 ? '0' : '6px'}, ${index === 0 ? '6px' : index === 1 ? '0' : '-6px'})`
                : 'none';
            bar.style.opacity = navMenu.classList.contains('active') && index === 1 ? '0' : '1';
        });
    });

    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close mobile menu if open
                navMenu.classList.remove('active');
                const bars = mobileMenu.querySelectorAll('.bar');
                bars.forEach(bar => {
                    bar.style.transform = 'none';
                    bar.style.opacity = '1';
                });
            }
        });
    });

    // Active navigation highlighting
    window.addEventListener('scroll', () => {
        const sections = document.querySelectorAll('section');
        const scrollPos = window.scrollY + 200;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });
}

// Earth globe interactions
function initEarthInteractions() {
    const earthGlobe = document.getElementById('earthGlobe');
    const continentHotspots = document.querySelectorAll('.continent-hotspot');

    // Earth rotation control
    let isHovering = false;
    
    earthGlobe.addEventListener('mouseenter', () => {
        isHovering = true;
        earthGlobe.style.animationPlayState = 'paused';
    });
    
    earthGlobe.addEventListener('mouseleave', () => {
        isHovering = false;
        earthGlobe.style.animationPlayState = 'running';
    });

    // Continent hotspot interactions
    continentHotspots.forEach(hotspot => {
        const continentName = hotspot.dataset.continent;
        
        hotspot.addEventListener('click', () => {
            // Create ripple effect
            createRippleEffect(hotspot);
            
            // Highlight corresponding continent card
            highlightContinentCard(continentName);
            
            // Show continent details
            showContinentDetails(continentName);
            
            // Trigger selection animation
            hotspot.classList.add('selected');
            setTimeout(() => hotspot.classList.remove('selected'), 1000);
        });

        hotspot.addEventListener('mouseenter', () => {
            // Scale up pulse effect
            const pulse = hotspot.querySelector('.hotspot-pulse');
            pulse.style.animationDuration = '0.8s';
            pulse.style.transform = 'scale(1.2)';
            
            // Show connecting line to corresponding card (visual enhancement)
            showConnectionLine(hotspot, continentName);
        });

        hotspot.addEventListener('mouseleave', () => {
            const pulse = hotspot.querySelector('.hotspot-pulse');
            pulse.style.animationDuration = '2s';
            pulse.style.transform = 'scale(1)';
            hideConnectionLine();
        });
    });
}

// Continent cards functionality
function initContinentCards() {
    const continentCards = document.querySelectorAll('.continent-card');
    
    continentCards.forEach(card => {
        const continentBtn = card.querySelector('.continent-btn');
        const progressFill = card.querySelector('.progress-fill');
        
        card.addEventListener('mouseenter', () => {
            // Animate progress bar on hover
            const currentWidth = Math.random() * 60 + 20; // Simulate progress
            progressFill.style.width = `${currentWidth}%`;
            
            // Add floating effect
            card.style.transform = 'translateY(-15px) scale(1.02)';
            
            // Particle effect
            createParticleEffect(card);
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
        
        continentBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const continentName = card.querySelector('h3').textContent.toLowerCase().replace(' ', '-');
            
            // Button click animation
            continentBtn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                continentBtn.style.transform = 'scale(1)';
            }, 150);
            
            // Launch continent selection
            launchContinent(continentName, card);
        });
    });
}

// Modal functionality
function initModal() {
    const modal = document.getElementById('gameModal');
    const startGameBtn = document.getElementById('startGameBtn');
    const learnMoreBtn = document.getElementById('learnMoreBtn');
    const closeBtn = modal.querySelector('.close');

    startGameBtn.addEventListener('click', () => {
        showModal();
        addModalEntryAnimation();
    });

    learnMoreBtn.addEventListener('click', () => {
        // Smooth scroll to features section
        document.getElementById('about').scrollIntoView({
            behavior: 'smooth'
        });
    });

    closeBtn.addEventListener('click', () => {
        hideModal();
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            hideModal();
        }
    });

    // Modal buttons functionality
    const modalButtons = modal.querySelectorAll('.btn');
    modalButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            if (btn.textContent.includes('Begin Adventure')) {
                // Start the game
                startGameSequence();
            } else if (btn.textContent.includes('Select Difficulty')) {
                // Show difficulty selection
                showDifficultySelection();
            }
        });
    });
}

// Scroll effects
function initScrollEffects() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Special animations for different sections
                if (entry.target.classList.contains('continent-card')) {
                    animateContinentCard(entry.target);
                } else if (entry.target.classList.contains('feature-card')) {
                    animateFeatureCard(entry.target);
                }
            }
        });
    }, observerOptions);

    // Observe elements for scroll animations
    const animatedElements = document.querySelectorAll('.continent-card, .feature-card, .section-title');
    animatedElements.forEach(el => observer.observe(el));
}

// Progress animations
function initProgressAnimations() {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    // Simulate progress loading based on difficulty
    progressBars.forEach(bar => {
        const card = bar.closest('.continent-card');
        const difficulty = card.dataset.difficulty;
        
        let progressValue = 0;
        switch(difficulty) {
            case 'easy': progressValue = Math.random() * 40 + 50; break;
            case 'medium': progressValue = Math.random() * 30 + 30; break;
            case 'hard': progressValue = Math.random() * 25 + 15; break;
            case 'extreme': progressValue = Math.random() * 15 + 5; break;
            default: progressValue = 25;
        }
        
        // Store the value for later use
        bar.dataset.progress = progressValue;
    });
}

// Helper Functions

function createRippleEffect(element) {
    const ripple = document.createElement('div');
    ripple.className = 'ripple-effect';
    ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        background: rgba(233, 69, 96, 0.6);
        width: 10px;
        height: 10px;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        animation: ripple-expand 1s ease-out forwards;
        pointer-events: none;
        z-index: 1000;
    `;
    
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 1000);
    
    // Add ripple animation keyframes if not exists
    if (!document.querySelector('#ripple-styles')) {
        const style = document.createElement('style');
        style.id = 'ripple-styles';
        style.textContent = `
            @keyframes ripple-expand {
                0% {
                    width: 10px;
                    height: 10px;
                    opacity: 1;
                }
                100% {
                    width: 100px;
                    height: 100px;
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

function highlightContinentCard(continentName) {
    const cards = document.querySelectorAll('.continent-card');
    cards.forEach(card => {
        const cardTitle = card.querySelector('h3').textContent.toLowerCase().replace(' ', '-');
        if (cardTitle === continentName) {
            card.style.border = '2px solid #4dabf7';
            card.style.boxShadow = '0 0 30px rgba(73, 171, 247, 0.5)';
            
            setTimeout(() => {
                card.style.border = '1px solid rgba(255, 255, 255, 0.1)';
                card.style.boxShadow = 'none';
            }, 3000);
        }
    });
}

function showContinentDetails(continentName) {
    const details = {
        'north-america': {
            description: 'Explore vast wilderness and modern cities',
            challenges: ['Mountain Navigation', 'Urban Puzzles', 'Wildlife Encounters']
        },
        'south-america': {
            description: 'Journey through rainforests and ancient ruins',
            challenges: ['Jungle Survival', 'Archaeological Mysteries', 'River Navigation']
        },
        'europe': {
            description: 'Navigate through rich history and culture',
            challenges: ['Historical Puzzles', 'Language Challenges', 'Cultural Quests']
        },
        'africa': {
            description: 'Adventure across diverse landscapes and cultures',
            challenges: ['Safari Navigation', 'Desert Survival', 'Cultural Exchange']
        },
        'asia': {
            description: 'Master ancient wisdom and modern innovation',
            challenges: ['Temple Puzzles', 'Technology Challenges', 'Martial Arts']
        },
        'australia': {
            description: 'Discover unique wildlife and vast outback',
            challenges: ['Outback Survival', 'Marine Adventures', 'Aboriginal Culture']
        },
        'antarctica': {
            description: 'Survive the ultimate frozen challenge',
            challenges: ['Extreme Weather', 'Scientific Research', 'Survival Skills']
        }
    };
    
    // Create floating info panel
    const infoPanel = document.createElement('div');
    infoPanel.className = 'continent-info-panel';
    infoPanel.innerHTML = `
        <h3>${continentName.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}</h3>
        <p>${details[continentName]?.description || 'Discover amazing adventures!'}</p>
        <ul>
            ${details[continentName]?.challenges.map(challenge => `<li>${challenge}</li>`).join('') || ''}
        </ul>
    `;
    
    // Style the panel
    infoPanel.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(26, 26, 46, 0.95);
        border: 2px solid #4dabf7;
        border-radius: 15px;
        padding: 2rem;
        color: white;
        font-family: 'Space Mono', monospace;
        z-index: 1500;
        backdrop-filter: blur(10px);
        max-width: 400px;
        animation: fadeInScale 0.5s ease-out;
    `;
    
    document.body.appendChild(infoPanel);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        infoPanel.style.animation = 'fadeOutScale 0.5s ease-out';
        setTimeout(() => infoPanel.remove(), 500);
    }, 4000);
    
    // Add animation styles
    if (!document.querySelector('#info-panel-styles')) {
        const style = document.createElement('style');
        style.id = 'info-panel-styles';
        style.textContent = `
            @keyframes fadeInScale {
                0% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
                100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            }
            @keyframes fadeOutScale {
                0% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
                100% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
            }
        `;
        document.head.appendChild(style);
    }
}

function createParticleEffect(element) {
    const particles = [];
    const rect = element.getBoundingClientRect();
    
    for (let i = 0; i < 5; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: #4dabf7;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            left: ${rect.left + Math.random() * rect.width}px;
            top: ${rect.top + Math.random() * rect.height}px;
        `;
        
        document.body.appendChild(particle);
        particles.push(particle);
        
        // Animate particle
        const moveX = (Math.random() - 0.5) * 200;
        const moveY = -Math.random() * 100 - 50;
        
        particle.animate([
            { transform: 'translate(0, 0)', opacity: 1 },
            { transform: `translate(${moveX}px, ${moveY}px)`, opacity: 0 }
        ], {
            duration: 1500,
            easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        }).onfinish = () => particle.remove();
    }
}

function showConnectionLine(hotspot, continentName) {
    // Visual enhancement - could draw SVG line to corresponding card
    // Implementation would depend on specific design requirements
    console.log(`Showing connection to ${continentName}`);
}

function hideConnectionLine() {
    // Hide the connection line
    console.log('Hiding connection line');
}

function launchContinent(continentName, card) {
    // Create launch sequence animation
    card.style.transform = 'translateY(-50px) scale(1.1)';
    card.style.filter = 'brightness(1.5)';
    
    setTimeout(() => {
        // Here you would integrate with your Python game
        console.log(`Launching ${continentName} continent!`);
        
        // Example: Send data to Python backend
        if (typeof pythonInterface !== 'undefined') {
            pythonInterface.launchContinent(continentName);
        } else {
            // Fallback for demo
            alert(`🚀 Launching ${continentName.replace('-', ' ')} adventure!`);
        }
        
        card.style.transform = 'translateY(0) scale(1)';
        card.style.filter = 'brightness(1)';
    }, 1000);
}

function showModal() {
    const modal = document.getElementById('gameModal');
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function hideModal() {
    const modal = document.getElementById('gameModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function addModalEntryAnimation() {
    const modalContent = document.querySelector('.modal-content');
    modalContent.style.animation = 'modalSlideIn 0.5s ease-out';
    
    // Add modal animation styles
    if (!document.querySelector('#modal-animations')) {
        const style = document.createElement('style');
        style.id = 'modal-animations';
        style.textContent = `
            @keyframes modalSlideIn {
                0% { 
                    opacity: 0; 
                    transform: translateY(-50px) scale(0.8); 
                }
                100% { 
                    opacity: 1; 
                    transform: translateY(0) scale(1); 
                }
            }
        `;
        document.head.appendChild(style);
    }
}

function startGameSequence() {
    // Create epic start sequence
    const sequence = document.createElement('div');
    sequence.className = 'game-start-sequence';
    sequence.innerHTML = `
        <div class="sequence-content">
            <h2>🌍 CONTINENTAL QUEST INITIATED 🚀</h2>
            <div class="loading-bar">
                <div class="loading-progress"></div>
            </div>
            <p>Preparing your galactic journey...</p>
        </div>
    `;
    
    sequence.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, #1a1a2e 0%, #0a0a0f 100%);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 3000;
        color: white;
        text-align: center;
    `;
    
    document.body.appendChild(sequence);
    
    // Animate loading bar
    const progressBar = sequence.querySelector('.loading-progress');
    progressBar.style.cssText = `
        width: 0%;
        height: 6px;
        background: linear-gradient(90deg, #4dabf7, #e94560);
        border-radius: 3px;
        transition: width 3s ease-in-out;
    `;
    
    setTimeout(() => {
        progressBar.style.width = '100%';
    }, 100);
    
    setTimeout(() => {
        hideModal();
        sequence.remove();
        
        // Here you would start the actual Python game
        if (typeof pythonInterface !== 'undefined') {
            pythonInterface.startGame().then(result => {
                console.log('🎮 Game start result:', result);
            }).catch(error => {
                console.error('❌ Failed to start game:', error);
            });
        }
    }, 3500);
}

function showDifficultySelection() {
    const modal = document.getElementById('gameModal');
    const modalContent = modal.querySelector('.modal-content');
    
    modalContent.innerHTML = `
        <span class="close">&times;</span>
        <h2>Select Your Challenge Level</h2>
        <div class="difficulty-options">
            <button class="difficulty-btn easy" data-difficulty="easy">
                <span class="difficulty-icon">🌱</span>
                <span class="difficulty-name">Explorer</span>
                <span class="difficulty-desc">Perfect for beginners</span>
            </button>
            <button class="difficulty-btn medium" data-difficulty="medium">
                <span class="difficulty-icon">⚡</span>
                <span class="difficulty-name">Adventurer</span>
                <span class="difficulty-desc">Balanced challenge</span>
            </button>
            <button class="difficulty-btn hard" data-difficulty="hard">
                <span class="difficulty-icon">🔥</span>
                <span class="difficulty-name">Master</span>
                <span class="difficulty-desc">For experienced players</span>
            </button>
            <button class="difficulty-btn extreme" data-difficulty="extreme">
                <span class="difficulty-icon">💀</span>
                <span class="difficulty-name">Legend</span>
                <span class="difficulty-desc">Ultimate challenge</span>
            </button>
        </div>
    `;
    
    // Add difficulty selection styles
    const style = document.createElement('style');
    style.textContent = `
        .difficulty-options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-top: 2rem;
        }
        .difficulty-btn {
            padding: 1rem;
            border: 2px solid transparent;
            border-radius: 10px;
            background: rgba(26, 26, 46, 0.8);
            color: white;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
        }
        .difficulty-btn.easy { border-color: #40c057; }
        .difficulty-btn.medium { border-color: #fab005; }
        .difficulty-btn.hard { border-color: #fd7e14; }
        .difficulty-btn.extreme { border-color: #e03131; }
        .difficulty-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(73, 171, 247, 0.3);
        }
        .difficulty-icon { font-size: 2rem; }
        .difficulty-name { font-weight: 700; }
        .difficulty-desc { font-size: 0.8rem; opacity: 0.7; }
    `;
    document.head.appendChild(style);
    
    // Add event listeners for difficulty buttons
    const difficultyButtons = modalContent.querySelectorAll('.difficulty-btn');
    difficultyButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const difficulty = btn.dataset.difficulty;
            console.log(`Selected difficulty: ${difficulty}`);
            startGameSequence();
        });
    });
    
    // Re-add close functionality
    const closeBtn = modalContent.querySelector('.close');
    closeBtn.addEventListener('click', hideModal);
}

function animateContinentCard(card) {
    card.style.transform = 'translateY(30px)';
    card.style.opacity = '0';
    
    setTimeout(() => {
        card.style.transition = 'all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        card.style.transform = 'translateY(0)';
        card.style.opacity = '1';
    }, Math.random() * 200);
}

function animateFeatureCard(card) {
    card.style.transform = 'scale(0.8)';
    card.style.opacity = '0';
    
    setTimeout(() => {
        card.style.transition = 'all 0.6s ease-out';
        card.style.transform = 'scale(1)';
        card.style.opacity = '1';
    }, Math.random() * 300);
}

// Python Integration Interface
// This object handles communication with Python backends

class PythonInterface {
    constructor() {
        console.log('🔍 [DEBUG] PythonInterface constructor called');
        console.log('🔍 [DEBUG] typeof pywebview:', typeof pywebview);
        console.log('🔍 [DEBUG] pywebview.api available:', typeof pywebview !== 'undefined' && pywebview.api);
        
        this.backend_type = this.detectBackend();
        this.base_url = this.getBaseUrl();
        console.log(`🔗 Detected backend: ${this.backend_type}`);
    }
    
    detectBackend() {
        // Check if running in webview (desktop app)
        // pywebview might not be immediately available, so check multiple ways
        if (typeof pywebview !== 'undefined' && pywebview.api) {
            return 'webview';
        }
        // Alternative check for webview - look for file:// protocol with local files
        else if (window.location.protocol === 'file:' && window.location.href.includes('continental_quest_landing.html')) {
            return 'webview';
        }
        // Check if Flask/Django API is available
        else if (window.location.protocol === 'http:' || window.location.protocol === 'https:') {
            return 'web_api';
        }
        // Default to mock for development
        return 'mock';
    }
    
    getBaseUrl() {
        if (this.backend_type === 'web_api') {
            return window.location.origin;
        }
        return null;
    }
    
    async launchContinent(continentName) {
        console.log(`🚀 Python: Launching ${continentName}`);
        
        try {
            switch (this.backend_type) {
                case 'webview':
                    // Direct call to Python through webview API
                    return await pywebview.api.launch_continent(continentName);
                    
                case 'web_api':
                    // HTTP request to Flask/Django backend
                    const response = await fetch(`${this.base_url}/api/launch/${continentName}`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    return await response.json();
                    
                default:
                    // Mock response for development
                    return {
                        status: 'success',
                        continent: continentName,
                        message: `Mock: Would launch ${continentName}`
                    };
            }
        } catch (error) {
            console.error('Error launching continent:', error);
            return { status: 'error', message: error.message };
        }
    }
    
    async startGame(options = {}) {
        console.log('🎮 [DEBUG] Starting game with options:', options);
        console.log('🎮 [DEBUG] Backend type:', this.backend_type);
        
        try {
            switch (this.backend_type) {
                case 'webview':
                    console.log('🔥 [WEBVIEW] Attempting to call Python API...');
                    
                    // For pywebview, try multiple methods to call the API
                    if (typeof pywebview !== 'undefined' && pywebview.api && pywebview.api.start_game) {
                        console.log('🔥 [WEBVIEW] Using pywebview.api.start_game');
                        return await pywebview.api.start_game(options);
                    } else if (typeof start_game === 'function') {
                        console.log('🔥 [WEBVIEW] Found start_game function');
                        return start_game(options);
                    } else if (window.start_game) {
                        console.log('🔥 [WEBVIEW] Found window.start_game');
                        return window.start_game(options);
                    } else {
                        console.log('🔥 [WEBVIEW] Calling Python directly');
                        // Direct Python call - this will trigger the Python function
                        // We'll return a success and let Python handle the globe launch
                        setTimeout(() => {
                            console.log('🚀 [WEBVIEW] Starting 3D globe directly...');
                            // This should trigger the Python function to start the globe
                            window.postMessage({type: 'START_GLOBE', options: options}, '*');
                        }, 100);
                        
                        return {
                            status: 'success',
                            message: 'Webview: Starting 3D globe...'
                        };
                    }
                    
                case 'web_api':
                    const response = await fetch(`${this.base_url}/api/start-game`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(options)
                    });
                    return await response.json();
                    
                default:
                    return {
                        status: 'success',
                        message: 'Mock: Game would start now'
                    };
            }
        } catch (error) {
            console.error('❌ [ERROR] Starting game failed:', error);
            return { status: 'error', message: error.message };
        }
    }
    
    async setDifficulty(difficulty) {
        console.log(`⚡ Python: Setting difficulty to ${difficulty}`);
        
        try {
            switch (this.backend_type) {
                case 'webview':
                    return await pywebview.api.set_difficulty(difficulty);
                    
                case 'web_api':
                    const response = await fetch(`${this.base_url}/api/difficulty`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ difficulty: difficulty })
                    });
                    return await response.json();
                    
                default:
                    return {
                        status: 'success',
                        difficulty: difficulty,
                        message: `Mock: Difficulty set to ${difficulty}`
                    };
            }
        } catch (error) {
            console.error('Error setting difficulty:', error);
            return { status: 'error', message: error.message };
        }
    }
    
    async getProgress(continent = null) {
        try {
            switch (this.backend_type) {
                case 'webview':
                    return await pywebview.api.get_progress(continent);
                    
                case 'web_api':
                    const url = continent ? 
                        `${this.base_url}/api/progress/${continent}` : 
                        `${this.base_url}/api/progress`;
                    const response = await fetch(url);
                    return await response.json();
                    
                default:
                    // Mock progress data
                    const mockProgress = {
                        'north-america': Math.random() * 100,
                        'south-america': Math.random() * 80,
                        'europe': Math.random() * 90,
                        'africa': Math.random() * 60,
                        'asia': Math.random() * 70,
                        'australia': Math.random() * 95,
                        'antarctica': Math.random() * 30
                    };
                    return continent ? mockProgress[continent] : mockProgress;
            }
        } catch (error) {
            console.error('Error getting progress:', error);
            return 0;
        }
    }
    
    async updateProgress(continent, progress) {
        try {
            switch (this.backend_type) {
                case 'webview':
                    return await pywebview.api.update_progress(continent, progress);
                    
                case 'web_api':
                    const response = await fetch(`${this.base_url}/api/progress/${continent}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ progress: progress })
                    });
                    return await response.json();
                    
                default:
                    return {
                        status: 'success',
                        continent: continent,
                        progress: progress
                    };
            }
        } catch (error) {
            console.error('Error updating progress:', error);
            return { status: 'error', message: error.message };
        }
    }
    
    async testConnection() {
        console.log('🔥 [TEST] Testing Python connection...');
        try {
            switch (this.backend_type) {
                case 'webview':
                    const result = await pywebview.api.test_connection();
                    console.log('🔥 [TEST] Webview result:', result);
                    return result;
                    
                case 'web_api':
                    const response = await fetch(`${this.base_url}/api/test`, {
                        method: 'GET'
                    });
                    return await response.json();
                    
                default:
                    return {
                        status: 'success',
                        message: 'Mock: Connection test successful',
                        backend: this.backend_type
                    };
            }
        } catch (error) {
            console.error('❌ [TEST] Connection test failed:', error);
            return { status: 'error', message: error.message };
        }
    }
}

// Initialize Python interface
window.pythonInterface = new PythonInterface();

// Add some fun Easter eggs
let konamiCode = [];
const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // ↑↑↓↓←→←→BA

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.keyCode);
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    
    if (konamiCode.join('') === konamiSequence.join('')) {
        // Easter egg activated!
        document.body.style.filter = 'hue-rotate(180deg)';
        alert('🎮 Easter Egg Activated! Welcome, master gamer! 🚀');
        setTimeout(() => {
            document.body.style.filter = 'none';
        }, 5000);
        konamiCode = [];
    }
});

console.log(`
🌍 Continental Quest Landing Page Loaded! 🚀
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ready for an epic galactic journey through Earth's continents!
Try the Konami code for a surprise... ↑↑↓↓←→←→BA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`);
