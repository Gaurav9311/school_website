# Quick Manual Testing Guide - Phase 6 UI/UX Fixes

## Server Status
✅ **Flask server is running at**: http://127.0.0.1:5000

---

## How to Test Each Fix

### Test 1: Gallery Image Aspect Ratios
**URL**: http://127.0.0.1:5000/

**What to look for**:
- [ ] **Mobile (320px)**: 
  - Open DevTools (F12) → Responsive Design Mode
  - Set width to 320px
  - Gallery shows 4 images in a vertical stack
  - Images appear crisp, not stretched or distorted
  - No horizontal scrollbar

- [ ] **Tablet (768px)**:
  - Set width to 768px
  - Gallery shows 2 columns of images
  - All images maintain consistent aspect ratios

- [ ] **Desktop (1440px)**:
  - Set width to 1440px
  - Gallery shows asymmetrical grid (larger and smaller images)
  - Images perfectly aligned without distortion

---

### Test 2: Timetable Responsiveness
**URL**: http://127.0.0.1:5000/school-book-timetable.html

**What to look for**:
- [ ] **Mobile (320px)**:
  - DevTools → Responsive Design Mode → 320px width
  - Timetable table is HIDDEN
  - Cards appear instead showing class names with periods
  - Each card displays "Period 1: Subject, Period 2: Subject" etc.
  - Scroll to see Monday-Wednesday schedule cards
  - NO horizontal scrollbar

- [ ] **Desktop (768px+)**:
  - Set width to 768px or larger
  - Cards are HIDDEN
  - Original timetable with columns for Class, Period 1-8 appears
  - Table fits without horizontal scroll

---

### Test 3: Syllabus Accordion
**URL**: http://127.0.0.1:5000/admission-syllabus.html

**What to look for**:
- [ ] **Page Load**:
  - See 3 accordion headers:
    - Class 1st to 5th
    - Class 6th to 8th
    - Class 9th & 11th

- [ ] **First Accordion Open**:
  - "Class 1st to 5th" section is expanded by default
  - Shows English, Mathematics, Hindi/EVS subject details

- [ ] **Click Second Header**:
  - Click "Class 6th to 8th"
  - First accordion collapses smoothly (animated)
  - Chevron icon rotates 180°
  - Second accordion expands with its content
  - Only ONE accordion open at a time

- [ ] **Mobile (320px)**:
  - Accordions still work perfectly
  - Tap/click header to toggle
  - Smooth expand/collapse animations

---

### Test 4: Parent Portal Cards
**URL**: http://127.0.0.1:5000/

**What to look for**:
- [ ] **Student & Parent Portal Section**:
  - 6 cards: Notice, Timetable, Admission & Syllabus, Faculty List, Planner, Academic Calendar
  
- [ ] **Mobile (320px)**:
  - Cards arranged in 2 columns
  - ALL 6 cards have SAME HEIGHT (no variation)
  - Icons and text aligned consistently

- [ ] **Tablet (768px)**:
  - Cards arranged in 3 columns
  - ALL cards have equal height
  - Consistent spacing

- [ ] **Desktop (1440px)**:
  - Cards arranged in 3 columns
  - ALL cards have equal height
  - Perfect visual alignment

---

### Test 5: Academic Calendar Accordion
**URL**: http://127.0.0.1:5000/academic_calender.html

**What to look for**:
- [ ] **Page Load**:
  - See 3 accordion sections:
    - Academic Terms & Examination Schedule (OPEN by default)
    - Syllabus Bifurcation Plan
    - Major Activity & Event Calendar

- [ ] **First Section Open**:
  - "Academic Terms" table is visible with:
    - Term I Begins, Periodic Tests, Half-Yearly Exams, etc.
    - Full table content visible

- [ ] **Click Other Headers**:
  - Click "Syllabus Bifurcation Plan"
  - First accordion collapses, second expands
  - Chevron rotates
  - Table appears inside accordion

- [ ] **Mobile (320px)**:
  - Accordions visible and working
  - Tables contained within accordion bodies
  - NO horizontal scroll on tables
  - Tap to expand/collapse

- [ ] **Mobile Tables**:
  - Scroll right to see if any content clips
  - Should NOT scroll horizontally (or very minimal if any)

---

## Advanced Testing

### No Horizontal Overflow Check
1. Open DevTools (F12)
2. Go to Console tab
3. Paste this code:
```javascript
if (document.body.scrollWidth > window.innerWidth) {
    console.warn('OVERFLOW DETECTED:', document.body.scrollWidth, 'vs', window.innerWidth);
} else {
    console.log('✓ NO OVERFLOW');
}
```
4. Press Enter
5. Should see "✓ NO OVERFLOW" message

### Accordion Functionality Check
1. Open DevTools (F12)
2. Go to Console tab
3. Paste this code:
```javascript
// Test accordion toggle
const headers = document.querySelectorAll('.accordion-header-custom, .calendar-accordion-header');
console.log('Found ' + headers.length + ' accordion headers');
if (headers.length > 0) {
    console.log('✓ Accordions found and initialized');
} else {
    console.log('✗ No accordions found');
}
```
4. Should see confirmation message

---

## Testing Checklist

### Gallery
- [ ] Mobile: Single column, no distortion
- [ ] Tablet: 2 columns, consistent size
- [ ] Desktop: Asymmetrical layout preserved
- [ ] All images load correctly
- [ ] No horizontal overflow

### Timetable
- [ ] Mobile: Cards visible, not table
- [ ] Mobile: No horizontal scroll
- [ ] Desktop: Table visible, not cards
- [ ] Table doesn't overflow horizontally
- [ ] Period labels clear and readable

### Syllabus
- [ ] Accordions visible
- [ ] First open by default
- [ ] Click toggles accordion
- [ ] Chevron rotates
- [ ] Only one open at a time
- [ ] Works on mobile

### Parent Portal
- [ ] 6 cards visible
- [ ] All same height on mobile
- [ ] All same height on tablet
- [ ] All same height on desktop
- [ ] Icons and text aligned

### Academic Calendar
- [ ] 3 accordion sections
- [ ] First open by default
- [ ] Tables visible inside accordions
- [ ] No horizontal scroll on tables
- [ ] Mobile: Accordions collapse/expand

---

## Troubleshooting

### If accordion doesn't work:
1. Check browser console (F12)
2. Look for errors related to responsive-ui.js
3. Verify script is loaded in page source
4. Try refreshing the page (Ctrl+F5)

### If images look distorted:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh the page (Ctrl+F5)
3. Check network tab in DevTools to ensure images load

### If table overflows:
1. Check viewport width in DevTools
2. Verify responsive.css loaded correctly
3. Look for CSS errors in console

### If cards have different heights:
1. Check if CSS loaded (DevTools → Styles tab)
2. Look for `height: 100%` property on .app-tile
3. Verify browser supports CSS Grid

---

## Browser DevTools Tips

### Open Responsive Design Mode
- **Windows/Linux**: Ctrl+Shift+M
- **Mac**: Cmd+Shift+M

### Set Specific Viewport
- Click device selector dropdown
- Choose "Edit Custom Devices..." to add custom sizes
- Test at: 320px, 480px, 768px, 1024px, 1440px

### Clear Cache
- DevTools → Settings → Network → "Disable cache (while DevTools is open)"
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### View Source Code
- Right-click on element → "Inspect" to see HTML and CSS
- Check for class names and styles applied

---

## All Tests Passing = ✅ Phase 6 Complete!

If all checks pass, congratulations! The Phase 6 UI/UX refinement is fully implemented and working correctly.
