async function actualizarDatos() {
    const response = await fetch("https://all-in-xau-backend.onrender.com/precio-sesion");
    const data = await response.json();
    
    document.querySelector(".precio").textContent = data.precio.toFixed(2);
}

actualizarDatos();
setInterval(actualizarDatos, 10000);