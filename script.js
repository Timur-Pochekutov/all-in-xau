async function actualizarDatos() {
    const response = await fetch("https://all-in-xau-backend.onrender.com/precio-sesion");
    const data = await response.json();
    
    document.querySelector(".precio").textContent = data.precio.toFixed(2);
    const cambioEl = document.querySelector(".cambio");
    cambioEl.textContent = data.cambio_pct !== null ? data.cambio_pct.toFixed(2) + "%" : "-";
    cambioEl.className = "cambio";
    if (data.cambio_pct > 0) cambioEl.classList.add("positivo");
    else if (data.cambio_pct < 0) cambioEl.classList.add("negativo");
    else if (data.cambio_pct === 0) cambioEl.classList.add("neutro");
 }

actualizarDatos();
setInterval(actualizarDatos, 10000);