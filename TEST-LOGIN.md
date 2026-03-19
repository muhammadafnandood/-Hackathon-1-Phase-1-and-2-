# 🔍 Login Test - Step by Step

## Backend is Running ✅
The backend is already running at http://127.0.0.1:8000

## Test Steps:

### 1. Open Browser Console
1. Open `interactive-textbook.html` in browser
2. Press **F12** to open Developer Tools
3. Click on **Console** tab

### 2. Clear Old Data
In console, type:
```javascript
localStorage.clear()
```
Press Enter

### 3. Refresh Page
Press **F5** to refresh

### 4. Create New Account
1. Click "Create New Account"
2. Fill in:
   - **First Name:** Muhammad
   - **Last Name:** Afnan
   - **Email:** afnan@example.com
   - **Password:** test123
3. Click "Create Account"

### 5. Login
1. Enter email: `afnan@example.com`
2. Enter password: `test123`
3. Click "Sign In"

### 6. Check Console Output
You should see:
```
✅ Login successful!
👤 User data: {first_name: "Muhammad", last_name: "Afnan", email: "afnan@example.com"}
💾 Stored user_data: {first_name: "Muhammad", last_name: "Afnan", ...}
🔍 Checking auth status...
📝 Token: Found
📝 User data: Found
✅ User loaded: {first_name: "Muhammad", ...}
👤 First name: Muhammad
👤 Last name: Afnan
👤 Email: afnan@example.com
👤 showUserProfile called
👤 currentUser: {first_name: "Muhammad", ...}
🔍 Checking name fields...
  - first_name: Muhammad
  - firstName: undefined
  - name: undefined
✓ Using first_name: Muhammad
✅ Final displayName: Muhammad
```

### 7. Verify Display
- **Top-right button** should show: **"Muhammad"**
- **Chat message** should say: **"Welcome back, Muhammad!"**

## If Still Showing "test":

### Check Backend Response
In browser console, run:
```javascript
fetch('http://127.0.0.1:8000/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({email: 'afnan@example.com', password: 'test123'})
})
.then(r => r.json())
.then(d => console.log('Backend response:', d))
```

Check what `d.user.first_name` shows.

### Manual Test
In console, run:
```javascript
// Check what's stored
const user = JSON.parse(localStorage.getItem('user_data'));
console.log('Stored user:', user);
console.log('First name:', user.first_name);
```

## Expected Result:
✅ Name shows as **"Muhammad"** (or whatever first name you entered)
❌ NOT "test"
