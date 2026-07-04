function test() {
    alert('hola mundo');
}

function jsAjax() {
    alert('Acción ejecutada');
}

(function() {
    if (document.body.classList.contains('login-page')) return;
    var timer = null;
    function logout() { window.location.href = '/logout'; }
    function reset() {
        clearTimeout(timer);
        timer = setTimeout(logout, 60000);
    }
    ['mousemove', 'click', 'keydown', 'scroll'].forEach(e => document.addEventListener(e, reset, true));
    reset();
})();