class Client {
  constructor(address = "127.0.0.1", port = 5555, token = "") {
      this.port = port;
      this.address = address;
      this.base_url = `http://${this.address}:${this.port}/anki_api`;
      this.token = token;
  }

  async create_car(address) {
      if (this.token === "") {
          const response = await fetch(`${this.base_url}/create_car?address=${address}`);
          this.token = await response.text();
          return this.token;
      } else {
          return this.token;
      }
  }

  async set_speed(speed, accel = 1000) {
      const response = await fetch(`${this.base_url}/set_speed?token=${this.token}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              speed: speed,
              accel: accel
          })
      });
      return await response.text();
  }

  async left_lane(lanes = 1.0) {
      const response = await fetch(`${this.base_url}/left_lane?token=${this.token}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              lanes: lanes
          })
      });
      return await response.text();
  }

  async right_lane(lanes = 1.0) {
      const response = await fetch(`${this.base_url}/right_lane?token=${this.token}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              lanes: lanes
          })
      });
      return await response.text();
  }

  async get_cars(active = false) {
      const response = await fetch(`${this.base_url}/get_cars`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              active: active
          })
      });
      const data = await response.json();
      return data.cars;
  }

  async disconnect(force_stop = true) {
      const response = await fetch(`${this.base_url}/disconnect?token=${this.token}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              force_stop: force_stop
          })
      });
      return await response.text();
  }
}
