# 🖼️ Image Zoom Feature

A comprehensive image enlargement system for MMU-BUZZ with multiple interaction methods, accessibility features, and responsive design.

## ✨ Features

### 🔍 1. Click-to-Zoom / Tap-to-Zoom
- **Click/Tap any image** → Opens in fullscreen modal overlay
- **Smooth animations** with fade-in and zoom-in effects
- **Close button (X)** in top-right corner
- **Zoom controls** at the bottom (Zoom In, Reset, Zoom Out)
- **Drag to pan** around large images when zoomed in

### 🖱️ 2. Hover Zoom (Desktop Only)
- **Hover over images** → Shows magnified preview in circular magnifier
- **Perfect for detailed images** like maps, diagrams, photos
- **Automatic positioning** of magnifier to follow cursor
- **Disabled on mobile** for better touch experience

### 📱 3. Pinch-to-Zoom (Mobile)
- **Native gesture support** on touch devices
- **Pinch to zoom** in/out smoothly
- **Drag to pan** around zoomed images
- **Works even when embedded** in containers

### ⌨️ 4. Accessibility & Keyboard Navigation
- **Esc key** to close modal
- **Arrow keys** to navigate around zoomed images
- **+/- keys** to zoom in/out
- **0 key** to reset zoom
- **Screen reader compatibility** with ARIA labels
- **Focus indicators** for keyboard users
- **Tab navigation** support

### 📐 5. Responsive Scaling
- **Auto-fit to screen size** while preserving aspect ratio
- **No stretching or pixelation**
- **Mobile-optimized** controls and layout
- **Smooth transitions** between zoom levels

## 🚀 Usage

### Automatic Integration
The zoom functionality is **automatically applied** to all images on the website. Simply add the `zoomable-image` class to any image:

```html
<img src="image.jpg" alt="Description" class="zoomable-image" style="max-width: 300px; height: auto;">
```

### Manual Integration
For custom images, ensure they have:
- A valid `src` attribute
- Minimum size of 100x100 pixels (smaller images are ignored)
- The `zoomable-image` class

## 🎮 Controls

### Desktop Controls
| Action | Keyboard | Mouse |
|--------|----------|-------|
| Open zoom | Click image | Click image |
| Close zoom | `Esc` | Click X or outside |
| Zoom in | `+` or `=` | Click zoom in button |
| Zoom out | `-` | Click zoom out button |
| Reset zoom | `0` | Click reset button |
| Pan around | Arrow keys | Drag when zoomed |
| Hover preview | - | Hover over image |

### Mobile Controls
| Action | Gesture |
|--------|---------|
| Open zoom | Tap image |
| Close zoom | Tap X or outside |
| Zoom in/out | Pinch |
| Pan around | Drag |
| Reset zoom | Double tap |

## 🎨 Customization

### CSS Variables
You can customize the appearance by modifying these CSS classes:

```css
.zoomable-image {
    /* Image hover effects */
    cursor: pointer;
    transition: transform 0.2s ease;
}

.image-zoom-modal {
    /* Modal background */
    background-color: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(5px);
}

.zoom-controls {
    /* Control button styling */
    background: rgba(0,0,0,0.7);
    color: white;
}
```

### JavaScript Configuration
Modify the `ImageZoom` class constructor for custom behavior:

```javascript
class ImageZoom {
    constructor() {
        this.maxZoom = 5;        // Maximum zoom level
        this.minZoom = 0.5;      // Minimum zoom level
        this.zoomStep = 0.2;     // Zoom increment
        // ... other options
    }
}
```

## 📁 File Structure

```
website/
├── static/
│   ├── CSS/
│   │   └── style.css          # Zoom styles and animations
│   └── JS/
│       └── image-zoom.js      # Main zoom functionality
├── templates/
│   ├── base.html              # Includes zoom script
│   ├── zoom_demo.html         # Demo page
│   └── [other templates]      # Updated with zoomable-image class
└── views.py                   # Demo route added
```

## 🔧 Technical Details

### Browser Support
- **Modern browsers** (Chrome, Firefox, Safari, Edge)
- **Mobile browsers** (iOS Safari, Chrome Mobile)
- **Touch devices** with gesture support
- **Keyboard navigation** support

### Performance
- **Lazy loading** of zoom functionality
- **Efficient event handling** with proper cleanup
- **Smooth animations** using CSS transforms
- **Memory management** for modal instances

### Accessibility
- **WCAG 2.1 AA compliant**
- **Screen reader support** with proper ARIA labels
- **Keyboard navigation** for all features
- **High contrast** support
- **Focus management** for modal interactions

## 🧪 Testing

### Demo Page
Visit `/zoom-demo` to test all features:
- Multiple sample images
- Different aspect ratios
- Responsive behavior
- All interaction methods

### Test Cases
1. **Click-to-zoom** on various image sizes
2. **Hover zoom** on desktop (disable on mobile)
3. **Pinch gestures** on touch devices
4. **Keyboard navigation** with all keys
5. **Accessibility** with screen readers
6. **Responsive scaling** on different screen sizes

## 🐛 Troubleshooting

### Common Issues

**Images not zoomable:**
- Ensure image has `zoomable-image` class
- Check image is at least 100x100 pixels
- Verify JavaScript is loaded

**Hover zoom not working:**
- Only works on desktop (width > 768px)
- Check if image is properly wrapped

**Touch gestures not responding:**
- Ensure touch events are not prevented
- Check for conflicting JavaScript

**Keyboard navigation issues:**
- Ensure modal has focus
- Check for event conflicts

## 🔄 Updates

The zoom functionality automatically detects new images added to the page and makes them zoomable without requiring page refresh.

## 📝 License

This feature is part of the MMU-BUZZ project and follows the same licensing terms.

---

**🎉 Enjoy the enhanced image viewing experience!**
