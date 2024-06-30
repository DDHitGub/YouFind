package CoreScraper;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import org.json.*;

public class CoreScraper {

    static final String URIString = "https://api.core.ac.uk/v3/search/works/";

    //Args: String: Subject,Int: limit, String: output path
    //example: CoreScraper "computer+science", 100, "example/exampleOutput.json"
    //gerade muss man space mit + ersetzen
    public static void main(String[] args) throws Exception {

        if (!(args.length == 3)) throw new RuntimeException("Wrong arguments");
        String Subject = args[0];
        String limit = args[1];
        String path = args[2];

        HttpRequest request = HttpRequest.newBuilder(new URI(URIString+"?q=+AND+fieldsOfStudy%3A%22"+Subject+"%22&limit="+limit)).GET().build();
        HttpClient httpClient = HttpClient.newHttpClient();
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        String body = response.body();
        FileWriter writer = new FileWriter(path);
        JSONArray responseJSON = new JSONObject(body).getJSONArray("results");

        for (Object entry : responseJSON) {
            JSONObject obj = (JSONObject) entry;
            obj.remove("fullText");
            obj.remove("abstract");
        }

        writer.write(responseJSON.toString(1));
        writer.close();
    }
}