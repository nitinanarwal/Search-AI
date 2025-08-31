# Business Search App - Testing Guide

This guide provides comprehensive test cases for the Business Search App to ensure all features work correctly.

## 🎯 Overview

The Business Search App is a full-stack application with:
- **Backend**: Python Flask API with semantic search, geospatial filtering, and ranking
- **Frontend**: React application with search interface and filters
- **Features**: Natural language search, location-based filtering, cause-based filtering, and multiple sorting options

## 📋 Prerequisites

Before testing, ensure:
1. **Backend is running** on `http://localhost:5000`
2. **Frontend is running** on `http://localhost:5173`
3. **Sample data is loaded** in `backend/data/nonprofits.json`

## 🧪 Test Categories

### 1. Backend API Tests
### 2. Frontend UI Tests
### 3. Search Functionality Tests
### 4. Filtering Tests
### 5. Sorting Tests
### 6. Integration Tests

---

## 1. Backend API Tests

### Test 1.1: Health Check
**Endpoint**: `GET /health`
**Expected Result**:
```json
{
  "status": "ok",
  "count": 6,
  "ts": "2024-01-01T12:00:00.000000"
}
```

### Test 1.2: Get All Organizations
**Endpoint**: `GET /api/businesses`
**Expected Result**:
- Status: 200
- Returns array of 6 nonprofit organizations
- Each organization has: id, name, mission_text, causes, location, ratings

### Test 1.3: Get Specific Organization
**Endpoint**: `GET /api/businesses/org_001`
**Expected Result**:
```json
{
  "success": true,
  "nonprofit": {
    "id": "org_001",
    "name": "Bay Area Housing Aid",
    "causes": ["housing", "families", "anti-homelessness"],
    "location": {"zip": "94103", "lat": 37.7763, "lon": -122.4167}
  }
}
```

### Test 1.4: Organization Not Found
**Endpoint**: `GET /api/businesses/invalid_id`
**Expected Result**:
- Status: 404
- Message: "Not found"

---

## 2. Search Functionality Tests

### Test 2.1: Basic Search
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "limit": 5
}
```
**Expected Result**:
- Returns organizations with "housing" in causes
- Should include: org_001, org_002, org_005, org_006
- Results sorted by relevance score

### Test 2.2: Natural Language Search
**Request**:
```json
POST /api/search
{
  "query": "affordable housing near 94103 for families",
  "limit": 5
}
```
**Expected Result**:
- Intent parsing should extract:
  - Location: zip 94103
  - Causes: ["housing", "families"]
- Should return organizations matching both criteria
- Results should be geographically relevant

### Test 2.3: Location-Based Search
**Request**:
```json
POST /api/search
{
  "query": "veterans",
  "location": {"zip": "85004", "radius_miles": 10},
  "limit": 5
}
```
**Expected Result**:
- Should return "Phoenix Veterans Mental Health" (org_003)
- Distance should be calculated and shown
- Results within 10-mile radius

### Test 2.4: Cause-Based Filtering
**Request**:
```json
POST /api/search
{
  "query": "education",
  "filters": {"cause": ["education", "youth"]},
  "limit": 5
}
```
**Expected Result**:
- Should return "Atlanta Youth Education Fund" (org_004)
- Only organizations with education or youth causes

### Test 2.5: Rating Filter
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "filters": {"min_rating": 4.5},
  "limit": 5
}
```
**Expected Result**:
- Only organizations with avg_rating >= 4.5
- Should include org_001 (4.6 rating)

---

## 3. Sorting Tests

### Test 3.1: Relevance Sorting (Default)
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "sort": "relevance",
  "limit": 3
}
```
**Expected Result**:
- Results sorted by final_score (semantic + geo + trust + popularity)
- Most relevant results first

### Test 3.2: Distance Sorting
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "location": {"zip": "94103", "radius_miles": 25},
  "sort": "distance",
  "limit": 3
}
```
**Expected Result**:
- Results sorted by distance from 94103
- Closest organizations first

### Test 3.3: Rating Sorting
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "sort": "rating",
  "limit": 3
}
```
**Expected Result**:
- Results sorted by avg_rating (highest first)
- org_001 (4.6) should be first

### Test 3.4: Popularity Sorting
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "sort": "popularity",
  "limit": 3
}
```
**Expected Result**:
- Results sorted by popularity_90d (highest first)
- org_001 (0.73) should be first

### Test 3.5: Impact Sorting
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "sort": "impact",
  "limit": 3
}
```
**Expected Result**:
- Results sorted by impact score (1/cost_per_family)
- Lower cost per family = higher impact

### Test 3.6: Newest Sorting
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "sort": "newest",
  "limit": 3
}
```
**Expected Result**:
- Results sorted by created_at (newest first)
- org_005 (2023-06-20) should be first

---

## 4. Frontend UI Tests

### Test 4.1: Page Load
**Action**: Open `http://localhost:5173`
**Expected Result**:
- Page loads without errors
- Search bar is visible
- Cause filter buttons are displayed
- No results shown initially

### Test 4.2: Search Bar Functionality
**Action**: Type "housing" in search bar and click Search
**Expected Result**:
- Loading state shows briefly
- Results appear with housing-related organizations
- Each result shows: name, mission, causes, rating, distance (if location set)

### Test 4.3: Location Filter
**Action**: 
1. Enter ZIP code "94103"
2. Set radius to "10"
3. Search for "housing"
**Expected Result**:
- Results filtered to within 10 miles of 94103
- Distance shown for each result
- Results sorted by relevance within radius

### Test 4.4: Cause Filtering
**Action**:
1. Click "housing" and "families" cause buttons
2. Search for "support"
**Expected Result**:
- Only organizations with housing OR families causes shown
- Filter buttons show active state (different styling)

### Test 4.5: Sort Dropdown
**Action**:
1. Search for "housing"
2. Change sort to "Distance"
**Expected Result**:
- Results re-sorted by distance (if location provided)
- Sort selection persists

### Test 4.6: Error Handling
**Action**: Stop backend server and try to search
**Expected Result**:
- Error message displayed: "Search failed. Check backend and console."
- Loading state clears

---

## 5. Integration Tests

### Test 5.1: End-to-End Search Flow
**Steps**:
1. Open frontend
2. Enter query: "affordable housing for families"
3. Enter ZIP: "94103"
4. Set radius: "15"
5. Select causes: "housing", "families"
6. Click Search
**Expected Result**:
- Results show organizations matching criteria
- Results within 15 miles of 94103
- Organizations have housing or families causes
- Results sorted by relevance

### Test 5.2: Pagination
**Steps**:
1. Search for "housing"
2. Check if more than 12 results exist
3. Verify pagination controls (if implemented)
**Expected Result**:
- First 12 results shown
- Pagination controls visible if more results exist

### Test 5.3: Responsive Design
**Steps**:
1. Test on desktop (full width)
2. Test on tablet (medium width)
3. Test on mobile (narrow width)
**Expected Result**:
- Layout adapts to screen size
- Search bar stacks on mobile
- Cause filters wrap appropriately

---

## 6. Performance Tests

### Test 6.1: Search Response Time
**Action**: Perform multiple searches
**Expected Result**:
- Search response time < 2 seconds
- No timeout errors

### Test 6.2: Large Result Sets
**Action**: Search with broad criteria (e.g., "support")
**Expected Result**:
- All matching results returned
- No memory issues
- Smooth scrolling through results

---

## 7. Data Validation Tests

### Test 7.1: Invalid ZIP Code
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "location": {"zip": "99999", "radius_miles": 10}
}
```
**Expected Result**:
- No geographic filtering applied
- Results returned without distance calculations

### Test 7.2: Invalid Sort Parameter
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "sort": "invalid_sort"
}
```
**Expected Result**:
- Defaults to "relevance" sorting
- No errors thrown

### Test 7.3: Empty Query
**Request**:
```json
POST /api/search
{
  "query": "",
  "limit": 5
}
```
**Expected Result**:
- Returns all organizations (or default results)
- No errors

---

## 8. Edge Cases

### Test 8.1: Very Large Radius
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "location": {"zip": "94103", "radius_miles": 1000}
}
```
**Expected Result**:
- Returns all organizations within 1000 miles
- No performance issues

### Test 8.2: Multiple Cause Filters
**Request**:
```json
POST /api/search
{
  "query": "support",
  "filters": {"cause": ["housing", "families", "education", "veterans"]}
}
```
**Expected Result**:
- Returns organizations matching any of the causes
- Results properly filtered

### Test 8.3: High Rating Filter
**Request**:
```json
POST /api/search
{
  "query": "housing",
  "filters": {"min_rating": 5.0}
}
```
**Expected Result**:
- Returns only organizations with perfect ratings
- Empty results if none exist

---

## 9. Browser Compatibility Tests

### Test 9.1: Chrome
**Action**: Test all features in Chrome
**Expected Result**: All features work correctly

### Test 9.2: Firefox
**Action**: Test all features in Firefox
**Expected Result**: All features work correctly

### Test 9.3: Safari
**Action**: Test all features in Safari
**Expected Result**: All features work correctly

### Test 9.4: Edge
**Action**: Test all features in Edge
**Expected Result**: All features work correctly

---

## 10. Accessibility Tests

### Test 10.1: Keyboard Navigation
**Action**: Navigate using only keyboard (Tab, Enter, Space)
**Expected Result**:
- All interactive elements accessible
- Focus indicators visible
- Search can be performed with keyboard

### Test 10.2: Screen Reader Compatibility
**Action**: Test with screen reader
**Expected Result**:
- Proper ARIA labels
- Semantic HTML structure
- Screen reader can read search results

---

## 📊 Test Results Template

Use this template to record test results:

```
Test Case: [Test ID]
Date: [YYYY-MM-DD]
Tester: [Name]
Status: ✅ PASS / ❌ FAIL / ⚠️ PARTIAL
Notes: [Any observations or issues]
```

## 🐛 Bug Reporting

When reporting bugs, include:
1. **Test case ID**
2. **Steps to reproduce**
3. **Expected vs actual result**
4. **Browser/OS information**
5. **Console errors (if any)**
6. **Screenshots (if applicable)**

## ✅ Success Criteria

All tests should pass for a successful deployment:
- ✅ All API endpoints return correct responses
- ✅ Search functionality works with various queries
- ✅ Filtering and sorting work correctly
- ✅ Frontend displays results properly
- ✅ Error handling works as expected
- ✅ Performance is acceptable (< 2s response time)
- ✅ Cross-browser compatibility maintained

---

## 🔧 Troubleshooting

### Common Issues:
1. **Backend not running**: Check `python server.py` in backend directory
2. **Frontend not loading**: Check `npm run dev` in frontend directory
3. **CORS errors**: Ensure backend CORS is configured
4. **No results**: Check if sample data is loaded
5. **Search not working**: Check browser console for errors

### Debug Commands:
```bash
# Check backend health
curl http://localhost:5000/health

# Test search API
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "housing", "limit": 5}'

# Check frontend
curl http://localhost:5173
```
