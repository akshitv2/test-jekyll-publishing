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
  document.cookie = "mickey=" + encodeURIComponent(
    document.getElementById("i").value.substring(0,32)) + "; path=/; SameSite=Strict";
}
</script>