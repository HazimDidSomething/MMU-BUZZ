/**
 * Image Zoom Functionality
 * Provides click-to-zoom, hover zoom, mobile gestures, and accessibility features
 */

class ImageZoom {
    constructor() {
        this.modal = null;
        this.currentImage = null;
        this.currentZoom = 1;
        this.maxZoom = 5;
        this.minZoom = 0.5;
        this.zoomStep = 0.2;
        this.isDragging = false;
        this.dragStart = { x: 0, y: 0 };
        this.imagePosition = { x: 0, y: 0 };
        this.touchStartDistance = 0;
        this.touchStartZoom = 1;
        this.hoverTimeout = null;
        this.isHoverZoomEnabled = window.innerWidth > 768;
        
        this.init();
    }

    init() {
        this.createModal();
        this.attachEventListeners();
        this.makeImagesZoomable();
    }

    createModal() {
        // Create modal HTML
        const modalHTML = `
            <div id="image-zoom-modal" class="image-zoom-modal" role="dialog" aria-labelledby="zoom-image-title" aria-hidden="true">
                <div class="zoom-modal-content" tabindex="0">
                    <div class="zoom-loading" id="zoom-loading">Loading...</div>
                    <img id="zoom-image" class="zoom-image" alt="Zoomed image" style="display: none;">
                    <div class="zoom-info" id="zoom-info"></div>
                    <span class="zoom-close" id="zoom-close" role="button" aria-label="Close zoom" tabindex="0">&times;</span>
                    <div class="zoom-controls">
                        <button class="zoom-btn" id="zoom-out" aria-label="Zoom out">
                            <i class="bi bi-zoom-out"></i> Zoom Out
                        </button>
                        <button class="zoom-btn" id="zoom-reset" aria-label="Reset zoom">
                            <i class="bi bi-arrow-clockwise"></i> Reset
                        </button>
                        <button class="zoom-btn" id="zoom-in" aria-label="Zoom in">
                            <i class="bi bi-zoom-in"></i> Zoom In
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Insert modal into body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modal = document.getElementById('image-zoom-modal');
        this.currentImage = document.getElementById('zoom-image');
    }

    attachEventListeners() {
        // Close modal events
        document.getElementById('zoom-close').addEventListener('click', () => this.closeModal());
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.closeModal();
        });

        // Zoom control events
        document.getElementById('zoom-in').addEventListener('click', () => this.zoomIn());
        document.getElementById('zoom-out').addEventListener('click', () => this.zoomOut());
        document.getElementById('zoom-reset').addEventListener('click', () => this.resetZoom());

        // Keyboard events
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));

        // Touch events for mobile
        this.currentImage.addEventListener('touchstart', (e) => this.handleTouchStart(e), { passive: false });
        this.currentImage.addEventListener('touchmove', (e) => this.handleTouchMove(e), { passive: false });
        this.currentImage.addEventListener('touchend', (e) => this.handleTouchEnd(e), { passive: false });

        // Mouse events for desktop
        this.currentImage.addEventListener('mousedown', (e) => this.handleMouseDown(e));
        this.currentImage.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.currentImage.addEventListener('mouseup', (e) => this.handleMouseUp(e));
        this.currentImage.addEventListener('mouseleave', (e) => this.handleMouseUp(e));

        // Prevent context menu on long press
        this.currentImage.addEventListener('contextmenu', (e) => e.preventDefault());

        // Window resize
        window.addEventListener('resize', () => {
            this.isHoverZoomEnabled = window.innerWidth > 768;
            if (this.modal.classList.contains('show')) {
                this.resetZoom();
            }
        });
    }

    makeImagesZoomable() {
        // Find all images and make them zoomable
        const images = document.querySelectorAll('img[src]');
        images.forEach(img => {
            // Skip if already processed
            if (img.classList.contains('zoomable-image')) return;
            
            // Skip very small images (likely icons)
            if (img.width < 100 && img.height < 100) return;
            
            img.classList.add('zoomable-image');
            img.addEventListener('click', (e) => this.openModal(e.target));
            
            // Add hover zoom for desktop
            if (this.isHoverZoomEnabled) {
                this.addHoverZoom(img);
            }
        });
    }

    addHoverZoom(img) {
        const container = document.createElement('div');
        container.className = 'hover-zoom-container';
        img.parentNode.insertBefore(container, img);
        container.appendChild(img);

        const magnifier = document.createElement('div');
        magnifier.className = 'hover-zoom-magnifier';
        container.appendChild(magnifier);

        container.addEventListener('mouseenter', () => {
            magnifier.style.display = 'block';
        });

        container.addEventListener('mouseleave', () => {
            magnifier.style.display = 'none';
        });

        container.addEventListener('mousemove', (e) => {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const magnifierX = x - 75; // Half of magnifier width
            const magnifierY = y - 75; // Half of magnifier height
            
            magnifier.style.left = Math.max(0, Math.min(magnifierX, rect.width - 150)) + 'px';
            magnifier.style.top = Math.max(0, Math.min(magnifierY, rect.height - 150)) + 'px';
            
            // Set background image and position
            magnifier.style.backgroundImage = `url(${img.src})`;
            magnifier.style.backgroundPosition = `-${x * 2}px -${y * 2}px`;
        });
    }

    openModal(img) {
        this.modal.classList.add('show');
        this.modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        
        // Show loading
        document.getElementById('zoom-loading').style.display = 'block';
        this.currentImage.style.display = 'none';
        
        // Load image
        const zoomImg = this.currentImage;
        zoomImg.onload = () => {
            document.getElementById('zoom-loading').style.display = 'none';
            zoomImg.style.display = 'block';
            this.resetZoom();
            this.updateZoomInfo();
            zoomImg.focus();
        };
        
        zoomImg.src = img.src;
        zoomImg.alt = img.alt || 'Zoomed image';
        
        // Update info
        const info = document.getElementById('zoom-info');
        info.textContent = `${img.naturalWidth || img.width} × ${img.naturalHeight || img.height}`;
    }

    closeModal() {
        this.modal.classList.remove('show');
        this.modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
        this.resetZoom();
    }

    zoomIn() {
        this.currentZoom = Math.min(this.currentZoom + this.zoomStep, this.maxZoom);
        this.applyZoom();
    }

    zoomOut() {
        this.currentZoom = Math.max(this.currentZoom - this.zoomStep, this.minZoom);
        this.applyZoom();
    }

    resetZoom() {
        this.currentZoom = 1;
        this.imagePosition = { x: 0, y: 0 };
        this.applyZoom();
    }

    applyZoom() {
        const img = this.currentImage;
        img.style.transform = `scale(${this.currentZoom}) translate(${this.imagePosition.x}px, ${this.imagePosition.y}px)`;
        this.updateZoomInfo();
    }

    updateZoomInfo() {
        const info = document.getElementById('zoom-info');
        const currentText = info.textContent.split(' | ')[0];
        info.textContent = `${currentText} | ${Math.round(this.currentZoom * 100)}%`;
    }

    handleKeyboard(e) {
        if (!this.modal.classList.contains('show')) return;
        
        switch(e.key) {
            case 'Escape':
                this.closeModal();
                break;
            case '+':
            case '=':
                e.preventDefault();
                this.zoomIn();
                break;
            case '-':
                e.preventDefault();
                this.zoomOut();
                break;
            case '0':
                e.preventDefault();
                this.resetZoom();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                this.panImage(-20, 0);
                break;
            case 'ArrowRight':
                e.preventDefault();
                this.panImage(20, 0);
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.panImage(0, -20);
                break;
            case 'ArrowDown':
                e.preventDefault();
                this.panImage(0, 20);
                break;
        }
    }

    panImage(deltaX, deltaY) {
        if (this.currentZoom <= 1) return;
        
        this.imagePosition.x += deltaX;
        this.imagePosition.y += deltaY;
        this.applyZoom();
    }

    handleMouseDown(e) {
        if (this.currentZoom <= 1) return;
        e.preventDefault();
        this.isDragging = true;
        this.dragStart = { x: e.clientX, y: e.clientY };
        this.currentImage.style.cursor = 'grabbing';
    }

    handleMouseMove(e) {
        if (!this.isDragging || this.currentZoom <= 1) return;
        e.preventDefault();
        
        const deltaX = e.clientX - this.dragStart.x;
        const deltaY = e.clientY - this.dragStart.y;
        
        this.imagePosition.x += deltaX;
        this.imagePosition.y += deltaY;
        
        this.dragStart = { x: e.clientX, y: e.clientY };
        this.applyZoom();
    }

    handleMouseUp(e) {
        this.isDragging = false;
        this.currentImage.style.cursor = this.currentZoom > 1 ? 'grab' : 'default';
    }

    handleTouchStart(e) {
        if (e.touches.length === 1) {
            // Single touch - start drag
            this.isDragging = true;
            this.dragStart = { x: e.touches[0].clientX, y: e.touches[0].clientY };
        } else if (e.touches.length === 2) {
            // Two touches - start pinch zoom
            e.preventDefault();
            const touch1 = e.touches[0];
            const touch2 = e.touches[1];
            this.touchStartDistance = Math.sqrt(
                Math.pow(touch2.clientX - touch1.clientX, 2) + 
                Math.pow(touch2.clientY - touch1.clientY, 2)
            );
            this.touchStartZoom = this.currentZoom;
        }
    }

    handleTouchMove(e) {
        if (e.touches.length === 1 && this.isDragging) {
            // Single touch drag
            const deltaX = e.touches[0].clientX - this.dragStart.x;
            const deltaY = e.touches[0].clientY - this.dragStart.y;
            
            this.imagePosition.x += deltaX;
            this.imagePosition.y += deltaY;
            
            this.dragStart = { x: e.touches[0].clientX, y: e.touches[0].clientY };
            this.applyZoom();
        } else if (e.touches.length === 2) {
            // Two touches - pinch zoom
            e.preventDefault();
            const touch1 = e.touches[0];
            const touch2 = e.touches[1];
            const currentDistance = Math.sqrt(
                Math.pow(touch2.clientX - touch1.clientX, 2) + 
                Math.pow(touch2.clientY - touch1.clientY, 2)
            );
            
            const scale = currentDistance / this.touchStartDistance;
            this.currentZoom = Math.max(this.minZoom, Math.min(this.maxZoom, this.touchStartZoom * scale));
            this.applyZoom();
        }
    }

    handleTouchEnd(e) {
        this.isDragging = false;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ImageZoom();
});

// Re-initialize for dynamically loaded content
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'childList') {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    const images = node.querySelectorAll ? node.querySelectorAll('img[src]') : [];
                    if (images.length > 0) {
                        // Re-initialize zoom for new images
                        setTimeout(() => {
                            const zoom = new ImageZoom();
                            zoom.makeImagesZoomable();
                        }, 100);
                    }
                }
            });
        }
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});
