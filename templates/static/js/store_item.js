let changeMainImage = element => {
    let mainImage = document.getElementById('mainProductImage');
    mainImage.src = element.firstChild.src;
}