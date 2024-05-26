document.addEventListener('DOMContentLoaded', function () {
  const locationInput = document.getElementById('id_location');
  const suggestionsBox = document.getElementById('city-suggestions');

  if (locationInput) {
    locationInput.addEventListener('input', function () {
      const query = locationInput.value;
      if (query.length > 2) {
        fetch(`/auth/fetch-cities/?query=${query}`)
          .then(response => response.json())
          .then(data => {
            suggestionsBox.innerHTML = '';
            data.forEach(city => {
              const item = document.createElement('div');
              item.className = 'list-group-item list-group-item-action';
              item.textContent = `${city.name}, ${city.country}`;
              item.addEventListener('click', function () {
                locationInput.value = item.textContent;
                suggestionsBox.innerHTML = '';
              });
              suggestionsBox.appendChild(item);
            });
          });
      } else {
        suggestionsBox.innerHTML = '';
      }
    });

    document.addEventListener('click', function (event) {
      if (
        !locationInput.contains(event.target) &&
        !suggestionsBox.contains(event.target)
      ) {
        suggestionsBox.innerHTML = '';
      }
    });
  }
});
