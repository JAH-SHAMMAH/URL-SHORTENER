// Function to shorten the URL
function shortenUrl() {
  const longUrlInput = document.getElementById("long-url");
  const shortUrlOutput = document.getElementById("short-url");

  const longUrl = longUrlInput.value.trim();

  if (!longUrl) {
    alert("Please enter a valid URL.");
    return;
  }

  //   const shortUrl = "KadWM";

  shortUrlOutput.textContent = shortUrl;
}

document.getElementById("shorten-btn").addEventListener("click", shortenUrl);
