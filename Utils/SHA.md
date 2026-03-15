---
parent: Utils
nav_order: 2
layout: default
---

# Sha Me

<input id="i">
    <button onclick="shaMe()">ShaMe!</button>
<p id="shamed"/>

<script>
    function shaMe() {
        document.getElementById('shamed').innerHTML = CryptoJS.SHA256(document.getElementById("i").value).toString();
    }
</script>