async function actualizarDatos() {
    const response = await fetch("http://localhost:5000/precio-sesion");
    const data = await response.json();
    
    document.querySelector(".precio").textContent = data.precio.toFixed(2);
}

actualizarDatos();
setInterval(actualizarDatos, 10000);