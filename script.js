async function getGoldPrice() {
    const url = "https://api.gold-api.com/price/XAU";
    const response = await fetch(url);
    const data = await response.json();
    
    const precio = document.querySelector(".precio");
    precio.textContent = data.price.toFixed(2);
}

getGoldPrice();
setInterval(getGoldPrice, 10000);