#ifndef ANKI_API_H
#define ANKI_API_H

#include <string>
#include <vector>
#include <cpprest/http_client.h>

using namespace web;
using namespace web::http;
using namespace web::http::client;

class Client {
public:
  Client(const std::string& address, int port = 5555);

  pplx::task<std::string> create_car(const std::string& car);
  pplx::task<std::string> set_speed(int speed, int accel = 1000);
  pplx::task<std::string> left_lane(double lanes = 1.0);
  pplx::task<std::string> right_lane(double lanes = 1.0);
  pplx::task<std::vector<std::string>> get_cars(bool active = false);

private:
  int port;
  std::string address;
  std::string base_url;
  std::string token;
};

#endif  // ANKI_API_H
