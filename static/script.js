function updateSelectedItem() {
    const selectElement = document.getElementById('item-select');
    const selectedItem = selectElement.options[selectElement.selectedIndex];
    const itemName = selectedItem.value;
    const itemPrice = selectedItem.getAttribute('data-price');
    document.getElementById('item_name').value = itemName;
    document.getElementById('amount').value = itemPrice;
}

function generateQRCode() {
    const itemName = document.getElementById('item_name').value;
    const amount = document.getElementById('amount').value;
    const qrCodeDiv = document.getElementById('qrcode');
    qrCodeDiv.innerHTML = '';
    const qrCodeText = `upi://pay?pa=abilbiju2004@okaxis&pn=ABIL&am=${amount}&cu=INR`;
    new QRCode(qrCodeDiv, {
        text: qrCodeText,
        width: 128,
        height: 128
    });
}