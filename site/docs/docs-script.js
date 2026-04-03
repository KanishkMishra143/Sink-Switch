document.addEventListener('DOMContentLoaded', () => {
    // --- 1. Mobile Menu Logic ---
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const docsSidebar = document.querySelector('.docs-sidebar');
    const sidebarOverlay = document.createElement('div');
    sidebarOverlay.className = 'sidebar-overlay';
    document.body.appendChild(sidebarOverlay);

    function toggleSidebar() {
        docsSidebar.classList.toggle('active');
        sidebarOverlay.classList.toggle('active');
        document.body.style.overflow = docsSidebar.classList.contains('active') ? 'hidden' : '';
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', toggleSidebar);
    }

    sidebarOverlay.addEventListener('click', toggleSidebar);

    // Close sidebar when clicking a link on mobile
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                toggleSidebar();
            }
        });
    });

    // Close on Escape
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && docsSidebar.classList.contains('active')) {
            toggleSidebar();
        }
    });

    // --- 2. "On This Page" Navigator ---
    const docsContent = document.querySelector('.docs-content');
    const navigatorList = document.getElementById('navigator-list');
    
    if (docsContent && navigatorList) {
        const headings = docsContent.querySelectorAll('h2, h3');
        
        headings.forEach(heading => {
            const id = heading.id || heading.textContent.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
            heading.id = id;
            
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = `#${id}`;
            a.textContent = heading.textContent;
            
            if (heading.tagName === 'H3') {
                li.style.paddingLeft = '1.5rem';
                li.style.fontSize = '0.8rem';
            }
            
            li.appendChild(a);
            navigatorList.appendChild(li);
        });

        // Highlight active heading on scroll
        const observerOptions = {
            root: null,
            rootMargin: '-100px 0px -70% 0px',
            threshold: 0
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    document.querySelectorAll('.navigator-list a').forEach(a => {
                        if (a.getAttribute('href') === `#${id}`) {
                            a.style.color = 'var(--primary)';
                            a.style.fontWeight = '700';
                        } else {
                            a.style.color = '';
                            a.style.fontWeight = '';
                        }
                    });
                }
            });
        }, observerOptions);

        headings.forEach(heading => observer.observe(heading));
    }

    // --- 3. Enhanced Global Docs Search (Algolia Style) ---
    const searchTrigger = document.getElementById('docs-search');
    const searchModal = document.getElementById('search-modal');
    
    // We'll rebuild the modal content to match the new professional style
    if (searchModal) {
        searchModal.innerHTML = `
            <div class="search-modal-container">
                <div class="search-modal-header">
                    <span class="search-icon">🔍</span>
                    <input type="text" class="modal-search-input" id="modal-search-input" placeholder="Search documentation...">
                </div>
                <div class="search-modal-body" id="modal-search-results">
                    <div style="padding: 2rem; text-align: center; color: var(--on-surface-muted);">
                        Type to start searching...
                    </div>
                </div>
                <div class="search-modal-footer">
                    <span><kbd>↵</kbd> to select</span>
                    <span><kbd>↑↓</kbd> to navigate</span>
                    <span><kbd>esc</kbd> to close</span>
                </div>
            </div>
        `;
    }

    const modalInput = document.getElementById('modal-search-input');
    const modalResults = document.getElementById('modal-search-results');

    // Deep search index (simulated)
    const searchIndex = [
        { title: 'Getting Started', category: 'Introduction', url: '../getting-started/index.html', content: 'Lightweight utility for switching audio sinks on Linux and Windows.' },
        { title: 'Linux Installation', category: 'Installation', url: '../installation/index.html', content: 'curl install script, pactl dependencies, pulse and pipewire support.' },
        { title: 'Windows Installation', category: 'Installation', url: '../installation/windows.html', content: 'Go version GUI, AutoHotkey script, powershell installer.' },
        { title: 'CLI Commands', category: 'Usage', url: '../usage/index.html', content: 'sink-switch next, toggle, list, set, quiet mode.' },
        { title: 'Dashboard', category: 'Usage', url: '../usage/dashboard.html', content: 'Graphical interface, device list, volume sliders, system tray.' },
        { title: 'Configuration', category: 'Customization', url: '../configuration/index.html', content: 'config.json, settings.json, primary sink, secondary sink, notifications.' },
        { title: 'Setting Hotkeys', category: 'Customization', url: '../configuration/hotkeys.html', content: 'GNOME shortcuts, KDE global shortcuts, AutoHotkey bindings.' },
        { title: 'FAQ', category: 'Resources', url: '../faq/index.html', content: 'troubleshooting, pipewire compatibility, latency, missing tray icon.' },
        { title: 'PulseAudio vs PipeWire', category: 'Technical', url: '../faq/index.html#pipewire-support', content: 'Compatibility and integration details for modern Linux sound systems.' }
    ];

    function openSearch() {
        searchModal.style.display = 'block';
        setTimeout(() => modalInput.focus(), 50);
    }

    function closeSearch() {
        searchModal.style.display = 'none';
        if (searchTrigger) searchTrigger.blur();
    }

    if (searchTrigger) {
        searchTrigger.addEventListener('click', openSearch);
        searchTrigger.addEventListener('focus', openSearch);
    }

    window.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            openSearch();
        }
        if (e.key === 'Escape' && searchModal && searchModal.style.display === 'block') {
            closeSearch();
        }
    });

    if (searchModal) {
        searchModal.addEventListener('click', (e) => {
            if (e.target === searchModal) closeSearch();
        });
    }

    let selectedIndex = -1;

    if (modalInput) {
        modalInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            if (query.length === 0) {
                modalResults.innerHTML = '<div style="padding: 2rem; text-align: center; color: var(--on-surface-muted);">Type to start searching...</div>';
                return;
            }

            const filtered = searchIndex.filter(item => 
                item.title.toLowerCase().includes(query) || 
                item.content.toLowerCase().includes(query) ||
                item.category.toLowerCase().includes(query)
            );

            renderResults(filtered);
        });

        modalInput.addEventListener('keydown', (e) => {
            const items = modalResults.querySelectorAll('.search-result-item');
            if (items.length === 0) return;

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedIndex = (selectedIndex + 1) % items.length;
                updateSelection(items);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedIndex = (selectedIndex - 1 + items.length) % items.length;
                updateSelection(items);
            } else if (e.key === 'Enter' && selectedIndex >= 0) {
                items[selectedIndex].click();
            }
        });
    }

    function renderResults(results) {
        modalResults.innerHTML = '';
        if (results.length === 0) {
            modalResults.innerHTML = '<div style="padding: 2rem; text-align: center; color: var(--on-surface-muted);">No results found for your query.</div>';
            return;
        }

        // Group by category
        const groups = {};
        results.forEach(item => {
            if (!groups[item.category]) groups[item.category] = [];
            groups[item.category].push(item);
        });

        Object.keys(groups).forEach(cat => {
            const title = document.createElement('div');
            title.className = 'search-results-group-title';
            title.textContent = cat;
            modalResults.appendChild(title);

            groups[cat].forEach(item => {
                const div = document.createElement('div');
                div.className = 'search-result-item';
                div.innerHTML = `
                    <h4>${item.title}</h4>
                    <p>${item.content}</p>
                `;
                div.addEventListener('click', () => {
                    window.location.href = item.url;
                });
                modalResults.appendChild(div);
            });
        });
        
        selectedIndex = -1;
    }

    function updateSelection(items) {
        items.forEach((item, i) => {
            if (i === selectedIndex) {
                item.classList.add('selected');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('selected');
            }
        });
    }
});
