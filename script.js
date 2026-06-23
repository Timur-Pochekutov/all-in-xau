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
    
    const maximoEl = document.querySelector(".maximo");
    maximoEl.textContent = data.maximo !== null ? "↑ " + data.maximo.toFixed(2) : "↑ -";
    
    const minimoEl = document.querySelector(".minimo");
    minimoEl.textContent = data.minimo !== null ? "↓ " + data.minimo.toFixed(2) : "↓ -";
}
actualizarDatos();
setInterval(actualizarDatos, 10000);
