#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
float sum_rand_float = 0;
int i = 0;
void setup () {
  Serial.begin(115200);
  WiFi.begin("Gokul", "12345678");
  const String node_id = "abcd1234";
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting..");
  }
  Serial.println("Connected to WiFi Network");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
    HTTPClient http;  //Declare an object of class HTTPClient
    int rand = random(7000, 10000);
    float rand_float = rand / 10000;
    sum_rand_float += rand_float;
    uint32_t start_time = millis();
    if (start_time % 1000 == 0) {
      i += 1;
      int stime = start_time / 1000;
      if (i == 14) {
        if (stime % 60 == 0)
        {
          Serial.println(stime);
          String str_rand_float = String(sum_rand_float);
          http.begin("http://192.168.137.1:8090/sendDataToSQL?node_id=abcd1234&voltage=220&current=" + str_rand_float); //Specify request destination
          //int httpCode = http.GET(); //Send the request
          sum_rand_float = 0;
          if (httpCode > 0) { //Check the returning code
            String payload = http.getString();   //Get the request response payload
            Serial.println(payload);             //Print the response payload
          } else {
            Serial.println("An error ocurred");
          }
          http.end();   //Close connection
        }
      }
      i = 0;
    }
    
  }
  //    if(stime%60==0)
  //    {
  //      String str_rand_float=String(sum_rand_float);
  //      http.begin("http://192.168.137.1:8090/sendDataToSQL?node_id=abcd1234&voltage=220&current="+str_rand_float); //Specify request destination
  //      int httpCode = http.GET(); //Send the request
  //      sum_rand_float=0;
  //      if (httpCode > 0) { //Check the returning code
  //      String payload = http.getString();   //Get the request response payload
  //      Serial.println(payload);             //Print the response payload
  //    } else {
  //      Serial.println("An error ocurred");
  //    }
  //    http.end();   //Close connection
  //  }
}
//uint32_t start_time = millis();
//long long int S_time=start_time/1000;
//Serial.println(S_time);
//if(S_time%60==0){
//  Serial.println("YES");
