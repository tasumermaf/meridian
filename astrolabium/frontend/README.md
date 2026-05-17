# Astrolabium Caudae Rubrae - Frontend

## Overview

This is the web frontend for the Astrolabium Caudae Rubrae temporal navigation system. It provides a real-time interface to display the alchemical quality of any moment based on sacred time calculations.

## Features

✅ **Location Input**
- Manual lat/lon entry
- Browser geolocation support
- IANA timezone selection
- Settings saved to localStorage

✅ **Three Body Layers Display**
- SOUL (Lunar/Primeval Law)
- ASTRAL (LGBF/Derivative Law)
- GROSS (Organ Clock)

✅ **Organ Clock Visualization**
- 12-segment circular display
- Current organ highlighted
- Wu Xing element color coding
- Emotional correspondences

✅ **Divine Hour Progress**
- Roman numeral display (I-VIII)
- DAY/NIGHT wing indicator
- Progress bar with time remaining
- Solar times (sunrise/sunset)

✅ **Alignment Indicators**
- Law Unity detection
- Anatomical intersection
- Elemental resonance
- Compound level display

✅ **Calendar Panel**
- Divine Month (1-13)
- Gematria values
- Great Rite proximity
- IAO cycle phase

✅ **Auto-Refresh**
- Updates every 60 seconds
- Real-time state tracking

## Running the Application

### Prerequisites

1. **API Server must be running**:
   ```bash
   cd C:\Astrolabium\astrolabium
   python api_server_optimized.py
   ```
   The API runs on http://localhost:8000

2. **Python 3.x** installed

### Start the Frontend

```bash
cd C:\Astrolabium\astrolabium\frontend
python serve.py
```

The frontend will be available at: **http://localhost:3000**

## Architecture

- **Standalone React** - No build tools required
- **In-browser Babel transpilation** - For JSX support
- **Dark theme** - Esoteric aesthetic
- **Mobile responsive** - Works on all devices
- **Minimal dependencies** - Only React from CDN

## File Structure

```
frontend/
├── index.html           # Main HTML with styles
├── app.js              # Main React app component
├── components/
│   ├── LocationInput.js    # Location settings
│   ├── StateDisplay.js     # Three body layers
│   ├── OrganClock.js       # Circular organ visualization
│   ├── DivineHour.js       # Divine hour progress
│   ├── AlignmentPanel.js   # Alignment indicators
│   └── CalendarPanel.js    # Calendar information
├── serve.py            # Python HTTP server
└── README.md          # This file
```

## Elemental System Separation

The frontend maintains strict separation of three elemental vocabularies:

1. **Wu Xing** (Wood, Fire, Earth, Metal, Water)
   - Used ONLY in Organ Clock display
   - Color coded in organ visualization

2. **Damanhurian** (Air, Earth, Fire, Ether, Water)
   - Used ONLY for Great Rite elements
   - Displayed in Calendar Panel

3. **Trigram** (Heaven, Earth, Wind, Thunder, Mountain, Fire, Water, Lake)
   - Used ONLY for Laws
   - Shown with trigram symbols

These systems are NEVER cross-compounded in the UI.

## Browser Support

- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers (iOS/Android)

## Troubleshooting

### "API Connection Error"
- Ensure api_server_optimized.py is running
- Check that port 8000 is not blocked
- Verify http://localhost:8000/health responds

### Location not saving
- Check browser localStorage is enabled
- Clear cache and reload

### No updates
- Verify auto-refresh is enabled
- Check browser console for errors

## Sacred Time Architecture

All calculations use sacred time based on:
- Solar position (sunrise/sunset at location)
- Lunar phase
- NO civil time contamination

Location (lat/lon) is required for all temporal calculations.

## Development

To modify components:
1. Edit the .js files in components/
2. Refresh browser (no build needed)
3. Check browser console for errors

## Performance

- API response time: <100ms (Gate G6 validated)
- Auto-refresh: Every 60 seconds
- Smooth animations and transitions
- Optimized for low bandwidth

---

*Phase 6.2: Frontend Implementation Complete*
*What is the alchemical quality of this moment?*