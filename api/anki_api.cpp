#include <iostream>
#include <string>
#include <cpprest/http_client.h>
#include <cpprest/json.h>

using namespace web;
using namespace web::http;
using namespace web::http::client;

class Client {
public:
  Client(const std::string& address, int port = 5555) 
    : port(port), address(address), base_url("http://" + address + ":" + std::to_string(port) + "/anki_api"), token("") {}

  pplx::task<std::string> create_car(const std::string& car) {
    http_client client(base_url);
    uri_builder builder("/create_car");
    builder.append_query("address", car);

    return client.request(methods::POST, builder.to_string())
      .then([](http_response response) {
        return response.extract_string();
      })
      .then([this](const std::string& token) {
        this->token = token;
        return token;
      });
  }

  pplx::task<std::string> set_speed(int speed, int accel = 1000) {
    http_client client(base_url);
    uri_builder builder("/set_speed");
    builder.append_query("token", token);
    builder.append_query("speed", speed);
    builder.append_query("accel", accel);

    return client.request(methods::POST, builder.to_string())
      .then([](http_response response) {
        return response.extract_string();
      });
  }

  pplx::task<std::string> left_lane(double lanes = 1.0) {
    http_client client(base_url);
    uri_builder builder("/left_lane");
    builder.append_query("token", token);
    builder.append_query("lanes", lanes);

    return client.request(methods::POST, builder.to_string())
      .then([](http_response response) {
        return response.extract_string();
      });
  }

  pplx::task<std::string> right_lane(double lanes = 1.0) {
    http_client client(base_url);
    uri_builder builder("/right_lane");
    builder.append_query("token", token);
    builder.append_query("lanes", lanes);

    return client.request(methods::POST, builder.to_string())
      .then([](http_response response) {
        return response.extract_string();
      });
  }

  pplx::task<std::vector<std::string>> get_cars(bool active = false) {
    http_client client(base_url);
    uri_builder builder("/get_cars");
    json::value body;
    body["active"] = json::value::boolean(active);

    return client.request(methods::POST, builder.to_string(), body.serialize(), "application/json")
      .then([](http_response response) {
        return response.extract_json();
      })
      .then([](json::value data) {
        std::vector<std::string> cars;
        for (const auto& car : data["cars"].as_array()) {
          cars.push_back(car.as_string());
        }
        return cars;
      });
  }

private:
  int port;
  std::string address;
  std::string base_url;
  std::string token;
};
