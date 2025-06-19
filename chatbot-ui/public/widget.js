// widget.js (host on https://chatbot.mycompany.com/widget.js)
(function() {
  // Read client_id from query
  const params = new URLSearchParams(window.location.search);
  const clientId = params.get('client_id');
  if (!clientId) {
    console.error('[Chatbot] Missing client_id in widget.js URL');
    return;
  }

  // Create toggle button
  const button = document.createElement('button');
  button.innerText = '💬';
  button.style.cssText = [
    'position:fixed', 'bottom:20px', 'right:20px',
    'width:50px','height:50px','border:none','border-radius:50%',
    'background:#4F46E5','color:#fff','font-size:24px','cursor:pointer',
    'box-shadow:0 4px 12px rgba(0,0,0,0.3)','z-index:99999'
  ].join(';');
  document.body.appendChild(button);

  // Create iframe container
  const iframe = document.createElement('iframe');
  iframe.src = `https://chatbot.mycompany.com/?embed=1&client_id=${clientId}`;
  iframe.style.cssText = [
    'position:fixed','bottom:80px','right:20px',
    'width:350px','height:600px','border:none','border-radius:8px',
    'box-shadow:0 8px 24px rgba(0,0,0,0.2)','display:none','z-index:99999'
  ].join(';');
  document.body.appendChild(iframe);

  // Toggle visibility on button click
  button.addEventListener('click', () => {
    iframe.style.display = iframe.style.display === 'none' ? 'block' : 'none';
  });
})();