// نافذة إدخال مفتاح API تلقائياً إذا لم يوجد في localStorage
window.addEventListener('DOMContentLoaded', function() {
  const apiKey = localStorage.getItem('GEMINI_API_KEY');
  if (!apiKey) {
    const modal = new bootstrap.Modal(document.getElementById('apiKeyModal'));
    modal.show();
  }
});

// حفظ المفتاح من النافذة المنبثقة
function setupApiKeyModal() {
  const saveBtn = document.getElementById('modalSaveApiKeyBtn');
  if (!saveBtn) return;
  saveBtn.addEventListener('click', function() {
    const apiKey = document.getElementById('modalApiKeyInput').value.trim();
    if (apiKey) {
      localStorage.setItem('GEMINI_API_KEY', apiKey);
      document.getElementById('modalApiKeyStatus').textContent = 'تم حفظ المفتاح بنجاح!';
      setTimeout(() => {
        const modal = bootstrap.Modal.getInstance(document.getElementById('apiKeyModal'));
        modal.hide();
        location.reload();
      }, 800);
    } else {
      document.getElementById('modalApiKeyStatus').textContent = 'الرجاء إدخال مفتاح صحيح.';
    }
  });
}

// تأكد من تفعيل الحدث بعد إضافة المودال للصفحة
window.addEventListener('DOMContentLoaded', setupApiKeyModal); 