document.addEventListener('DOMContentLoaded', () => {
  const contentList = document.getElementById('contentList');
  const takedownForm = document.getElementById('takedownForm');

  async function loadContent() {
    const res = await fetch('/list');
    const data = await res.json();
    contentList.innerHTML = '';
    for (const [id, filename] of Object.entries(data)) {
      const li = document.createElement('li');
      li.innerHTML = `<span><strong>${id}</strong>: ${filename}</span>
                      <a href="/download/${id}">Download</a>`;
      contentList.appendChild(li);
    }
  }

  takedownForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const contentId = document.getElementById('takedownId').value.trim();
    if (!contentId) return alert('Enter content ID');

    const res = await fetch('/takedown', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content_id: contentId })
    });

    const result = await res.json();
    alert(result.message || result.error);
    takedownForm.reset();
    loadContent();
  });

  loadContent();
});
