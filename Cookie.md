# Cookie

<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>

<script>
const decryptData = (ciphertext, key, iv) => {

    const keyParsed = CryptoJS.enc.Utf8.parse(key);
    const ivParsed = CryptoJS.enc.Base64.parse(iv);

    const bytes = CryptoJS.AES.decrypt(ciphertext, keyParsed, {
        iv: ivParsed,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });

    return bytes.toString(CryptoJS.enc.Utf8);
};

const secretKey = "sixteen_byte_key";
const message = "EjoZOspxiXFpY9HQiqJqDGwmIa8DuF8TbNeqQi7rZ10=";
const iv = "5vmRg/wCfA/8CVQwnIA/hw==";

console.log(decryptData(message, secretKey, iv));
</script>
