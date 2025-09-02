@@ .. @@
 // ===== NOTIFICATIONS =====
 function showNotification(message, type = 'info', duration = 5000) {
     const notification = document.createElement('div');
-    notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
+    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show notification-toast`;
     notification.style.cssText = `
         position: fixed;
         top: 20px;
@@ .. @@
     return modalInstance;
 }
 
+// Global notification function for compatibility
+window.showNotification = showNotification;
+
 // ===== LOADING STATES =====
 function showLoading(element, text = 'Loading...') {
     element.classList.add('loading');
@@ .. @@
     element.disabled = false;
 }
 
+// Global loading functions for compatibility
+window.showPrimaryLoader = function() {
+    const loader = document.createElement('div');
+    loader.id = 'primaryLoader';
+    loader.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center';
+    loader.style.cssText = 'background: rgba(0,0,0,0.5); z-index: 9999;';
+    loader.innerHTML = `
+        <div class="spinner-border text-primary" role="status">
+            <span class="visually-hidden">Loading...</span>
+        </div>
+    `;
+    document.body.appendChild(loader);
+};
+
+window.hidePrimaryLoader = function() {
+    const loader = document.getElementById('primaryLoader');
+    if (loader) {
+        loader.remove();
+    }
+};
+
 // ===== API HELPERS =====
 async function apiRequest(url, options = {}) {
     const defaultOptions = {