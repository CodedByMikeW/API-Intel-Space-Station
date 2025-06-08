import requests
from datetime import  datetime
import smtplib
import time
MY_EMAIL ="Redacted"
MY_PASSWORD="Redacted"

MY_LAT = 40.005974
MY_LONG = -74.005974

def is_iss_overhead():
    response=requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data=response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if MY_LAT-5<= iss_latitude <= MY_LAT+5 and MY_LONG-5<= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters ={
    "lat":MY_LAT,
    "lng":MY_LONG,
    "formatted":0,
}
    response = requests.get('https://api.sunrise-sunset.org/json',params=parameters)
    response.raise_for_status()
    data= response.json()
    sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
    sunset = data["results"]["sunset"].split("T")[1].split(":")[0]

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("stmp.gmail.com",port=587)
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Look up to the sky\n\nThe International Space Station is above in they sky.\nLongitude: {MY_LONG}, Latitude: {MY_LAT} \n From assistant MikeBot "
        )
