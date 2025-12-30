

function checkauth(){

    let email=document.getElementById("email").value;
        let password=document.getElementById("password").value;

        fetch("/login",{
            method:"POST",
            headers:{"content-Type":"application/json"},
             body:JSON.stringyfy({email,password})
        })
        .then(res => res.json())
        .then(data =>{
            if(data.status === "success"){
                alert("login sucess")
                document.getElementById("sec2").style.display = "block";

            }
            else{
                alert("invalid credentials")
            }
        });

        

}





function getweather() {
    var city = document.getElementById("winput").value;
    var apiKey = "YOUR_API_KEY_HERE";

    const url = `https://api.openweathermap.org/data/3.0/weather?q=${city}&units=metric&appid=${apiKey}`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.cod === 200) {
                document.getElementById("weather-right").innerHTML =
                `🌍 City: ${data.name}<br>
                 🌡️ Temp: ${data.main.temp} °C<br>
                 ☁️ Weather: ${data.weather[0].description}`;
            } else {
                document.getElementById("weather-right").innerHTML =
                "❌ City not found";
            }
        })
        .catch(err => {
            console.log(err);
        });
}



