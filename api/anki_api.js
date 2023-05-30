class Client {
  constructor(address, port = 5555) {
    this.port = port;
    this.address = address;
    this.base_url = `http://${this.address}:${this.port}/anki_api`;
    this.token = "";
  }

  create_car(car) {
    return fetch(`${this.base_url}/create_car?address=${car}`)
      .then((response) => response.text())
      .then((token) => {
        this.token = token;
        return token;
      });
  }

  set_speed(speed, accel = 1000) {
    return fetch(
      `${this.base_url}/set_speed?token=${this.token}&speed=${speed}&accel=${accel}`
    ).then((response) => response.text());
  }

  left_lane(lanes = 1.0) {
    return fetch(
      `${this.base_url}/left_lane?token=${this.token}&lanes=${lanes}`
    ).then((response) => response.text());
  }

  right_lane(lanes = 1.0) {
    return fetch(
      `${this.base_url}/right_lane?token=${this.token}&lanes=${lanes}`
    ).then((response) => response.text());
  }

  get_cars(active = false) {
    return fetch(`${this.base_url}/get_cars`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ active: active }),
    })
      .then((response) => response.json())
      .then((data) => data.cars);
  }

  disconnect(force_stop = false) {
    return fetch(`${this.base_url}/disconnect?token=${this.token}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ force_stop: force_stop }),
    })
      .then((response) => response.text())
  }
}