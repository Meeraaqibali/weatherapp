// Wrap your code in a function to initialize it when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    const apiKey = "2afba597ee9a33f8a1e98e9a119bd41a";
    const apiUrl = "https://api.openweathermap.org/data/2.5/weather?units=metric&q=";

    const searchBox = document.querySelector(".search input");
    const searchBtn = document.querySelector(".search button");
    const weatherIcon = document.querySelector(".weather-icon");

    async function checkWeather(city) {
        try {
            const response = await fetch(apiUrl + city + `&appid=${apiKey}`);

            if (!response.ok) {
                throw new Error('Failed to fetch weather data');
            }

            const data = await response.json();
            updateWeather(data);
        } catch (error) {
            console.error('Error fetching weather data:', error);
            displayError();
        }
    }

    function updateWeather(data) {
        document.querySelector(".city").innerHTML = data.name;
        document.querySelector(".temp").innerHTML = Math.round(data.main.temp) + "°c";
        document.querySelector(".humidity").innerHTML = data.main.humidity + "%";
        document.querySelector(".wind").innerHTML = data.wind.speed + " km/h";

        setWeatherIcon(data.weather[0].main);
        displayWeather();
    }

    function setWeatherIcon(weatherCondition) {
        const iconPath = `images/${weatherCondition.toLowerCase()}.png`;
        weatherIcon.src = iconPath;
    }

    function displayWeather() {
        document.querySelector(".weather").style.display = "block";
        document.querySelector(".error").style.display = "none";
    }

    function displayError() {
        document.querySelector(".error").style.display = "block";
        document.querySelector(".weather").style.display = "none";
    }

    searchBtn.addEventListener("click", function() {
        checkWeather(searchBox.value);
    });
});



