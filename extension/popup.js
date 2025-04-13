document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM loaded");

  const recommendationContainer = document.getElementById("recommendations");
  const loadingIndicator = document.createElement("div");
  loadingIndicator.className = "loading-spinner";
  recommendationContainer.appendChild(loadingIndicator);

  const recommendBtn = document.getElementById("recommend-btn");
  const ottSelect = document.getElementById("ott-platform");

  function fetchTopSeries(platform) {
    recommendationContainer.innerHTML = ""; // Clear previous results
    loadingIndicator.style.display = "block"; // Show loading

    fetch(
      `http://localhost:5000/recommend?platform=${encodeURIComponent(platform)}`
    )
      .then((response) => response.json())
      .then((data) => {
        loadingIndicator.style.display = "none"; // Hide loading

        if (!data.recommendations || data.recommendations.length === 0) {
          recommendationContainer.innerHTML =
            "<p>No recommendations found.</p>";
          return;
        }

        data.recommendations.forEach((series) => {
          const seriesCard = document.createElement("li");
          seriesCard.classList.add("series-card");

          seriesCard.innerHTML = `
                      <img src="${series.poster}" alt="${series.title}" class="series-poster">
                      <div class="series-info">
                          <h3>${series.title}</h3>
                          <p>⭐ ${series.rating}</p>
                          <p>${series.description}</p>
                      </div>
                  `;
          recommendationContainer.appendChild(seriesCard);
        });
      })
      .catch((error) => {
        console.error("❌ Fetch Error:", error);
        loadingIndicator.style.display = "none";
        recommendationContainer.innerHTML =
          "<p>Failed to load recommendations.</p>";
      });
  }

  recommendBtn.addEventListener("click", function () {
    const selectedPlatform = ottSelect.value;
    fetchTopSeries(selectedPlatform);
  });
});
