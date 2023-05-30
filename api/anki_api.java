import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpHeaders;
import java.util.concurrent.CompletableFuture;

public class Client {
    private int port;
    private String address;
    private String base_url;
    private String token;

    public Client(String address, int port) {
        this.port = port;
        this.address = address;
        this.base_url = "http://" + this.address + ":" + this.port + "/anki_api";
        this.token = "";
    }

    public CompletableFuture<String> create_car(String car) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(base_url + "/create_car?address=" + car))
                .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body)
                .thenApply(token -> {
                    this.token = token;
                    return token;
                });
    }

    public CompletableFuture<String> set_speed(int speed, int accel) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(base_url + "/set_speed?token=" + token + "&speed=" + speed + "&accel=" + accel))
                .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body);
    }

    public CompletableFuture<String> left_lane(double lanes) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(base_url + "/left_lane?token=" + token + "&lanes=" + lanes))
                .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body);
    }

    public CompletableFuture<String> right_lane(double lanes) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(base_url + "/right_lane?token=" + token + "&lanes=" + lanes))
                .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body);
    }

    public CompletableFuture<String[]> get_cars(boolean active) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(base_url + "/get_cars"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString("{\"active\":" + active + "}"))
                .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body)
                .thenApply(response -> {
                    HttpHeaders headers = response.headers();
                    String[] cars = headers.map().get("cars").get(0).split(",");
                    return cars;
                });
    }
}
