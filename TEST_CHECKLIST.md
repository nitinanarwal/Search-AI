# Business Search App - Test Checklist

## ✅ Quick Test Checklist

Use this checklist to quickly verify all features are working correctly.

### 🔧 Setup Verification
- [ ] Backend running on http://localhost:5000
- [ ] Frontend running on http://localhost:5173
- [ ] Can access frontend in browser
- [ ] No console errors in browser

### 📋 API Endpoints
- [ ] Health check: `GET /health` returns status "ok"
- [ ] Get all organizations: `GET /api/businesses` returns 6 organizations
- [ ] Get specific organization: `GET /api/businesses/org_001` returns Bay Area Housing Aid
- [ ] Organization not found: `GET /api/businesses/invalid_id` returns 404

### 🔍 Search Functionality
- [ ] Basic search "housing" returns housing organizations
- [ ] Natural language search "affordable housing near 94103 for families" works
- [ ] Location search with ZIP code filters results
- [ ] Cause filtering works (housing, families, etc.)
- [ ] Rating filtering works (min_rating: 4.5)

### 📊 Sorting Options
- [ ] Relevance sorting (default) works
- [ ] Distance sorting works (when location provided)
- [ ] Rating sorting works (highest first)
- [ ] Popularity sorting works
- [ ] Impact sorting works
- [ ] Newest sorting works

### 🎨 Frontend UI
- [ ] Page loads without errors
- [ ] Search bar accepts input
- [ ] Search button triggers search
- [ ] Results display correctly
- [ ] Location filters (ZIP, radius) work
- [ ] Cause filter buttons work
- [ ] Sort dropdown works
- [ ] Loading states show during search
- [ ] Error handling works (try stopping backend)

### 🔄 Integration Tests
- [ ] End-to-end search flow works
- [ ] Results update when filters change
- [ ] Multiple filters work together
- [ ] Search with no results handled gracefully

### 📱 Responsive Design
- [ ] Desktop layout looks good
- [ ] Tablet layout adapts properly
- [ ] Mobile layout is usable
- [ ] Search bar stacks on mobile

### ⚡ Performance
- [ ] Search response time < 2 seconds
- [ ] No timeout errors
- [ ] Smooth scrolling through results

### 🐛 Edge Cases
- [ ] Empty search query handled
- [ ] Invalid ZIP code handled
- [ ] Large radius search works
- [ ] Multiple cause filters work
- [ ] High rating filter works

---

## 🚀 Quick Test Commands

### Backend Health Check
```bash
curl http://localhost:5000/health
```

### Test Search API
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "housing", "limit": 5}'
```

### Run Automated Tests
```bash
python test_runner.py
```

---

## 📝 Test Results Log

| Test | Status | Notes |
|------|--------|-------|
| Backend Health | ⬜ | |
| Frontend Load | ⬜ | |
| Basic Search | ⬜ | |
| Location Search | ⬜ | |
| Cause Filtering | ⬜ | |
| Rating Filtering | ⬜ | |
| Relevance Sort | ⬜ | |
| Distance Sort | ⬜ | |
| Rating Sort | ⬜ | |
| Popularity Sort | ⬜ | |
| Impact Sort | ⬜ | |
| Newest Sort | ⬜ | |
| Error Handling | ⬜ | |
| Responsive Design | ⬜ | |
| Performance | ⬜ | |

**Legend**: ✅ PASS | ❌ FAIL | ⚠️ PARTIAL | ⬜ NOT TESTED

---

## 🐛 Common Issues & Solutions

### Backend Not Starting
- Check if port 5000 is available
- Verify Python dependencies are installed
- Check for syntax errors in server.py

### Frontend Not Loading
- Check if port 5173 is available
- Verify Node.js dependencies are installed
- Check browser console for errors

### Search Not Working
- Verify backend is running
- Check CORS configuration
- Look for network errors in browser console

### No Results
- Check if sample data is loaded
- Verify search query is valid
- Check if filters are too restrictive

### Slow Performance
- Check backend logs for errors
- Verify database/index is built
- Check network connectivity

---

## 📊 Success Criteria

All tests should pass for a successful deployment:
- ✅ All API endpoints return correct responses
- ✅ Search functionality works with various queries
- ✅ Filtering and sorting work correctly
- ✅ Frontend displays results properly
- ✅ Error handling works as expected
- ✅ Performance is acceptable (< 2s response time)
- ✅ Cross-browser compatibility maintained

---

## 🎯 Testing Tips

1. **Start with basic functionality** before testing edge cases
2. **Test one feature at a time** to isolate issues
3. **Use the automated test runner** for quick API validation
4. **Check browser console** for JavaScript errors
5. **Test on different browsers** for compatibility
6. **Document any issues** found during testing
7. **Verify error messages** are user-friendly
8. **Test with different screen sizes** for responsive design

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section in `TESTING_GUIDE.md`
2. Review browser console for errors
3. Check backend logs for Python errors
4. Verify all prerequisites are met
5. Test with the automated test runner
