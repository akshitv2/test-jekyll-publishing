<input id="i">
<button onclick="setCookie()">Save</button>

<script>
function setCookie(){
  document.cookie = "mickey=" + encodeURIComponent(
    document.getElementById("i").value
  ) + "; path=/; SameSite=Strict";
}
</script>