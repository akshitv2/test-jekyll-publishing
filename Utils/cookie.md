---
parent: Utils
nav_order: 2
layout: default
---

# Cookie Setter

<input id="i">
<button onclick="setCookie()">Save</button>

<script>
function setCookie(){
    const abc = document.getElementById("i").value;
console.log(abc.substring(0,16));

  document.cookie = "mickey=" + encodeURIComponent(
    document.getElementById("i").value.substring(0,16)) + "; path=/; SameSite=Strict";
}
</script>