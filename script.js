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

async function actualizarMercados() {
        const response = await fetch ("https://all-in-xau-backend.onrender.com/mercados");
        const data = await response.json();

        document.querySelector(".mkt-usd").textContent = data.USD !== null ? data.USD.toFixed(2) : "_";
        document.querySelector(".mkt-eur").textContent = data.EUR !== null ? data.EUR.toFixed(2) : "_";
        document.querySelector(".mkt-gbp").textContent = data.GBP !== null ? data.GBP.toFixed(2) : "_";
        document.querySelector(".mkt-jpy").textContent = data.JPY !== null ? data.JPY.toFixed(2) : "_";
        document.querySelector(".mkt-aud").textContent = data.AUD !== null ? data.AUD.toFixed(2) : "_";
    }
    actualizarMercados();
    setInterval(actualizarMercados, 10000);

async function actualizarETF() {
    const response = await fetch("https://all-in-xau-backend.onrender.com/etf")
    const data = await response.json();

    document.querySelector(".etf-precio").textContent = data.precio !== null ? data.precio.toFixed(2) : "-";

    const cambioEl = document.querySelector(".etf-cambio");
    cambioEl.textContent = data.cambio_pct !== null ? data.cambio_pct.toFixed(2) + "%" : "-";
    cambioEl.className = "etf-cambio";
    
    if (data.cambio_pct > 0) cambioEl.classList.add("positivo");
    else if (data.cambio_pct < 0) cambioEl.classList.add("positivo");
    else if (data.cambio_pct === 0) cambioEl.classList.add("neutro"); 
}

actualizarETF();
setInterval(actualizarETF, 60000);