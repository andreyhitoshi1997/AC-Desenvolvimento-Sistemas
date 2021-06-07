let carts = document.querySelectorAll('.btn-cart');
let name_product = document.getElementById("product-name")
let price_product = document.getElementById("product-price")
let products = [{
    name:name_product,
    price:price_product,
    inCart:0
}]

for (let i=0; i < carts.length; i++){
    carts[i].addEventListener('click', () =>{
        cartNumbers(products[i])
    })
}

function onLoadCartNumbers() {
    let productNumbers = localStorage.getItem('cartNumbers')
    if (productNumbers) {
        document.querySelector('.carrinho span').textContent = productNumbers;
    }
}

function cartNumbers(product){
    console.log("the product clicked is ", product)
    let productNumbers = localStorage.getItem('cartNumbers')
    productNumbers = parseInt(productNumbers)

    if(productNumbers){
        localStorage.setItem('cartNumbers',productNumbers + 1)
        document.querySelector('.carrinho span').textContent = productNumbers + 1
        } else{
            localStorage.setItem('cartNumbers',1)
            document.querySelector('.carrinho span').textContent = 1
        }
    }

    onLoadCartNumbers()
    